import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from file_main import DataFileManagement
from docx import Document
from docx.shared import Pt

# Classes originais adaptadas (importadas)

class RelatorioVendas:
    def __init__(self, dados):
        self.doc = Document()
        self.dados = dados
        self._configurar_estilos()

    def _configurar_estilos(self):
        style = self.doc.styles['Normal']
        font = style.font  # type: ignore
        font.name = 'Arial'
        font.size = Pt(11)

    def add_title(self, text):
        p = self.doc.add_heading(level=1)
        run = p.add_run(text)
        run.bold = True

    def add_subtitle(self, text):
        p = self.doc.add_heading(level=2)
        run = p.add_run(text)
        run.bold = True

    def criar_relatorio(self):
        self.add_title("Relatório de Vendas")
        self.doc.add_paragraph(f"Vendedor: {self.dados['nome_vendedor']}")
        self.add_subtitle("Resumo Geral")
        self.doc.add_paragraph(f"Média total de vendas: {self.dados['media_total']}")
        self._criar_tabela("Média por Região", 'media_regiao')
        self._criar_tabela("Média por Período", 'media_periodo')
        if self.dados.get('media_data'):
            self._criar_tabela("Média por Data", 'media_data')
        if self.dados.get('media_geral'):
            self.add_subtitle("Média Geral de Todos os Vendedores")
            self.doc.add_paragraph(f"Média geral: {self.dados['media_geral']}")
        self.add_subtitle("Observações Finais")
        self.doc.add_paragraph("[Análises adicionais e comentários]")
        self.doc.save('relatorio_vendas_completo.docx')

    def _criar_tabela(self, titulo, chave):
        self.add_subtitle(titulo)
        table = self.doc.add_table(rows=1, cols=2)
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Categoria'
        hdr_cells[1].text = 'Valor Médio'
        for chave_item, valor in self.dados[chave].items():
            row_cells = table.add_row().cells
            row_cells[0].text = chave_item
            row_cells[1].text = valor

class SearchingFile(DataFileManagement):
    def __init__(self):
        super().__init__()
        self.relatorio_data = {}
    
    def load_dataset(self, file_path):
        self.dataset = pd.read_csv(file_path)
        self.columns_list = self.dataset.columns.tolist()

    def preparar_relatorio(self, coluna, valor, media_data, media_geral):
        self.column_name = coluna
        self.selected_value = valor
        self.filtered_rows = self.dataset[self.dataset[self.column_name] == self.selected_value]
        self.relatorio_data['nome_vendedor'] = self.selected_value
        self.relatorio_data['media_total'] = f"R$ {self.filtered_rows['Valor_Venda'].mean():.2f}"
        self.relatorio_data['media_regiao'] = self._formatar_medias('Regiao')
        self.relatorio_data['media_periodo'] = self._formatar_medias('Periodo')
        if media_data:
            self.relatorio_data['media_data'] = self._formatar_medias('Data')
        if media_geral:
            media_geral_calc = self.dataset['Valor_Venda'].mean()
            self.relatorio_data['media_geral'] = f"R$ {media_geral_calc:.2f}"
        relatorio = RelatorioVendas(self.relatorio_data)
        relatorio.criar_relatorio()

    def _formatar_medias(self, coluna):
        return self.filtered_rows.groupby(coluna)['Valor_Venda'].mean().apply(lambda x: f"R$ {x:.2f}").to_dict()

# Interface Gráfica

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerador de Relatório de Vendas")
        self.geometry("500x400")

        self.searching = SearchingFile()

        self.label_arquivo = ttk.Label(self, text="Arquivo de dados:")
        self.label_arquivo.pack(pady=5)
        self.botao_arquivo = ttk.Button(self, text="Selecionar Arquivo", command=self.carregar_arquivo)
        self.botao_arquivo.pack(pady=5)

        self.label_coluna = ttk.Label(self, text="Coluna para filtrar:")
        self.label_coluna.pack(pady=5)
        self.combo_colunas = ttk.Combobox(self, state="readonly")
        self.combo_colunas.pack(pady=5)
        self.combo_colunas.bind("<<ComboboxSelected>>", self.carregar_valores)

        self.label_valor = ttk.Label(self, text="Valor para filtrar:")
        self.label_valor.pack(pady=5)
        self.combo_valores = ttk.Combobox(self, state="readonly")
        self.combo_valores.pack(pady=5)

        self.chk_media_data = tk.BooleanVar()
        self.chk_media_geral = tk.BooleanVar()
        self.check_data = ttk.Checkbutton(self, text="Média por Data", variable=self.chk_media_data)
        self.check_data.pack(pady=5)
        self.check_geral = ttk.Checkbutton(self, text="Média Geral", variable=self.chk_media_geral)
        self.check_geral.pack(pady=5)

        self.botao_gerar = ttk.Button(self, text="Gerar Relatório", command=self.gerar_relatorio)
        self.botao_gerar.pack(pady=20)

    def carregar_arquivo(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.searching.load_dataset(file_path)
            self.combo_colunas['values'] = self.searching.columns_list

    def carregar_valores(self, event):
        coluna = self.combo_colunas.get()
        if coluna:
            self.combo_valores['values'] = sorted(self.searching.dataset[coluna].dropna().unique().tolist())

    def gerar_relatorio(self):
        coluna = self.combo_colunas.get()
        valor = self.combo_valores.get()
        if not (coluna and valor):
            messagebox.showerror("Erro", "Selecione a coluna e o valor.")
            return
        self.searching.preparar_relatorio(coluna, valor, self.chk_media_data.get(), self.chk_media_geral.get())
        messagebox.showinfo("Sucesso", "Relatório gerado com sucesso!")

if __name__ == "__main__":
    app = App()
    app.mainloop()