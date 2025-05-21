import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from dataloader import DataLoader
from filters import filter_status_atraso, filter_by_year, count_inadimplentes, total_liquido_por_vendedor, total_liquido_por_consorcio_vendedor, relatorio_por_consorciado, clientes_inadimplentes, total_credito_em_atraso
from report_generator import ReportGenerator, RelatorioToDf
import pandas as pd
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerador de Relatório de Vendas")
        self.geometry("1000x700")
        self.minsize(800, 600)
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.configure_style()
        self.report_gen = ReportGenerator()
        self.df = pd.DataFrame()
        self.numeric_columns = []
        self.filter_buttons = []
        self._build_ui()
        
    def configure_style(self):
        self.style.configure('.', background='#f0f2f5', font=('Segoe UI', 10))
        self.style.configure('TButton', padding=8, relief='flat', background='#007bff', foreground='white')
        self.style.map('TButton',
                      foreground=[('active', 'white'), ('disabled', 'gray')],
                      background=[('active', '#0056b3'), ('!disabled', '#007bff')])
        self.style.configure('TLabel', background='#f0f2f5', foreground='#333333')
        self.style.configure('Header.TLabel', font=('Segoe UI', 12, 'bold'), foreground='#2c3e50')
        self.style.configure('TCombobox', padding=5)
        self.style.configure('TCheckbutton', background='#f0f2f5')
        self.style.configure('TEntry', padding=5, relief='flat')
        self.style.configure('TFrame', background='#f0f2f5')
        self.style.configure('TLabelframe', background='#f0f2f5', relief='groove', borderwidth=2)
        self.style.configure('TLabelframe.Label', background='#f0f2f5', foreground='#2c3e50')

    def _build_ui(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(expand=True, fill='both')

        # Configurar grid principal
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)

        # Frame de Seleção de Arquivo
        file_frame = ttk.LabelFrame(main_frame, text=" Seleção de Arquivo ", padding=15)
        file_frame.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        file_frame.columnconfigure(0, weight=1)

        self.file_var = tk.StringVar(value="Nenhum arquivo selecionado")
        self.entry_file = ttk.Entry(file_frame, textvariable=self.file_var, state='readonly')
        self.entry_file.grid(row=0, column=0, padx=(0, 10), sticky='ew')
        ttk.Button(file_frame, text="Procurar", style='TButton', command=self.load_file)\
            .grid(row=0, column=1, sticky='ew')

        # Frame de Filtros Rápidos
        filters_frame = ttk.LabelFrame(main_frame, text=" Filtros Rápidos ", padding=15)
        filters_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        filters_frame.columnconfigure(0, weight=1)

        self.btn_atraso = ttk.Button(filters_frame, text="Em Atraso",
                                   command=lambda: self.display_df(filter_status_atraso(self.df), "Vendas em Atraso"))
        self.btn_ano = ttk.Button(filters_frame, text="Ano 2025",
                                command=lambda: self.display_df(filter_by_year(self.df, 2025), "Vendas 2025"))
        self.btn_total = ttk.Button(filters_frame, text="Total Líq. por Vendedor",
                                  command=lambda: self.display_df(total_liquido_por_vendedor(self.df), "Total Líquido"))
        self.btn_total_consorcio = ttk.Button(filters_frame, text="Total Líq. por Consorcio e Vendedor",
                                  command=lambda: self.display_df(total_liquido_por_consorcio_vendedor(self.df), "Total Líquido"))
        self.btn_total_consorcio_relatorio = ttk.Button(filters_frame, text="Relatório Consorciados",
                                  command=lambda: self.display_df(RelatorioToDf.generate(relatorio_por_consorciado(self.df)), "Total Líquido - Relatório"))
        self.btn_clientes_inadimplentes = ttk.Button(filters_frame, text="Clientes inadimplantes", 
                                    command= lambda: self.display_df(clientes_inadimplentes(self.df), "Inadimplentes"))

        buttons = [self.btn_atraso, self.btn_ano, 
                  self.btn_total, self.btn_total_consorcio, self.btn_total_consorcio_relatorio, self.btn_clientes_inadimplentes]
        
        for idx, btn in enumerate(buttons):
            if idx%2==0:
                btn.grid(row=idx, column=0, pady=4, sticky='w')
            else:
                btn.grid(row=idx-1, column=1, pady=4, sticky='w') 

        # Frame de Filtros Personalizados
        custom_filter_frame = ttk.LabelFrame(main_frame, text=" Filtros Personalizados ", padding=15)
        custom_filter_frame.grid(row=2, column=0, padx=5, pady=5, sticky='ew')
        custom_filter_frame.columnconfigure(0, weight=1)

        ttk.Label(custom_filter_frame, text="Coluna para filtrar:").grid(row=0, column=0, sticky='w')
        self.combo_columns = ttk.Combobox(custom_filter_frame, state='readonly')
        self.combo_columns.grid(row=1, column=0, pady=5, sticky='ew')
        self.combo_columns.bind("<<ComboboxSelected>>", self.load_values)

        ttk.Label(custom_filter_frame, text="Valor para filtrar:").grid(row=2, column=0, sticky='w')
        self.combo_values = ttk.Combobox(custom_filter_frame, state='readonly')
        self.combo_values.grid(row=3, column=0, pady=5, sticky='ew')

        # Frame de Opções
        options_frame = ttk.LabelFrame(main_frame, text=" Opções de Relatório ", padding=15)
        options_frame.grid(row=3, column=0, padx=5, pady=5, sticky='ew')
        options_frame.columnconfigure(0, weight=1)

        self.var_media_date = tk.BooleanVar()
        self.var_media_all = tk.BooleanVar()
        self.var_total_credito_atraso = tk.BooleanVar()
        self.var_numero_inadimplentes = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Incluir média por data", variable=self.var_media_date)\
            .grid(row=0, column=0, sticky='w', pady=2)
        ttk.Checkbutton(options_frame, text="Incluir média geral", variable=self.var_media_all)\
            .grid(row=1, column=0, sticky='w', pady=2)
        ttk.Checkbutton(options_frame, text='Incluir total de credito em atraso', variable=self.var_total_credito_atraso)\
            .grid(row=0, column=1, sticky='w', pady=2)
        ttk.Checkbutton(options_frame, text='Incluir número de inadimplentes', variable=self.var_numero_inadimplentes)\
            .grid(row=1, column=1, sticky='w', pady=2)

        # Botão Gerar Relatório
        ttk.Button(main_frame, text="Gerar Relatório", style='Accent.TButton', command=self.generate)\
            .grid(row=4, column=0, pady=15, sticky='ew')

        # Criar estilo adicional para botão principal
        self.style.configure('Accent.TButton', background='#28a745', foreground='white')
        self.style.map('Accent.TButton',
                      background=[('active', '#218838'), ('!disabled', '#28a745')])

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
                for btn in [self.btn_atraso, self.btn_ano, self.btn_total, self.btn_total_consorcio,self.btn_total_consorcio_relatorio, self.btn_clientes_inadimplentes ]:
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
        win.geometry("900x600")
        win.minsize(600, 400)

        container = ttk.Frame(win)
        container.pack(fill='both', expand=True, padx=10, pady=10)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(1, weight=1)

        # Frame de controles
        control_frame = ttk.Frame(container)
        control_frame.grid(row=0, column=0, sticky='ew', pady=(0, 10))

        ttk.Button(
            control_frame,
            text="Exportar para Excel",
            style='TButton',
            command=lambda: self.export_to_excel(df, title)
        ).pack(side='right')

        # Treeview
        tv_frame = ttk.Frame(container)
        tv_frame.grid(row=1, column=0, sticky='nsew')
        tv_frame.columnconfigure(0, weight=1)
        tv_frame.rowconfigure(0, weight=1)

        tv = ttk.Treeview(tv_frame, columns=list(df.columns), show='headings')
        vsb = ttk.Scrollbar(tv_frame, orient="vertical", command=tv.yview)
        hsb = ttk.Scrollbar(tv_frame, orient="horizontal", command=tv.xview)
        tv.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        for col in df.columns:
            tv.heading(col, text=col)
            tv.column(col, width=100, anchor='center', minwidth=50)

        for _, row in df.iterrows():
            tv.insert('', 'end', values=list(row))

        tv.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
    
    def export_to_excel(self, df: pd.DataFrame, title: str):
        # Pergunta onde salvar
        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Arquivos Excel", "*.xlsx")]
        )
        if not filepath:
            return

        # Verifica se 'CONSORCIADO' existe
        if 'NOME CONSORCIADO' not in df.columns:
            messagebox.showerror("Erro", "A coluna 'NOME CONSORCIADO' não está presente no DataFrame.")
            return

        # Cria o writer usando xlsxwriter
        with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
            workbook  = writer.book
            sheet_name = title[:31]  # máximo 31 chars
            worksheet = workbook.add_worksheet(sheet_name)
            writer.sheets[sheet_name] = worksheet

            # Formatos
            header_fmt = workbook.add_format({
                'bold': True,
                'align': 'center',
                'bg_color': '#D7E4BC',
                'border': 1
            })
            group_fmt = workbook.add_format({
                'bold': True,
                'font_size': 12,
                'bg_color': '#F7F7F7'
            })

            row = 0
            # Itera por cada grupo de consorciado
            for consorciado, group in df.groupby('NOME CONSORCIADO'):
                # Extrai faixa de datas (caso haja)
                data_info = ""
                if 'DATA VENDA' in group.columns:
                    datas = pd.to_datetime(group['DATA VENDA'].dropna(), errors='coerce')
                    if not datas.empty:
                        data_min = datas.min().strftime('%d/%m/%Y')
                        data_info = f" - {data_min}"

                # Remove as colunas 'NOME CONSORCIADO' e 'DATA VENDA' se existirem
                cols_to_drop = [col for col in ['NOME CONSORCIADO', 'DATA VENDA'] if col in group.columns]
                group = group.drop(columns=cols_to_drop)

                # Título do grupo
                titulo_grupo = f"{consorciado}{data_info}"
                worksheet.merge_range(row, 0, row, len(group.columns)-1, titulo_grupo, group_fmt)
                row += 1

                # Cabeçalhos
                for col_num, col_name in enumerate(group.columns):
                    worksheet.write(row, col_num, col_name, header_fmt)
                row += 1

                # Dados
                for record in group.itertuples(index=False):
                    for col_num, value in enumerate(record):
                        worksheet.write(row, col_num, value)
                    row += 1

                # Linha em branco
                row += 1

            # Ajusta largura das colunas (sem CONSORCIADO/DATA VENDA)
            cols_to_measure = [col for col in df.columns if col not in ['NOME CONSORCIADO', 'DATA VENDA']]
            for i, col in enumerate(cols_to_measure):
                max_len = max(
                    df[col].astype(str).map(len).max(),
                    len(col)
                )
                worksheet.set_column(i, i, max_len + 2)

        messagebox.showinfo("Sucesso", f"Dados exportados!\n{filepath}")

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
                'Total de credito em atraso': f"{total_credito_em_atraso(self.df)} "  if self.var_total_credito_atraso.get() else None,
                'Numero de inadimplentes no relatorio': f"{count_inadimplentes(self.df)} "  if self.var_numero_inadimplentes.get() else None,
                'observacoes': ''
            }

            self.report_gen.generate(data, 'relatorio_vendas.docx')
            messagebox.showinfo("Sucesso", "Relatório gerado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar relatório:\n{str(e)}")
