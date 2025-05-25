import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('pt_BR')

num_registros = 1000

status_cota = ['A', 'M',]
categorias = ['000085', '000123', '000456', '000789']
regras = ['006040', '000085', '005000', '001234']
consorciado = ["coca-cola", "Intel", "Lenovo", "Positivo", "Agosto LTDA", "Ruan INC."]
vendedores = [fake.name() for _ in range(5)]

def gerar_codigo():
    return f"{random.randint(0,9999):04d}-{random.randint(0,9999):04d}-00"

dados = []
for _ in range(num_registros):
    data_venda = fake.date_between(start_date='-1y', end_date='today')
    contrato = f"{random.randint(0, 9999999):07d}"
    parc_lib = f"{random.randint(1, 80)} / {random.randint(12, 120)}"
    
    comissao_percent = 0.40
    base_calc = round(random.uniform(5000, 50000), 2)
    comissao = round(base_calc * comissao_percent, 2)
    estorno = round(comissao * random.uniform(0, 0.3), 2) if random.random() > 0.7 else 0
    cancelamento = round(comissao * random.uniform(0, 0.5), 2) if random.random() > 0.8 else 0
    base = base_calc - estorno - cancelamento
    liquido = comissao - estorno - cancelamento
    
    dados.append({
        'DATA VENDA': data_venda,
        'DATA ALOCAÇÃO': data_venda + timedelta(days=random.randint(1, 15)),
        'BEM': gerar_codigo(),
        'CÓD COMISSIONADO': random.randint(100000, 999999),
        'CÓD PV': random.randint(10000, 99999),
        'CÓD EQUIPE': random.randint(1000, 9999),
        'CONTRATO': contrato,
        'CONSORCIADO': gerar_codigo(),
        'NOME CONSORCIADO': random.choice(consorciado),
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
        'LÍQUIDO R$': liquido,  # Mantemos como float
        'VENDEDOR': random.choice(vendedores)
    })

    df = pd.DataFrame(dados)
    
    # Aplicamos a formatação apenas na exportação
    def formatar_excel(workbook):
        num_fmt = workbook.add_format({'num_format': '#,##0.00'})
        perc_fmt = workbook.add_format({'num_format': '0.00%'})
        money_fmt = workbook.add_format({'num_format': 'R$ #,##0.00'})
        
        return {
            'BASE CÁLC COMISSAO': money_fmt,
            'COMISSAO R$': money_fmt,
            'ESTORNO R$': money_fmt,
            'CANCELAMENTO COTA R$': money_fmt,
            'BASE R$': money_fmt,
            'LÍQUIDO R$': money_fmt,
            'COMISSAO %': perc_fmt
        }
    
with pd.ExcelWriter('dados_comissao_fake.xlsx', engine='xlsxwriter') as writer:
    df.to_excel(writer, index=False)
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    
    formatos = formatar_excel(workbook)
    
    for col, fmt in formatos.items():
        col_idx = df.columns.get_loc(col)
        worksheet.set_column(col_idx, col_idx, None, fmt)