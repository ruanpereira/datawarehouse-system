# import kagglehub
import pandas as pd
import os

class FileBase():
    def __init__(self):
        self.path = "data/"
        self.csv_path = None
        self.push_path()
    def push_path(self):
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith('.csv'):
                    self.csv_path = os.path.join(root, file)
                    break 

    def get_path(self):
        return self.path
    
    def get_csv_path(self):
        return self.csv_path

class DataFileManagement(FileBase):
    def __init__(self):
        super().__init__()
        self.dataset = None
        self.columns = None
        self.create_dataset()
        self.set_columns_to_list()
    
    
    def create_dataset(self):
        self.dataset = pd.read_csv(self.csv_path)
        self.columns = self.dataset.columns

    def create_vendas_txt(self):
        name_file = input("informe o nome do arquivo: ")
        with open(f"{name_file}.txt", 'w', encoding='utf-8') as f:
            f.write(self.dataset.to_string(index=False))
        print(f"Arquivo {name_file} criado!")
    
    def set_columns_to_list(self):
        self.columns_list = list(self.columns)
    
    def get_columns(self):
        if self.columns_list is not None:
            return self.columns_list
        else:
            return "Use o metodo set_columns antes!"
        
