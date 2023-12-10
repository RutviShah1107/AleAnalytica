import pandas as pd

class ReadData:
    def __init__(self, path: str):
        self.df = pd.DataFrame()
        self.path = path

    def read_dataframe(self):
        self.df = pd.read_csv(self.path)
        return self.df
