import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS vendas (
        id SERIAL PRIMARY KEY,
        contrato TEXT,
        nome_consorciado TEXT,
        vendedor TEXT,
        data_venda TIMESTAMP,
        base NUMERIC,
        liquido NUMERIC,
        status_cota TEXT
    );
""")

conn.commit()

cur.close()
conn.close()
