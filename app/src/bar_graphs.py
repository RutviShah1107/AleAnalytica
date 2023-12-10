import pandas as pd
import numpy as np
import json
import plotly
import plotly.express as px
from .read_data import ReadData
from .split_text import SplitText

class BarGraphs:
    def __init__(self, df: pd.DataFrame(), column: str):
        self.df = df
        self.mapping = {}
        self.column = column
        self.mapping_dict = {}
        self.mapping_df = pd.DataFrame()
        self.grouped_dataframe = pd.DataFrame()

        self.read_mapping()
        self.create_mapping_dict()
        
    def read_mapping_file(self):
        rd = ReadData('./data/mapping_file.csv')
        return rd.read_dataframe()

    def create_mapping_dict(self):
        self.mapping_df = self.read_mapping_file()
        self.mapping_dict = {row['Options']: [row['Columns'], row['Question']] for _, row in self.mapping_df.iterrows()}

    def read_mapping(self):
        with open('./data/demographics.json', 'r') as json_file:
            self.mapping = json.load(json_file)

    def group_and_map(self):
        column_code = self.mapping_dict[self.column][0]
        column_mapping = self.mapping[self.column]
        column_mapping = {int(key): value for key, value in column_mapping.items()}
        st = SplitText()
        column_mapping = st.split_dict_text(column_mapping)


        if self.column == 'Age':
            bins = [21, 28, 35, 50, 75] 
            labels = column_mapping.values()
            self.df[self.column + '_coded'] = pd.cut(self.df[column_code], bins=bins, labels=labels, include_lowest=True)

        else:
            self.df[self.column + '_coded'] = self.df[column_code].map(column_mapping)
        self.grouped_dataframe = self.df.groupby(['Cluster', self.column + '_coded']).size().unstack(fill_value=0)

    def generate_color_scale(self):
        color_indices = [i * (len(px.colors.sequential.YlOrRd) - 1) // (len(self.grouped_dataframe.columns) - 1) for i in range(len(self.grouped_dataframe.columns))]
        return [px.colors.sequential.YlOrRd[i] for i in color_indices]

    def generate_graph(self):
        self.group_and_map()
        fig = px.bar(
            self.grouped_dataframe,
            x=self.grouped_dataframe.index,
            y=self.grouped_dataframe.columns,
            barmode='group',
            title = self.column + ' Distribution by Cluster',
            color_discrete_sequence=self.generate_color_scale()
            )
        self.df.drop(self.column + '_coded', axis=1, inplace=True)

        fig.update_layout(
            width=1000,  # Adjust this width as needed
            height=800,  # Adjust this height as needed
            xaxis=dict(tickangle=90)  # Rotate x-axis labels by 90 degrees

        )

        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON


