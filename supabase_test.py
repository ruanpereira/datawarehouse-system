import psycopg2
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente
load_dotenv()

# Obtém a URL do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL")

# Conecta ao banco de dados
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Cria a tabela
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

# Confirma a transação
conn.commit()

# Fecha a conexão
cur.close()
conn.close()
