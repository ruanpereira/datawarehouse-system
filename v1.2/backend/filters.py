import pandas as pd
from datetime import datetime
from typing import Union
from sqlalchemy import select, func, extract, and_
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.db import Session, vendas


def filter_status_atraso() -> pd.DataFrame:
    """Retorna apenas vendas com status 'Em atraso'."""
    print("DEBUG: Calling filter_status_atraso()")
    with Session() as session:
        stmt = select(vendas).where(vendas.c.status_cota != 'A')
        print(f"DEBUG: Executing SQL: {stmt}")
        records = session.execute(stmt).mappings().all()
        print(f"DEBUG: Retrieved {len(records)} rows")
    return pd.DataFrame(records)


def filter_by_year(year: int) -> pd.DataFrame:
    """Retorna vendas ocorridas no ano especificado."""
    print(f"DEBUG: Calling filter_by_year(year={year})")
    with Session() as session:
        stmt = select(vendas).where(extract('year', vendas.c.data_venda) == year)
        print(f"DEBUG: Executing SQL: {stmt}")
        records = session.execute(stmt).mappings().all()
        print(f"DEBUG: Retrieved {len(records)} rows")
    return pd.DataFrame(records)


def total_liquido_por_vendedor() -> pd.DataFrame:
    """
    Agrupa vendas por vendedor somando o valor líquido,
    renomeia a coluna para 'Total Líquido' e ordena do maior para o menor valor.
    """
    print("DEBUG: Calling total_liquido_por_vendedor()")
    with Session() as session:
        stmt = (
            select(
                vendas.c.vendedor,
                func.sum(vendas.c.liquido_reais).label('total_liquido')
            )
            .where(vendas.c.vendedor != None)
            .group_by(vendas.c.vendedor)
            .order_by(func.sum(vendas.c.liquido_reais).desc())
        )
        print(f"DEBUG: Executing SQL: {stmt}")
        rows = session.execute(stmt).all()
        print(f"DEBUG: Retrieved {len(rows)} rows")
    df = pd.DataFrame(rows, columns=['VENDEDOR', 'Total Líquido'])
    return df


def total_liquido_por_consorcio_vendedor() -> pd.DataFrame:
    """Agrupa consorciado e vendedor somando o valor líquido."""
    print("DEBUG: Calling total_liquido_por_consorcio_vendedor()")
    with Session() as session:
        stmt = (
            select(
                vendas.c.nome_consorciado,
                vendas.c.vendedor,
                func.sum(vendas.c.liquido_reais).label('total_liquido')
            )
            .group_by(vendas.c.nome_consorciado, vendas.c.vendedor)
        )
        print(f"DEBUG: Executing SQL: {stmt}")
        rows = session.execute(stmt).all()
        print(f"DEBUG: Retrieved {len(rows)} rows")
    df = pd.DataFrame(rows, columns=['NOME CONSORCIADO', 'VENDEDOR', 'Total Líquido'])
    return df


def relatorio_por_consorciado() -> dict:
    """
    Gera relatório por consorciado com data da primeira venda,
    vendedores (soma líquida *1.2) e total geral.
    """
    print("DEBUG: Calling relatorio_por_consorciado()")
    report = {}
    with Session() as session:
        consorciados = session.execute(
            select(vendas.c.nome_consorciado).distinct()
        ).scalars().all()
        print(f"DEBUG: Found {len(consorciados)} consorciados")
        for nome in consorciados:
            print(f"DEBUG: Processing consorciado={nome}")
            rows = session.execute(
                select(
                    vendas.c.data_venda,
                    vendas.c.vendedor,
                    vendas.c.liquido_reais
                ).where(vendas.c.nome_consorciado == nome)
            ).all()
            if not rows:
                print(f"DEBUG: No vendas for {nome}")
                continue
            data_venda = rows[0].data_venda
            agg = {}
            for r in rows:
                agg[r.vendedor] = agg.get(r.vendedor, 0) + r.liquido_reais
            vendedores = {v: total * 1.2 for v, total in agg.items()}
            total_geral = sum(vendedores.values())
            report[nome] = {
                'data_venda': data_venda,
                'vendedores': vendedores,
                'total': total_geral
            }
            print(f"DEBUG: Report for {nome} -> total={total_geral}")
    return report


def filter_em_atraso(
    data_ref: Union[str, datetime] = "2025-03-17"
) -> pd.DataFrame:
    """
    Retorna parcelas em atraso: data_vencimento <= data_ref e sem data_pagamento.
    """
    print(f"DEBUG: Calling filter_em_atraso(data_ref={data_ref})")
    data_ref_dt = pd.to_datetime(data_ref, dayfirst=True)
    with Session() as session:
        stmt = (
            select(vendas)
            .where(
                and_(
                    vendas.c.data_vencimento <= data_ref_dt,
                    vendas.c.data_pagamento == None
                )
            )
        )
        print(f"DEBUG: Executing SQL: {stmt}")
        rows = session.execute(stmt).mappings().all()
        print(f"DEBUG: Retrieved {len(rows)} rows")
    return pd.DataFrame(rows)


def clientes_inadimplentes(
    data_ref: Union[str, datetime] = "2025-03-17"
) -> pd.DataFrame:
    """Retorna contratos e nome dos inadimplentes e base de crédito."""
    print(f"DEBUG: Calling clientes_inadimplentes(data_ref={data_ref})")
    atrasos_df = filter_em_atraso(data_ref)
    if atrasos_df.empty:
        print("DEBUG: Nenhum atraso encontrado")
        return pd.DataFrame(columns=['CONTRATO', 'NOME CONSORCIADO', 'BASE R$'])
    result = (
        atrasos_df
        .drop_duplicates(subset=['contrato', 'nome_consorciado'])
        [['contrato', 'nome_consorciado', 'base_reais']]
        .rename(columns={
            'contrato': 'CONTRATO',
            'nome_consorciado': 'NOME CONSORCIADO',
            'base_reais': 'BASE R$'
        })
    )
    print(f"DEBUG: Found {len(result)} inadimplentes")
    return result


def total_credito_em_atraso(
    data_ref: Union[str, datetime] = "2025-03-17"
) -> float:
    """Calcula somatório de BASE R$ dos inadimplentes."""
    print(f"DEBUG: Calling total_credito_em_atraso(data_ref={data_ref})")
    df = clientes_inadimplentes(data_ref)
    total = df['BASE R$'].sum() if not df.empty else 0.0
    print(f"DEBUG: Total crédito em atraso = {total}")
    return total


def count_inadimplentes(
    data_ref: Union[str, datetime] = "2025-03-17"
) -> int:
    """Retorna quantidade de clientes inadimplentes."""
    print(f"DEBUG: Calling count_inadimplentes(data_ref={data_ref})")
    df = clientes_inadimplentes(data_ref)
    count = len(df)
    print(f"DEBUG: Count inadimplentes = {count}")
    return count


if __name__ == "__main__":
    print("=== Teste Rápido de Consultas ===")
    df_atraso = filter_status_atraso()
    print(f"Vendas em atraso: {len(df_atraso)} linhas")
    df_2025 = filter_by_year(2025)
    print(f"Vendas em 2025: {len(df_2025)} linhas")
    df_vendedor = total_liquido_por_vendedor()
    print("Total líquido por vendedor:")
    print(df_vendedor)
    print(df_2025)
    #df_inad = clientes_inadimplentes("2025-03-17")
    #print(f"Clientes inadimplentes: {len(df_inad)}")
    #print(df_inad)
    #total_credito = total_credito_em_atraso("2025-03-17")
    #print(f"Total de crédito em atraso: {total_credito}")