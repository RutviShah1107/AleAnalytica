from __future__ import absolute_import

from collections import OrderedDict

from plotly import exceptions, optional_imports
from plotly.graph_objs import graph_objs

# Optional imports, may be None for users that only use our core functionality.
np = optional_imports.get_module("numpy")
scp = optional_imports.get_module("scipy")
sch = optional_imports.get_module("scipy.cluster.hierarchy")
scs = optional_imports.get_module("scipy.spatial")


def create_dendrogram(
    X,
    orientation="bottom",
    labels=None,
    colorscale=None,
    distfun=None,
    linkagefun=lambda x: sch.linkage(x, "ward"),
    hovertext=None,
    color_threshold=None,
    **kwargs
):
    if not scp or not scs or not sch:
        raise ImportError(
            "FigureFactory.create_dendrogram requires scipy, \
                            scipy.spatial and scipy.hierarchy"
        )

    s = X.shape
    if len(s) != 2:
        exceptions.PlotlyError("X should be 2-dimensional array.")

    if distfun is None:
        distfun = scs.distance.pdist

    dendrogram = _Dendrogram(
        X,
        orientation,
        labels,
        colorscale,
        distfun=distfun,
        linkagefun=linkagefun,
        hovertext=hovertext,
        color_threshold=color_threshold,
        kwargs=kwargs
    )

    return graph_objs.Figure(data=dendrogram.data, layout=dendrogram.layout)


