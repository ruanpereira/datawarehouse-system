import pandas as pd
from datetime import datetime
from typing import Union

def filter_status_atraso(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna apenas vendas com status 'Em atraso'."""
    print(df[df['STATUS COTA'] != 'A'])
    return df[df['STATUS COTA'] != 'A']

def filter_by_year(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """Retorna vendas ocorridas no ano especificado."""
    return df[df['DATA VENDA'].dt.year == year]

def total_liquido_por_vendedor(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa vendas por vendedor somando o valor líquido,
    renomeia a coluna de saída para 'Total Líquido' e
    ordena do maior para o menor valor.
    Exclui linhas onde 'VENDEDOR' não seja texto (evita valores numéricos ou linhas de totalização prévias).
    """
    # Cópia para não alterar df original
    df_copy = df.copy()

    # Verifica se as colunas existem
    for col in ('VENDEDOR', 'LÍQUIDO R$'):
        if col not in df_copy.columns:
            raise KeyError(f"Coluna '{col}' não encontrada no DataFrame.")

    # Filtra apenas vendedores "reais" (tipos string) e não-vazios
    mask_valid = df_copy['VENDEDOR'].apply(lambda x: isinstance(x, str) and x.strip() != "")
    df_copy = df_copy.loc[mask_valid]

    # Converte líquido para numérico, substitui não-numéricos por zero
    df_copy['LÍQUIDO R$'] = (
        pd.to_numeric(df_copy['LÍQUIDO R$'], errors='coerce')
          .fillna(0)
    )

    # Agrupa, soma, renomeia e ordena
    result = (
        df_copy
        .groupby('VENDEDOR', as_index=False)['LÍQUIDO R$']
        .sum()
        .rename(columns={'LÍQUIDO R$': 'Total Líquido'})
        .sort_values(by='Total Líquido', ascending=False)
    )
    print(result)

    return result


def total_liquido_por_consorcio_vendedor(df: pd.DataFrame) -> pd.DataFrame:
    """Agrupa consorciado e vendedor somando o valor líquido."""
    print(df.groupby(['NOME CONSORCIADO', 'VENDEDOR'])['LÍQUIDO R$'].sum().reset_index())
    return df.groupby(['NOME CONSORCIADO', 'VENDEDOR'])['LÍQUIDO R$'].sum().reset_index()

def relatorio_por_consorciado(df: pd.DataFrame) -> dict:
    """
    Gera um dicionário com os dados agrupados por consorciado, incluindo a data de venda.
    Retorna: {consorciado: {'data_venda': data, 'vendedores': DataFrame, 'total': float}}
    """
    grouped = df.groupby('NOME CONSORCIADO')
    result = {}
    for consorciado, group in grouped:
        data_venda = group['DATA VENDA'].iloc[0]
        vendedores = group.groupby('VENDEDOR')['LÍQUIDO R$'].sum().reset_index()
        vendedores['Total'] = vendedores['LÍQUIDO R$'] * 1.2  # adiciona 20%
        total_consorciado = vendedores['Total'].sum()
        result[consorciado] = {
            'data_venda': data_venda,
            'vendedores': vendedores,
            'total': total_consorciado
        }
        print(result)
    return result

# ————— Novas funções para cálculo de inadimplentes —————

def filter_em_atraso(
    df: pd.DataFrame,
    data_ref: Union[str, datetime] = "2025-03-17"
) -> pd.DataFrame:
    """
    Retorna apenas as parcelas que estão em atraso.
    Considera atraso toda parcela cujo 'DATA VENCIMENTO' <= data_ref
    e sem 'DATA PAGAMENTO'.
    """
    # converte colunas de data, se ainda não forem datetime
    df = df.copy()
    df['DATA VENCIMENTO'] = pd.to_datetime(df['DATA VENCIMENTO'], dayfirst=True)
    if 'DATA PAGAMENTO' in df.columns:
        df['DATA PAGAMENTO'] = pd.to_datetime(df['DATA PAGAMENTO'], dayfirst=True)
    data_ref = pd.to_datetime(data_ref, dayfirst=True)
    mask = (df['DATA VENCIMENTO'] <= data_ref) & df.get('DATA PAGAMENTO', pd.Series()).isna()
    return df[mask]

def clientes_inadimplentes(
    df: pd.DataFrame,
    data_ref: Union[str, datetime] = "2025-03-17"
) -> pd.DataFrame:
    """
    Retorna um DataFrame com os clientes (contrato + nome) que têm
    ao menos uma parcela em atraso, incluindo o valor de crédito/base.
    """
    atrasos = filter_em_atraso(df, data_ref)
    cols = ['CONTRATO', 'NOME CONSORCIADO', 'BASE R$']
    return atrasos.drop_duplicates(subset=['CONTRATO', 'NOME CONSORCIADO'])[cols]

def total_credito_em_atraso(
    df: pd.DataFrame,
    data_ref: Union[str, datetime] = "2025-03-17"
) -> float:
    """
    Calcula o somatório de crédito (BASE R$) dos clientes inadimplentes.
    """
    inadimplentes = clientes_inadimplentes(df, data_ref)
    return inadimplentes['BASE R$'].sum()

def count_inadimplentes(
    df: pd.DataFrame,
    data_ref: Union[str, datetime] = "2025-03-17"
) -> int:
    """
    Retorna o número de clientes que estão com parcela(s) em atraso.
    """
    inadimplentes = clientes_inadimplentes(df, data_ref)
    return len(inadimplentes)
