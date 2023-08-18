import pandas as pd
import os

class Data():
    def __init__(self):
        self.local_path = '../data_files/english-premier-league/data/'

    def dataReader(self):
        folder_path = self.local_path
        csv_files = [file_name for file_name in os.listdir(folder_path) if file_name.endswith('.csv')]
        selected_col = ['HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTHG','HTAG','HS','AS','HST','AST','HY','AY','HR','AR']

        csv_data = []
        for csv_file in csv_files:
            file_path = os.path.join(folder_path, csv_file)
            file_data = pd.read_csv(file_path, usecols=selected_col)
            csv_data.append(file_data)

        matches_data = pd.concat(csv_data).reset_index()
        return matches_data