class _Dendrogram(object):
    """Refer to FigureFactory.create_dendrogram() for docstring."""

    def __init__(
        self,
        X,
        orientation="bottom",
        labels=None,
        colorscale=None,
        width=np.inf,
        height=np.inf,
        xaxis="xaxis",
        yaxis="yaxis",
        distfun=None,
        linkagefun=lambda x: sch.linkage(x, "ward"),
        hovertext=None,
        color_threshold=None,
        kwargs=None
    ):
        self.orientation = orientation
        self.labels = labels
        self.xaxis = xaxis
        self.yaxis = yaxis
        self.data = []
        self.leaves = []
        self.sign = {self.xaxis: 1, self.yaxis: 1}
        self.layout = {self.xaxis: {}, self.yaxis: {}}

        if self.orientation in ["left", "bottom"]:
            self.sign[self.xaxis] = 1
        else:
            self.sign[self.xaxis] = -1

        if self.orientation in ["right", "bottom"]:
            self.sign[self.yaxis] = 1
        else:
            self.sign[self.yaxis] = -1

        if distfun is None:
            distfun = scs.distance.pdist

        (dd_traces, xvals, yvals, ordered_labels, leaves) = self.get_dendrogram_traces(
            X, colorscale, distfun, linkagefun, hovertext, color_threshold, kwargs
        )

        self.labels = ordered_labels
        self.leaves = leaves
        yvals_flat = yvals.flatten()
        xvals_flat = xvals.flatten()

        self.zero_vals = []

        for i in range(len(yvals_flat)):
            if yvals_flat[i] == 0.0 and xvals_flat[i] not in self.zero_vals:
                self.zero_vals.append(xvals_flat[i])

        if len(self.zero_vals) > len(yvals) + 1:
           
            l_border = int(min(self.zero_vals))
            r_border = int(max(self.zero_vals))
            correct_leaves_pos = range(
                l_border, r_border + 1, int((r_border - l_border) / len(yvals))
            )
            self.zero_vals = [v for v in correct_leaves_pos]

        self.zero_vals.sort()
        self.layout = self.set_figure_layout(width, height)
        self.data = dd_traces

        self.add_vertical_line(xvals.max(), color="black", width=1, dash="dash")

    def add_vertical_line(self, x_value, color, width, dash):
        line = dict(
            type="line",
            x0=0,
            x1=x_value + 5,
            y0=140,
            y1=140,
            line=dict(color=color, width=width, dash=dash),
        )
        self.layout["shapes"] = [line]


    def get_color_dict(self, colorscale):
        d = {
            "r": "red",
            "g": "green",
            "b": "blue",
            "c": "cyan",
            "m": "magenta",
            "y": "yellow",
            "k": "black",
            "w": "white",
        }
        default_colors = OrderedDict(sorted(d.items(), key=lambda t: t[0]))

        if colorscale is None:
            rgb_colorscale = [
                "rgb(0,116,217)",  # blue
                "rgb(35,205,205)",  # cyan
                "rgb(61,153,112)",  # green
                "rgb(40,35,35)",  # black
                "rgb(133,20,75)",  # magenta
                "rgb(255,65,54)",  # red
                "rgb(255,255,255)",  # white
                "rgb(255,220,0)",  # yellow
            ]
        else:
            rgb_colorscale = colorscale

        for i in range(len(default_colors.keys())):
            k = list(default_colors.keys())[i]  # PY3 won't index keys
            if i < len(rgb_colorscale):
                default_colors[k] = rgb_colorscale[i]

    
        new_old_color_map = [
            ("C0", "b"),
            ("C1", "g"),
            ("C2", "r"),
            ("C3", "c"),
            ("C4", "m"),
            ("C5", "y"),
            ("C6", "k"),
            ("C7", "g"),
            ("C8", "r"),
            ("C9", "c"),
        ]
        for nc, oc in new_old_color_map:
            try:
                default_colors[nc] = default_colors[oc]
            except KeyError:
                default_colors[nc] = "rgb(0,116,217)"

        return default_colors

    def set_axis_layout(self, axis_key):
        
        axis_defaults = {
            "type": "linear",
            "ticks": "outside",
            "mirror": "allticks",
            "rangemode": "tozero",
            "showticklabels": True,
            "zeroline": False,
            "showgrid": False,
            "showline": True,
        }

        if len(self.labels) != 0:
            axis_key_labels = self.xaxis
            if self.orientation in ["left", "right"]:
                axis_key_labels = self.yaxis
            if axis_key_labels not in self.layout:
                self.layout[axis_key_labels] = {}
            self.layout[axis_key_labels]["tickvals"] = [
                zv * self.sign[axis_key] for zv in self.zero_vals
            ]
            self.layout[axis_key_labels]["ticktext"] = self.labels
            self.layout[axis_key_labels]["tickmode"] = "array"

        self.layout[axis_key].update(axis_defaults)

        return self.layout[axis_key]

    def set_figure_layout(self, width, height):
        """
        Sets and returns default layout object for dendrogram figure.

        """
        self.layout.update(
            {
                "showlegend": False,
                "autosize": False,
                "hovermode": "closest",
                "width": width,
                "height": height,
            }
        )

        self.set_axis_layout(self.xaxis)
        self.set_axis_layout(self.yaxis)

        return self.layout

    def get_dendrogram_traces(
        self, X, colorscale, distfun, linkagefun, hovertext, color_threshold, kwargs={}
    ):
        
        d = distfun(X)
        Z = linkagefun(d)
        P = sch.dendrogram(
            Z,
            orientation=self.orientation,
            labels=self.labels,
            no_plot=True,
            color_threshold=color_threshold,
            **kwargs
        )

        icoord = np.array(P["icoord"])
        dcoord = np.array(P["dcoord"])
        ordered_labels = np.array(P["ivl"])
        color_list = np.array(P["color_list"])
        colors = self.get_color_dict(colorscale)

        trace_list = []

        for i in range(len(icoord)):
            # xs and ys are arrays of 4 points that make up the '∩' shapes
            # of the dendrogram tree
            if self.orientation in ["top", "bottom"]:
                xs = icoord[i]
            else:
                xs = dcoord[i]

            if self.orientation in ["top", "bottom"]:
                ys = dcoord[i]
            else:
                ys = icoord[i]
            color_key = color_list[i]
            hovertext_label = None
            if hovertext:
                hovertext_label = hovertext[i]
            trace = dict(
                type="scatter",
                x=np.multiply(self.sign[self.xaxis], xs),
                y=np.multiply(self.sign[self.yaxis], ys),
                mode="lines",
                marker=dict(color=colors[color_key]),
                text=hovertext_label,
                hoverinfo="text",
            )

            try:
                x_index = int(self.xaxis[-1])
            except ValueError:
                x_index = ""

            try:
                y_index = int(self.yaxis[-1])
            except ValueError:
                y_index = ""

            trace["xaxis"] = "x" + x_index
            trace["yaxis"] = "y" + y_index

            trace_list.append(trace)

        return trace_list, icoord, dcoord, ordered_labels, P["leaves"]
