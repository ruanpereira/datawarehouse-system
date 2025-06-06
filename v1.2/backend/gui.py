import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from dataloader import DataLoader
from filters import (
    filter_status_atraso,
    filter_by_year,
    count_inadimplentes,
    total_liquido_por_vendedor,
    total_liquido_por_consorcio_vendedor,
    relatorio_por_consorciado,
    clientes_inadimplentes,
    total_credito_em_atraso
)
from report_generator import ReportGenerator, RelatorioToDf
from data.db import insert_upload_and_vendas
import pandas as pd


class StyleDefault:
    def setup_style(self):
        # Cria Style sem referenciar um widget
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('.', background='#f0f2f5', font=('Segoe UI', 10))
        self.style.configure('TButton', padding=8, relief='flat', background='#007bff', foreground='white')
        self.style.map(
            'TButton',
            foreground=[('active', 'white'), ('disabled', 'gray')],
            background=[('active', '#0056b3'), ('!disabled', '#007bff')]
        )
        self.style.configure('TLabel', background='#f0f2f5', foreground='#333333')
        self.style.configure('Header.TLabel', font=('Segoe UI', 12, 'bold'), foreground='#2c3e50')
        self.style.configure('TCombobox', padding=5)
        self.style.configure('TCheckbutton', background='#f0f2f5')
        self.style.configure('TEntry', padding=5, relief='flat')
        self.style.configure('TFrame', background='#f0f2f5')
        self.style.configure('TLabelframe', background='#f0f2f5', relief='groove', borderwidth=2)
        self.style.configure('TLabelframe.Label', background='#f0f2f5', foreground='#2c3e50')
        # Estilo do botão principal
        self.style.configure('Accent.TButton', background='#28a745', foreground='white')
        self.style.map(
            'Accent.TButton',
            background=[('active', '#218838'), ('!disabled', '#28a745')]
        )


class MainUIBuilder:
    def setup_UI(self):
        # Constrói toda a interface gráfica
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
        ttk.Button(
            file_frame,
            text="Procurar",
            style='TButton',
            command=self.load_file
        ).grid(row=0, column=1, sticky='ew')

        # Frame de Filtros Rápidos
        filters_frame = ttk.LabelFrame(main_frame, text=" Filtros Rápidos ", padding=15)
        filters_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        filters_frame.columnconfigure(0, weight=1)

        # Botões de filtros rápidos (não exibidos até carregar arquivo)
        self.btn_atraso = ttk.Button(
            filters_frame,
            text="Em Atraso",
            command=lambda: self.display_df(filter_status_atraso(self.df), "Vendas em Atraso")
        )
        self.btn_ano = ttk.Button(
            filters_frame,
            text="Ano 2025",
            command=lambda: self.display_df(filter_by_year(self.df, 2025), "Vendas 2025")
        )
        self.btn_total = ttk.Button(
            filters_frame,
            text="Total Líq. por Vendedor",
            command=lambda: self.display_df(total_liquido_por_vendedor(self.df), "Total Líquido")
        )
        self.btn_total_consorcio = ttk.Button(
            filters_frame,
            text="Total Líq. por Consorcio e Vendedor",
            command=lambda: self.display_df(total_liquido_por_consorcio_vendedor(self.df), "Total Líquido")
        )
        self.btn_total_consorcio_relatorio = ttk.Button(
            filters_frame,
            text="Relatório Consorciados",
            command=lambda: self.display_df(
                RelatorioToDf.generate(relatorio_por_consorciado()),
                "Total Líquido - Relatório"
            )
        )
        self.btn_clientes_inadimplentes = ttk.Button(
            filters_frame,
            text="Clientes inadimplentes",
            command=lambda: self.display_df(clientes_inadimplentes(self.df), "Inadimplentes")
        )

        buttons = [
            self.btn_atraso,
            self.btn_ano,
            self.btn_total,
            self.btn_total_consorcio,
            self.btn_total_consorcio_relatorio,
            self.btn_clientes_inadimplentes
        ]
        # Inicialmente escondidos
        for btn in buttons:
            btn.grid_remove()

        for idx, btn in enumerate(buttons):
            r, c = (idx // 2, idx % 2)
            btn.grid(row=r, column=c, pady=4, sticky='w')

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

        ttk.Checkbutton(
            options_frame,
            text="Incluir média por data",
            variable=self.var_media_date
        ).grid(row=0, column=0, sticky='w', pady=2)

        ttk.Checkbutton(
            options_frame,
            text="Incluir média geral",
            variable=self.var_media_all
        ).grid(row=1, column=0, sticky='w', pady=2)

        ttk.Checkbutton(
            options_frame,
            text='Incluir total de credito em atraso',
            variable=self.var_total_credito_atraso
        ).grid(row=0, column=1, sticky='w', pady=2)

        ttk.Checkbutton(
            options_frame,
            text='Incluir número de inadimplentes',
            variable=self.var_numero_inadimplentes
        ).grid(row=1, column=1, sticky='w', pady=2)

        # Botão Gerar Relatório
        ttk.Button(
            main_frame,
            text="Gerar Relatório",
            style='Accent.TButton',
            command=self.generate
        ).grid(row=4, column=0, pady=15, sticky='ew')


class FileManager:
    def load_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Arquivos Suportados", "*.csv *.xls *.xlsx *.pdf")]
        )
        if not path:
            return

        try:
            df = DataLoader.load(path)
            batch_id = insert_upload_and_vendas(df, path)
            self.df = df
            self.current_batch_id = batch_id
            self.numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
            self.combo_columns['values'] = df.columns.tolist()
            self.file_var.set(path)

            # Mostrar botões de filtro após carregar
            for btn in [
                self.btn_atraso,
                self.btn_ano,
                self.btn_total,
                self.btn_total_consorcio,
                self.btn_total_consorcio_relatorio,
                self.btn_clientes_inadimplentes
            ]:
                btn.grid()

            messagebox.showinfo("Sucesso", "Arquivo carregado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar arquivo:\n{e}")

    def load_values(self, event=None):
        col = self.combo_columns.get()
        if col and hasattr(self, 'df') and not self.df.empty:
            vals = sorted(self.df[col].dropna().astype(str).unique().tolist())
            self.combo_values['values'] = vals


