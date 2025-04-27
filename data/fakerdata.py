from faker import Faker
from datetime import datetime
import csv
import random

fake = Faker('pt_BR')
regioes = ['Sul', 'Norte', 'Leste', 'Oeste', 'Centro']
periodos = ['Manhã', 'Tarde', 'Noite']
vendedores = ["Ana Silva", "João Pereira", "Maria Oliveira", "Pedro Santos", "Clara Mendes"]
num_rows = 100

start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)

with open('sales_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Vendedor', 'Valor_Venda', 'Regiao', 'Data', 'Periodo'])
    for _ in range(num_rows):
        vendedor = random.choice(vendedores)
        valor_venda = f"{random.uniform(270000, 600000):.2f}"
        regiao = random.choice(regioes)
        data = fake.date_between(start_date=start_date, end_date=end_date).strftime('%d/%m/%Y')
        periodo = random.choice(periodos)
        writer.writerow([vendedor, valor_venda, regiao, data, periodo])