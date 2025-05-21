import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Connect to the database
try:
    connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )
    print("Connection successful!")
    cursor = connection.cursor()
    # Cria a tabela 'vendas' se ela não existir
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id SERIAL PRIMARY KEY,
            batch_id TEXT,
            data_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            origem_arquivo TEXT,
            data_venda TIMESTAMP,
            data_alocacao TIMESTAMP,
            cod_comissionado_1 TEXT,
            bem TEXT,
            cod_comissionado_2 TEXT,
            cod_pv TEXT,
            cod_equipe TEXT,
            contrato TEXT,
            consorciado TEXT,
            nome_consorciado TEXT,
            status_cota TEXT,
            parc_lib TEXT,
            regra TEXT,
            categoria TEXT,
            comissao_percentual NUMERIC,
            base_calc_comissao NUMERIC,
            comissao_reais NUMERIC,
            estorno_reais NUMERIC,
            cancelamento_cota_reais NUMERIC,
            base_reais NUMERIC,
            liquido_reais NUMERIC,
            vendedor TEXT
        );
    """)
    connection.commit()
    print("Tabela 'vendas' criada ou já existente.")

    # Fecha o cursor e a conexão
    cursor.close()
    connection.close()
    print("Conexão encerrada com sucesso.")

except Exception as e:
    print(f"Falha ao conectar ou executar comandos no banco de dados: {e}")
