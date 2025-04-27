import pdfplumber
import re
from pprint import pprint

def extract_pdf_data(pdf_path):
    data = {
        "codigo_pn": None,
        "nome_pn": None,
        "cnpj": None,
        "simples_nacional": None,
        "dados_bancarios": {},
        "transacoes": [],
        "totais": {}
    }

    with pdfplumber.open(pdf_path) as pdf:
        text = pdf.pages[0].extract_text()
        
        # Extrair campos básicos
        data["codigo_pn"] = re.search(r"REP\d+", text).group()
        data["nome_pn"] = re.search(r"Nome do PN:\s+(.+)", text).group(1)
        data["cnpj"] = re.search(r"CNPJ:\s+([\d./-]+)", text).group(1)
        data["simples_nacional"] = re.search(r"SIMPLES Nacional:\s+(\w+)", text).group(1)
        
        # Dados bancários corrigidos
        banco_match = re.search(
            r"Dados bancários:\s+(.+?)\n(.+?)\n", 
            text, 
            re.DOTALL
        )
        if banco_match:
            banco_nome = banco_match.group(1).strip()
            conta_info = banco_match.group(2).replace(' ', '').split('/')
            
            data["dados_bancarios"] = {
                "banco": banco_nome,
                "agencia": conta_info[0].strip(),
                "conta": conta_info[1].strip() if len(conta_info) > 1 else None
            }

        # Extrair totais 
        def extract_total(pattern):
            match = re.search(pattern, text, re.DOTALL)
            if match:
                return float(match.group(1).replace('.', '').replace(',', '.'))
            return 0.0

        data["totais"] = {
            "credito": extract_total(r"CRÉDITO:\s+R\$\s+([\d.,]+)"),
            "debito": extract_total(r"DÉBITO:\s+R\$\s+([\d.,]+)"),
            "total_bruto": extract_total(r"TOTAL BRUTO:\s+R\$\s+([\d.,]+)"),
            "irrf": extract_total(r"IRRF:\s+R\$\s+([\d.,]+)"),
            "total_liquido": extract_total(r"TOTAL LÍQUIDO:\s+R\$\s+([\d.,]+)")
        }

    return data

# Uso
dados = extract_pdf_data("Comissao_48181-MAC RON ALVES COELHO PIRES - 22.04.2025.pdf")
pprint(dados)