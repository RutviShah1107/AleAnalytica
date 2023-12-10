import plotly.graph_objects as go
import pandas as pd
from .read_data import ReadData
from .split_text import SplitText
from plotly.subplots import make_subplots
import json
import plotly
import numpy as np

class AttitudeColumnsLikert:
    def __init__(self, df: pd.DataFrame(), question: str, cluster: int):
        self.df = df
        self.df_subset = df
        self.question = question
        self.cluster = cluster
        self.mapping = {}
        self.mapping_dict = {}
        self.mapping_df = pd.DataFrame()
        self.df_likert = pd.DataFrame()
        self.df_likert_secondary = pd.DataFrame()

        with open('./data/cluster_names.json', 'r') as file:
            self.cluster_mapping = json.load(file)

        self.create_mapping_dict()
        
    def read_mapping_file(self):
        rd = ReadData('./data/mapping_file.csv')
        return rd.read_dataframe()

    def create_mapping_dict(self):
        self.mapping_df = self.read_mapping_file()
        self.mapping_dict = {row['Columns']: [row['Options'], row['OptionsSet2']] for _, row in self.mapping_df.iterrows() if str(row['Columns']).startswith(self.question + '_')}
        st = SplitText()
        self.mapping_dict = st.split_dict_text(self.mapping_dict)

    def choose_categories(self, column):
        category_dict = {
            'A2': ['Not at all important', 'Somewhat unimportant', 'Neutral', 'Somewhat important', 'Extremely important'],
            'A4': ['Disagree strongly', 'Disagree slightly','Neither agree nor disagree', 'Agree slightly', 'Agree strongly'],
            'A5': ['Does not describe me at all',  'Does not really describe me', 'Neutral', 'Slightly describes me', 'Describes me perfectly'],
            'A8': ['I hate it',  'Somewhat hate', 'Neutral', 'Somewhat like', 'I love it'],
            'A9': ['I hate it',  'Somewhat hate', 'Neutral', 'Somewhat like', 'I love it']

        }
        return category_dict[column]

    def subset_dataframe_single(self):
        self.df_subset = self.df[self.df['Cluster_number'] == self.cluster]
        columns = self.df.columns[self.df.columns.str.startswith(self.question + '_')].to_list()
        self.df_subset = self.df_subset[columns]
        if self.question != 'A8' and self.question != 'A9':
            results = {col: [self.df_subset[col].eq(value).sum() for value in [-1, -0.5, 0, 0.5, 1]] for col in columns}
        else:
            results = {col: np.histogram(self.df_subset[col], bins=[0, 2, 3, 4, 5, 7])[0].tolist() for col in columns}

        combined_results = {self.mapping_dict[key][0]: results[key] for key in self.mapping_dict}
        d = {'Question': list(combined_results.keys())}
        category_names = self.choose_categories(self.question)
        for category in category_names:
            d[category] = [result[category_names.index(category)] for result in combined_results.values()]
        self.df_likert = pd.DataFrame(d)

    def subset_dataframe_double(self):
        self.df_subset = self.df[self.df['Cluster_number'] == self.cluster]
        columns = self.df.columns[self.df.columns.str.startswith(self.question + '_')].to_list()
        self.df_subset = self.df_subset[columns]
        results = {col: [self.df_subset[col].eq(value).sum() for value in [-1, -0.5, 0.5, 1]] for col in columns}

        combined_results = {self.mapping_dict[key][0]: results[key] for key in self.mapping_dict}

        dl = {'Question': list(self.mapping_dict[key][0] for key in self.mapping_dict)}
        dl['Strongly agree'] = [result[0] for result in combined_results.values()]
        dl['Agree'] = [result[1] for result in combined_results.values()]

        dr = {'Question': list(self.mapping_dict[key][1] for key in self.mapping_dict)}
        dr['Strongly agree'] = [result[3] for result in combined_results.values()]
        dr['Agree'] = [result[2] for result in combined_results.values()]

        self.df_likert = pd.DataFrame(dl)
        self.df_likert_secondary = pd.DataFrame(dr)

    def generate_graph_single(self):
        self.subset_dataframe_single()
        colors = ['#FFAAAA', '#FF0000', 'lightgrey', '#AAFFAA', '#00FF00']
        i=0
        fig = go.Figure()
        for col in self.df_likert.columns[2:0:-1]:
            fig.add_trace(go.Bar(x=-self.df_likert[col].values,
                                y=self.df_likert['Question'],
                                orientation='h',
                                name=col,
                                customdata=self.df_likert[col],
                                width=0.5,
                                hovertemplate = "%{y}: %{customdata}",
                        marker=dict(color=colors[i])))
            i+=1
        for col in self.df_likert.columns[3:]:
            fig.add_trace(go.Bar(x= self.df_likert[col],
                                y = self.df_likert['Question'],
                                orientation='h',
                                name= col,
                                width=0.5,
                                hovertemplate="%{y}: %{x}",
                        marker=dict(color=colors[i])))
            i+=1

        fig.update_layout(barmode='relative',
                        height=800,
                        width=1000,
                        yaxis_autorange='reversed',
                        bargap=0.1,
                        legend_orientation ='h',
                        legend_x=-0.05, 
                        legend_y=1.1,
                        title={
                                'text': f"<b>{self.cluster_mapping[str(self.cluster)]}</b>",  # Set the cluster name as bold
                                'x': 0.1,  # Set the x-position of the title in the middle
                                'y': 0.95,  # Set the y-position of the title near the top
                                'xanchor': 'center',  # Align the title to the center horizontally
                                'yanchor': 'top',  # Align the title to the top vertically
                                # 'font': dict(size=18)  # Adjust the font size of the title
                            }                 )
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON


    def generate_graph_double(self):
        self.subset_dataframe_double()
        colors = ['#ADD8E6','#0000FF', '#AAFFAA', '#00FF00']
        i=0
        fig = go.Figure()
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        for col in self.df_likert.columns[2:0:-1]:
            fig.add_trace(go.Bar(x=-self.df_likert[col].values,
                                y=self.df_likert['Question'],
                                orientation='h',
                                name=col,
                                customdata=self.df_likert[col],
                                width=0.5,
                                hovertemplate = "%{y}: %{customdata}",
                        marker=dict(color=colors[i])),
                        secondary_y = False)
            i+=1
        for col in self.df_likert_secondary.columns[1:]:
            fig.add_trace(go.Bar(x= self.df_likert_secondary[col],
                                y = self.df_likert_secondary['Question'],
                                orientation='h',
                                name= col,
                                width=0.5,
                                hovertemplate="%{y}: %{x}",
                        marker=dict(color=colors[i])), secondary_y = True)
            i+=1

        fig.update_layout(barmode='relative',
                        height=1000,
                        width=1000,
                        yaxis_autorange='reversed',
                        bargap=0.1,
                        legend_orientation ='h',
                        legend_x=-0.05, 
                        legend_y=1.1,
                        title={
                                'text': f"<b>{self.cluster_mapping[str(self.cluster)]}</b>",  # Set the cluster name as bold
                                'x': 0.1,  # Set the x-position of the title in the middle
                                'y': 0.95,  # Set the y-position of the title near the top
                                'xanchor': 'center',  # Align the title to the center horizontally
                                'yanchor': 'top',  # Align the title to the top vertically
                                # 'font': dict(size=18)  # Adjust the font size of the title
                            }
                        )
        fig.update_yaxes(autorange='reversed', secondary_y=True)

        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON
