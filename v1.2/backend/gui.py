import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from dataloader import DataLoader
from filters import filter_status_atraso, filter_high_commission, filter_by_year, total_liquido_por_vendedor
from report_generator import ReportGenerator
import pandas as pd
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerador de Relatório de Vendas")
        self.geometry("1000x700")
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.configure_style()
        self.report_gen = ReportGenerator()
        self.df = pd.DataFrame()
        self.numeric_columns = []
        self.filter_buttons = []
        self._build_ui()

    def configure_style(self):
        self.style.configure('TButton', padding=6, font=('Arial', 10))
        self.style.configure('TLabel', font=('Arial', 10, 'bold'))
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        self.style.configure('TCombobox', padding=5)
        self.style.configure('TCheckbutton', font=('Arial', 10))
        self.style.configure('TEntry', padding=5)
        self.style.map('TButton',
                      foreground=[('active', '!disabled', 'black')],
                      background=[('active', '#0052cc'), ('!active', '#007bff')])

    def _build_ui(self):
        main_frame = ttk.Frame(self, padding=15)
        main_frame.pack(expand=True, fill='both')

        # Frame de Filtros Rápidos
        filters_frame = ttk.LabelFrame(main_frame, text=" Filtros Rápidos ", padding=10)
        filters_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.btn_atraso = ttk.Button(filters_frame, text="Em Atraso",
                                   command=lambda: self.display_df(filter_status_atraso(self.df), "Vendas em Atraso"))
        self.btn_comissao = ttk.Button(filters_frame, text="> Comissão 8%",
                                     command=lambda: self.display_df(filter_high_commission(self.df), "Comissão >8%"))
        self.btn_ano = ttk.Button(filters_frame, text="Ano 2025",
                                command=lambda: self.display_df(filter_by_year(self.df, 2025), "Vendas 2025"))
        self.btn_total = ttk.Button(filters_frame, text="Total Líq. por Vendedor",
                                  command=lambda: self.display_df(total_liquido_por_vendedor(self.df), "Total Líquido"))

        for idx, btn in enumerate([self.btn_atraso, self.btn_comissao, self.btn_ano, self.btn_total]):
            btn.grid(row=idx, column=0, pady=3, sticky='ew')
            btn.grid_remove()

        # Frame de Seleção de Arquivo
        file_frame = ttk.LabelFrame(main_frame, text=" Seleção de Arquivo ", padding=10)
        file_frame.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        self.file_var = tk.StringVar(value="Nenhum arquivo selecionado")
        self.entry_file = ttk.Entry(file_frame, textvariable=self.file_var, state='readonly')
        self.entry_file.grid(row=0, column=0, padx=(0, 5), sticky='ew')
        ttk.Button(file_frame, text="Procurar", command=self.load_file).grid(row=0, column=1, sticky='ew')

        # Frame de Filtros Personalizados
        custom_filter_frame = ttk.LabelFrame(main_frame, text=" Filtros Personalizados ", padding=10)
        custom_filter_frame.grid(row=2, column=0, padx=5, pady=5, sticky='ew')

        ttk.Label(custom_filter_frame, text="Coluna para filtrar:").grid(row=0, column=0, sticky='w')
        self.combo_columns = ttk.Combobox(custom_filter_frame, state='readonly')
        self.combo_columns.grid(row=1, column=0, pady=3, sticky='ew')
        self.combo_columns.bind("<<ComboboxSelected>>", self.load_values)

        ttk.Label(custom_filter_frame, text="Valor para filtrar:").grid(row=2, column=0, sticky='w')
        self.combo_values = ttk.Combobox(custom_filter_frame, state='readonly')
        self.combo_values.grid(row=3, column=0, pady=3, sticky='ew')

        # Frame de Opções
        options_frame = ttk.LabelFrame(main_frame, text=" Opções de Relatório ", padding=10)
        options_frame.grid(row=3, column=0, padx=5, pady=5, sticky='ew')

        self.var_media_date = tk.BooleanVar()
        self.var_media_all = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Incluir média por data", variable=self.var_media_date).grid(row=0, column=0, sticky='w')
        ttk.Checkbutton(options_frame, text="Incluir média geral", variable=self.var_media_all).grid(row=1, column=0, sticky='w')

        # Botão Gerar Relatório
        ttk.Button(main_frame, text="Gerar Relatório", style='TButton', command=self.generate)\
            .grid(row=4, column=0, pady=15, sticky='ew')

        # Configurar pesos das linhas/colunas
        main_frame.columnconfigure(0, weight=1)
        filters_frame.columnconfigure(0, weight=1)
        file_frame.columnconfigure(0, weight=1)

    def load_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Arquivos Suportados", "*.csv *.xls *.xlsx *.pdf")]
        )
        if path:
            try:
                self.df = DataLoader.load(path)
                self.numeric_columns = self.df.select_dtypes(include=['number']).columns.tolist()
                self.combo_columns['values'] = self.df.columns.tolist()
                self.file_var.set(path)
                
                # Mostrar botões de filtro
                for btn in [self.btn_atraso, self.btn_comissao, self.btn_ano, self.btn_total]:
                    btn.grid()
                
                messagebox.showinfo("Sucesso", "Arquivo carregado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao carregar arquivo:\n{str(e)}")

    def load_values(self, event=None):
        col = self.combo_columns.get()
        if col and not self.df.empty:
            vals = sorted(self.df[col].dropna().astype(str).unique().tolist())
            self.combo_values['values'] = vals

    def display_df(self, df: pd.DataFrame, title: str):
        win = tk.Toplevel(self)
        win.title(title)
        win.geometry("800x500")

        container = ttk.Frame(win)
        container.pack(fill='both', expand=True)

        tv = ttk.Treeview(container, columns=list(df.columns), show='headings')
        vsb = ttk.Scrollbar(container, orient="vertical", command=tv.yview)
        hsb = ttk.Scrollbar(container, orient="horizontal", command=tv.xview)
        tv.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        for col in df.columns:
            tv.heading(col, text=col)
            tv.column(col, width=100, anchor='center')

        for _, row in df.iterrows():
            tv.insert('', 'end', values=list(row))

        tv.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

    def generate(self):
        col = self.combo_columns.get()
        val = self.combo_values.get()
        
        if not col or not val:
            messagebox.showerror("Erro", "Selecione uma coluna e um valor para filtrar!")
            return
            
        if not self.numeric_columns:
            messagebox.showerror("Erro", "Nenhuma coluna numérica encontrada!")
            return

        try:
            media_col = self.numeric_columns[0]
            df_filtered = self.df[self.df[col].astype(str) == val]

            data = {
                'filtro': f"{col}: {val}",
                'media_total': f"R$ {df_filtered[media_col].mean():.2f}",
                'media_geral': f"R$ {self.df[media_col].mean():.2f}" if self.var_media_all.get() else None,
                'observacoes': ''
            }

            self.report_gen.generate(data, 'relatorio_vendas.docx')
            messagebox.showinfo("Sucesso", "Relatório gerado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar relatório:\n{str(e)}")
