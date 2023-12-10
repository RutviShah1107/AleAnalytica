import pandas as pd
from .split_text import SplitText
from .read_data import ReadData
import plotly.express as px
import json
import plotly

class HeatmapColumns:
    def __init__(self, df: pd.DataFrame(), question: str):
        self.df = df
        self.df_subset = df
        self.question = question
        self.mapping = {}
        self.mapping_dict = {}
        self.mapping_df = pd.DataFrame()
        self.grouped_dataframe = pd.DataFrame()

        self.create_mapping_dict()

    def mode(self, x):
        mode_value = x.mode().iloc[0]
        mode_frequency = x.value_counts().max()
        return pd.Series(mode_value) 
        
    def read_mapping_file(self):
        rd = ReadData('./data/mapping_file.csv')
        return rd.read_dataframe()

    def create_mapping_dict(self):
        self.mapping_df = self.read_mapping_file()
        self.mapping_dict = {row['Columns']: row['Options'] for _, row in self.mapping_df.iterrows() if str(row['Columns']).startswith(self.question + '_')}
        if self.mapping_dict == {}:
            self.mapping_dict = {row['Columns']: row['Options'] for _, row in self.mapping_df.iterrows() if str(row['Columns']).startswith(self.question)}

        st = SplitText()
        self.mapping_dict = st.split_dict_text(self.mapping_dict)


    def subset_dataframe(self):
        columns = self.df.columns[self.df.columns.str.startswith(self.question + '_')].to_list()
        if columns == []:
            columns = self.df.columns[self.df.columns.str.startswith(self.question)].to_list()
        columns.append('Cluster')
        self.df_subset = self.df[columns]
        # self.grouped_dataframe = self.df_subset.groupby('Cluster').apply(lambda group: group.apply(self.mode))
        self.grouped_dataframe = self.df_subset.groupby('Cluster').mean()
        self.grouped_dataframe.rename(columns=self.mapping_dict, inplace=True)

    def generate_graph(self):
        self.subset_dataframe()
        self.grouped_dataframe = self.grouped_dataframe.transpose()
        fig = px.imshow(self.grouped_dataframe,
                    labels=dict(x="Cluster", y="Column", color="Frequency"),
                    x=self.grouped_dataframe.columns,
                    y=self.grouped_dataframe.index,
                    color_continuous_scale="YlOrRd",
                    aspect='auto'
                )
        fig.update_layout(
            width=1000,  # Adjust this width as needed
            height=1000,  # Adjust this height as needed
            xaxis=dict(tickangle=90)  # Rotate x-axis labels by 90 degrees

        )
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON

