import os
import pandas as pd
import re
from PyPDF2 import PdfReader

class DataLoader_local:
    """Responsável por carregar diferentes formatos de dados em DataFrame."""
    SUPPORTED_EXTENSIONS = {'.csv', '.xls', '.xlsx', '.pdf'}

    @staticmethod
    def load_local(file_path: str) -> pd.DataFrame:
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in DataLoader_local.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Formato não suportado: {ext}")

        if ext == '.csv':
            df = pd.read_csv(file_path, parse_dates=['DATA VENDA'])
        elif ext in ('.xls', '.xlsx'):
            df = pd.read_excel(file_path, parse_dates=['DATA VENDA'])
        else:
            reader = PdfReader(file_path)
            text = "\n".join(page.extract_text() or '' for page in reader.pages)
            df = pd.DataFrame({'Texto': [text]})
            return df

        # Aplicar filtros em colunas se "VENDEDOR" estiver presente
        if 'VENDEDOR' in df.columns:
            df = df[df['VENDEDOR'].apply(lambda x: isinstance(x, str) and x.strip() != "")]
            invalid_keywords = ["ENCERRAMENTO", "TOTAL", "DESCONTOS", "R\$"]
            keyword_pattern = '|'.join(invalid_keywords)
            regex_numeric = r'^\s*\d+[\d.,]*\s*$'
            df = df[~df['VENDEDOR'].str.upper().str.contains(keyword_pattern, regex=True)]
            df = df[~df['VENDEDOR'].str.match(regex_numeric)]

        return df
