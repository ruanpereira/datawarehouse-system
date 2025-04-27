import kagglehub
import pandas as pd
import os


path = kagglehub.dataset_download("dienert/vendas")


csv_path = None
for root, _, files in os.walk(path):
    for file in files:
        if file.endswith('.csv'):
            csv_path = os.path.join(root, file)
            break


if csv_path:
    print(f"Arquivo CSV encontrado em: {csv_path}")
    

    dataset = pd.read_csv(csv_path)
    print("\nPrimeiras 5 linhas do dataset:")
    print(dataset.head(5))
    if 'dataset' in locals():
        for index, value in enumerate(dataset.columns):
            print(f"{index+1}. {value}")
    else:
        print("Dataset não foi carregado corretamente")
    print(f"{list(dataset.columns)}")

    with open('vendas_data.txt', 'w', encoding='utf-8') as f:
        f.write(dataset.to_string(index=False))
    print("\nArquivo 'vendas_data.txt' criado com sucesso.")
    
# 
    # try:
        # filtered_product = dataset[dataset['product'] == "Lang Club"]
        # with open('filtered_product.txt', 'w', encoding='utf-8') as f:
            # f.write(filtered_product.to_string(index=False))
        # print("\nArquivo 'filtered_product.txt' criado com sucesso.")
    # except KeyError:
        # print("\nErro: Coluna 'product' não encontrada. Verifique os nomes das colunas.")
    # 
# 
    # try:
        # filtered_email = dataset[dataset['email'] == 'jessica.cole@example.net']
        # with open('filtered_email.txt', 'w', encoding='utf-8') as f:
            # f.write(filtered_email.to_string(index=False))
        # print("\nArquivo 'filtered_email.txt' criado com sucesso.")
    # except KeyError:
        # print("\nErro: Coluna 'email' não encontrada. Verifique os nomes das colunas.")
    # 
    # try:
        # filtered_customer = dataset[dataset['customer_name'] == 'John Doe']
        # with open('filtered_customer.txt', 'w', encoding='utf-8') as f:
            # f.write(filtered_customer.to_string(index=False))
        # print("\nArquivo 'filtered_customer.txt' criado com sucesso.")
    # except KeyError:
        # print("\nErro: Coluna 'customer_name' não encontrada. Verifique os nomes das colunas.")
    # 
# 
    # try:
        # filtered_combined = dataset[(dataset['product'] == "Lang Club") & (dataset['email'] == 'jessica.cole@example.net')]
        # with open('filtered_combined.txt', 'w', encoding='utf-8') as f:
            # f.write(filtered_combined.to_string(index=False))
        # print("\nArquivo 'filtered_combined.txt' criado com sucesso.")
    # except KeyError:
        # print("\nErro: Alguma coluna não encontrada. Verifique os nomes das colunas.")
    #   
else:
    print("Nenhum arquivo CSV encontrado no diretório baixado.")