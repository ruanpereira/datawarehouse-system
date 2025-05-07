import pandas as pd

def filter_status_atraso(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna apenas vendas com status 'Em atraso'."""
    return df[df['STATUS COTA'] == 'Em atraso']

def filter_high_commission(df: pd.DataFrame, threshold: float = 8.0) -> pd.DataFrame:
    """Retorna vendas com comissão acima de threshold."""
    return df[df['COMISSAO %'] > threshold]

def filter_by_year(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """Retorna vendas ocorridas no ano especificado."""
    return df[df['DATA VENDA'].dt.year == year]

def total_liquido_por_vendedor(df: pd.DataFrame) -> pd.DataFrame:
    """Agrupa vendas por vendedor somando o valor líquido."""
    return df.groupby('VENDEDOR')['LÍQUIDO R$'].sum().reset_index()

def total_liquido_por_consorcio_vendedor(df: pd.DataFrame) -> pd.DataFrame:
    """Agrupa consorcio e vendedor somando o valor liquido"""
    return df.groupby(['CONSORCIADO', 'VENDEDOR'])['LÍQUIDO R$'].sum().reset_index()