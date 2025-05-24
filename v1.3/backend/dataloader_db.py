import os
import pandas as pd
from PyPDF2 import PdfReader
from datetime import datetime

class DataLoader_db:
    """Responsável por carregar e tratar diferentes formatos de dados em DataFrame."""
    SUPPORTED_EXTENSIONS = {'.csv', '.xls', '.xlsx', '.pdf'}
    
    COLUMN_MAPPING = {
        'DATA VENDA': 'data_venda',
        'DATA ALOCAÇÃO': 'data_alocacao',
        'CÓD COMISSIONADO': 'cod_comissionado',
        'BEM': 'bem',
        'CÓD PV': 'cod_pv',
        'CÓD EQUIPE': 'cod_equipe',
        'CONTRATO': 'contrato',
        'CONSORCIADO': 'consorciado',
        'NOME CONSORCIADO': 'nome_consorciado',
        'STATUS COTA': 'status_cota',
        'PARC/LIB': 'parc_lib',
        'REGRA': 'regra',
        'CATEGORIA': 'categoria',
        'COMISSAO %': 'comissao_percentual',
        'BASE CÁLC COMISSAO': 'base_calc_comissao',
        'COMISSAO R$': 'comissao_reais',
        'ESTORNO R$': 'estorno_reais',
        'CANCELAMENTO COTA R$': 'cancelamento_cota_reais',
        'BASE R$': 'base_reais',
        'LÍQUIDO R$': 'liquido_reais',
        'VENDEDOR': 'vendedor'
    }

    @staticmethod
    def load_db(file_path: str) -> pd.DataFrame:
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in DataLoader_db.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Formato não suportado: {ext}")

        # Carregar dados brutos
        if ext == '.csv':
            df = pd.read_csv(file_path, delimiter=';', decimal=',', dayfirst=True)
        elif ext in ('.xls', '.xlsx'):
            df = pd.read_excel(file_path, engine='openpyxl')
        else:
            df = DataLoader_db._handle_pdf(file_path)

        # Pré-processamento
        df = DataLoader_db._preprocess_data(df)
        return df

    @staticmethod
    def _preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
        # Renomear colunas
        df = df.rename(columns=DataLoader_db.COLUMN_MAPPING)
        
        # Converter datas
        date_columns = ['data_venda', 'data_alocacao']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(
                    df[col], 
                    dayfirst=True, 
                    errors='coerce'
                ).dt.tz_localize(None)  # Remove timezone
                df[col] = df[col].where(df[col].notna(), None)

        # Converter valores numéricos
        numeric_cols = [
            'comissao_percentual', 'base_calc_comissao', 'comissao_reais',
            'estorno_reais', 'cancelamento_cota_reais', 'base_reais', 'liquido_reais'
        ]
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.replace(r'[^\d,]', '', regex=True)
                    .str.replace(',', '.')
                    .replace('', None)
                    .astype(float)
                )
        
        # Tratar valores nulos
        df = df.replace({
            'NULL': None,
            'null': None,
            '': None,
            'nan': None,
            'NaN': None,
            pd.NaT: None
        })
        
        return df

    @staticmethod
    def _handle_pdf(file_path: str) -> pd.DataFrame:
        reader = PdfReader(file_path)
        text = "\n".join(page.extract_text() or '' for page in reader.pages)
        return pd.DataFrame({'Texto': [text]})