class DataFrameViewer:
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
            command=lambda: [ win.destroy(), self.export_to_excel(df, title)]
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


class ExportFile:
    def export_to_excel(self, df: pd.DataFrame, title: str):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Arquivos Excel", "*.xlsx")]
        )
        if not filepath:
            return

        df_export = df.copy()
        # Normaliza coluna CONSORCIADO
        if 'NOME CONSORCIADO' in df_export.columns and 'CONSORCIADO' not in df_export.columns:
            df_export.rename(columns={'NOME CONSORCIADO': 'CONSORCIADO'}, inplace=True)

        # Converte datas
        for col in ['DATA VENDA', 'DATA ALOCAÇÃO']:
            if col in df_export.columns:
                df_export[col] = pd.to_datetime(df_export[col], errors='coerce')

        with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
            workbook = writer.book
            sheet_name = title[:31]

            if 'CONSORCIADO' not in df_export.columns:
                df_export.to_excel(writer, sheet_name=sheet_name, index=False)
            else:
                worksheet = workbook.add_worksheet(sheet_name)
                writer.sheets[sheet_name] = worksheet

                header_fmt = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#D7E4BC', 'border': 1})
                group_fmt = workbook.add_format({'bold': True, 'font_size': 12, 'bg_color': '#F7F7F7'})
                date_fmt = workbook.add_format({'num_format': 'dd/mm/yyyy'})

                row = 0
                for cons, group in df_export.groupby('CONSORCIADO'):
                    data_info = ''
                    if 'DATA VENDA' in group.columns:
                        datas = group['DATA VENDA'].dropna()
                        if not datas.empty:
                            data_info = f" - {datas.min().strftime('%d/%m/%Y')}"

                    display_group = group.drop(columns=[c for c in ['CONSORCIADO', 'DATA VENDA'] if c in group.columns])
                    date_cols = [c for c in display_group.columns if pd.api.types.is_datetime64_any_dtype(display_group[c])]  
                    worksheet.merge_range(row, 0, row, len(display_group.columns)-1, f"{cons}{data_info}", group_fmt)
                    row += 1

                    for col_num, name in enumerate(display_group.columns):
                        worksheet.write(row, col_num, name, header_fmt)
                    row += 1

                    for rec in display_group.itertuples(index=False):
                        for col_num, val in enumerate(rec):
                            fmt = date_fmt if display_group.columns[col_num] in date_cols else None
                            if fmt:
                                worksheet.write(row, col_num, val, fmt)
                            else:
                                worksheet.write(row, col_num, val)
                        row += 1
                    row += 1

                for idx, col in enumerate(display_group.columns):
                    max_len = max(display_group[col].astype(str).map(len).max(), len(col))
                    worksheet.set_column(idx, idx, max_len + 2)

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
                'Total de credito em atraso': f"{total_credito_em_atraso(self.df)}" if self.var_total_credito_atraso.get() else None,
                'Numero de inadimplentes no relatorio': f"{count_inadimplentes(self.df)}" if self.var_numero_inadimplentes.get() else None,
                'observacoes': ''
            }
            self.report_gen.generate(data, 'relatorio_vendas.docx')
            messagebox.showinfo("Sucesso", "Relatório gerado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar relatório:\n{e}")


class App(
    tk.Tk,
    StyleDefault,
    MainUIBuilder,
    FileManager,
    DataFrameViewer,
    ExportFile
):
    def __init__(self):
        super().__init__()
        self.title("Análise e filtros de vendas")
        self.geometry("1000x700")
        self.minsize(800, 600)
        self.setup_style()
        self.report_gen = ReportGenerator()
        self.df = pd.DataFrame()
        self.numeric_columns = []
        self.setup_UI()
