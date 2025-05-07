import os
import pandas as pd
from PyPDF2 import PdfReader

class DataLoader:
    """Responsável por carregar diferentes formatos de dados em DataFrame."""
    SUPPORTED_EXTENSIONS = {'.csv', '.xls', '.xlsx', '.pdf'}

    @staticmethod
    def load(file_path: str) -> pd.DataFrame:
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in DataLoader.SUPPORTED_EXTENSIONS:
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
