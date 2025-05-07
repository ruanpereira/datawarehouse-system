import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('pt_BR')

num_registros = 100

status_cota = ['Ativa', 'Cancelada', 'Quitada', 'Em atraso']
categorias = ['Automóvel', 'Imóvel', 'Motocicleta', 'Caminhão']
regras = ['Normal', 'Promocional', 'Especial', 'Corretor']
consorciado = ["coca-cola", "Intel", "Lenovo", "Positivo"]

# Gerando os dados
dados = []
for _ in range(num_registros):
    data_venda = fake.date_between(start_date='-1y', end_date='today')
    contrato = fake.random_number(digits=8)
    parc_lib = f"{random.randint(1, 80)}/{random.randint(12, 120)}"
    comissao_percent = round(random.uniform(1.0, 10.0), 2)
    base_calc = round(random.uniform(5000, 50000), 2)
    comissao = round(base_calc * comissao_percent / 100, 2)
    estorno = round(comissao * random.uniform(0, 0.3), 2) if random.random() > 0.7 else 0
    cancelamento = round(comissao * random.uniform(0, 0.5), 2) if random.random() > 0.8 else 0
    base = base_calc - estorno - cancelamento
    liquido = comissao - estorno - cancelamento
    
    dados.append({
        'DATA VENDA': data_venda,
        'CÓD COMISSIONADO': fake.random_number(digits=6),
        'CÓD PV': fake.random_number(digits=5),
        'CONTRATO': contrato,
        'CONSORCIADO': random.choice(consorciado),
        'NOME CONSORCIADO': fake.name(),
        'STATUS COTA': random.choice(status_cota),
        'PARC/LIB': parc_lib,
        'REGRA': random.choice(regras),
        'CATEGORIA': random.choice(categorias),
        'COMISSAO %': comissao_percent,
        'BASE CÁLC COMISSAO': base_calc,
        'COMISSAO R$': comissao,
        'ESTORNO R$': estorno,
        'CANCELAMENTO COTA R$': cancelamento,
        'BASE R$': base,
        'LÍQUIDO R$': liquido,
        'VENDEDOR': fake.name()
    })

df = pd.DataFrame(dados)

colunas_ordenadas = [
    'DATA VENDA', 'CÓD COMISSIONADO', 'CÓD PV', 'CONTRATO', 'CONSORCIADO',
    'NOME CONSORCIADO', 'STATUS COTA', 'PARC/LIB', 'REGRA', 'CATEGORIA',
    'COMISSAO %', 'BASE CÁLC COMISSAO', 'COMISSAO R$', 'ESTORNO R$',
    'CANCELAMENTO COTA R$', 'BASE R$', 'LÍQUIDO R$', 'VENDEDOR'
]
df = df[colunas_ordenadas]

df.to_excel('dados_comissao_fake.xlsx', index=False)