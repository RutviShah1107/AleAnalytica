import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import json
import plotly
from .modified_dendogram import create_dendrogram

class Clustering:
    def __init__(self, df_analysis: pd.DataFrame(), df: pd.DataFrame(), p: int = 8):
        self.df = df
        self.df_analysis = df_analysis
        # self.scaler = StandardScaler()
        self.p = p

        self.create_clusters()

    ## Not use since added this option in the dendogram function in modified_dendogram.py
    def create_links(self):
        return linkage(self.df_analysis, method='ward')  

    def create_clusters(self):
        linked = self.create_links()
        threshold = 140 
        clusters = fcluster(linked, threshold, criterion='distance')
        self.df['Cluster'] = clusters

    def generate_graph(self):
        fig = create_dendrogram(self.df_analysis, p=self.p, truncate_mode='lastp', distance_sort='descending')
        fig.update_xaxes(title_text="Number of Survey Respondents in Cluster")
        # fig.update_layout(
        #     width=1000,  # Set the width of the graph
        #     height=600,  # Set the height of the graph
        # )
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON

