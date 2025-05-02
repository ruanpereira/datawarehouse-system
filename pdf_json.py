import pandas as pd
import os
from PyPDF2 import PdfReader
# Para Excel, instale openpyxl: pip install openpyxl
# Para PDF, instale PyPDF2: pip install pypdf

class FileBase():
    SUPPORTED_EXTENSIONS = ['.csv', '.xlsx', '.xls', '.pdf']  # Extensões suportadas
    
    def __init__(self):
        self.path = "data/"
        self.file_path = None
        self.file_type = None
        self.push_path()
    
    def push_path(self):
        for root, _, files in os.walk(self.path):
            for file in files:
                for ext in self.SUPPORTED_EXTENSIONS:
                    if file.lower().endswith(ext):
                        self.file_path = os.path.join(root, file)
                        self.file_type = ext
                        break  # Encerra o loop de extensões
                if self.file_path is not None:
                    break  # Encerra o loop de arquivos
            if self.file_path is not None:
                break  # Encerra o loop de diretórios
    
    def get_path(self):
        return self.path
    
    def get_file_path(self):
        return self.file_path
    
    def get_file_type(self):
        return self.file_type

class DataFileManagement(FileBase):
    def __init__(self):
        super().__init__()
        self.dataset = None
        self.columns = None
        self.create_dataset()
        self.set_columns_to_list()
    
    def create_dataset(self):
        file_path = self.get_file_path()
        file_type = self.get_file_type()
        
        if file_type == '.csv':
            self.dataset = pd.read_csv(file_path)
        elif file_type in ('.xlsx', '.xls'):
            self.dataset = pd.read_excel(file_path)
        elif file_type == '.pdf':
            # Extrai texto do PDF (para tabelas, considere usar tabula-py)
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            self.dataset = pd.DataFrame({'Texto': [text]})
        else:
            raise ValueError(f"Formato de arquivo não suportado: {file_type}")
        
        self.columns = self.dataset.columns
    
    def create_vendas_txt(self):
        name_file = input("Informe o nome do arquivo: ")
        with open(f"{name_file}.txt", 'w', encoding='utf-8') as f:
            f.write(self.dataset.to_string(index=False))
        print(f"Arquivo {name_file}.txt criado!")
    
    def set_columns_to_list(self):
        self.columns_list = list(self.columns)
    
    def get_columns(self):
        return self.columns_list if self.columns_list is not None else "Use set_columns_to_list() primeiro!"