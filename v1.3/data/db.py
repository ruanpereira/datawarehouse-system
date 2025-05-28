# db.py
import os
import uuid
from datetime import datetime
import pandas as pd
import numpy as np
import re
from sqlalchemy import (create_engine, Column, Integer, String, DateTime,
                        Numeric, MetaData, Table)
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy import select

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False, future=True)
Session = sessionmaker(bind=engine)
metadata = MetaData()

vendas = Table(
    'vendas', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('batch_id', String, index=True),
    Column('data_upload', DateTime, default=datetime.utcnow),
    Column('origem_arquivo', String),
    Column('data_venda', DateTime),
    Column('data_alocacao', DateTime),
    Column('cod_comissionado', String),
    Column('bem', String),
    Column('cod_pv', String),
    Column('cod_equipe', String),
    Column('contrato', String),
    Column('consorciado', String),
    Column('nome_consorciado', String),
    Column('status_cota', String),
    Column('parc_lib', String),
    Column('regra', String),
    Column('categoria', String),
    Column('comissao_percentual', Numeric),
    Column('base_calc_comissao', Numeric),
    Column('comissao_reais', Numeric),
    Column('estorno_reais', Numeric),
    Column('cancelamento_cota_reais', Numeric),
    Column('base_reais', Numeric),
    Column('liquido_reais', Numeric),
    Column('vendedor', String),
)

uploads = Table(
    'uploads', metadata,
    Column('id', String, primary_key=True),
    Column('data_upload', DateTime, default=datetime.utcnow),
    Column('origem_arquivo', String),
    Column('num_registros', Integer),
)

def init_db():
    metadata.create_all(engine)

def insert_upload_and_vendas(df, origem_arquivo):
    """Insere um lote (upload) + linhas de vendas."""
    batch_id = str(uuid.uuid4())
    sess = Session()

    invalid_keywords = ["ENCERRAMENTO", "TOTAL", "DESCONTOS", "R\$"]
    keyword_pattern = '|'.join(invalid_keywords)
    regex_numeric = r'^\s*\d+[\d.,]*\s*$'

    df = df[df['vendedor'].apply(lambda x: isinstance(x, str) and x.strip() != "")]
    df = df[~df['vendedor'].str.upper().str.contains(keyword_pattern, regex=True)]
    df = df[~df['vendedor'].str.match(regex_numeric)]

    records = df.replace({pd.NaT: None})
    records = records.where(pd.notnull(records), None)

    sess.execute(uploads.insert().values(
        id=batch_id,
        origem_arquivo=os.path.basename(origem_arquivo),
        num_registros=len(df)
    ))

    records['batch_id'] = batch_id
    records['origem_arquivo'] = os.path.basename(origem_arquivo)

    data_to_insert = records.to_dict(orient='records')

    for item in data_to_insert:
        for key, value in item.items():
            if isinstance(value, (np.generic)):
                item[key] = value.item()

    sess.execute(vendas.insert(), data_to_insert)
    sess.commit()
    sess.close()
    return batch_id

def query_vendas_by_batch(batch_id):
    """Retorna DataFrame de todas as vendas desse lote."""
    import pandas as pd
    sess = Session()
    res = sess.execute(vendas.select().where(vendas.c.batch_id == batch_id)).mappings().all()
    sess.close()
    return pd.DataFrame(res)
def query_vendas_by_name(origem_arquivo):
    import pandas as pd
    session = Session()

    # Buscar o batch_id (id da tabela uploads) com base na origem_arquivo
    batch_id = session.execute(
        select(uploads.c.id).where(uploads.c.origem_arquivo == origem_arquivo)
    ).scalar_one_or_none()

    if not batch_id:
        session.close()
        return pd.DataFrame()  # Nenhum upload encontrado

    # Agora buscar todas as vendas com esse batch_id
    res = session.execute(
        select(vendas).where(vendas.c.batch_id == batch_id)
    ).mappings().all()

    session.close()
    return pd.DataFrame(res)
