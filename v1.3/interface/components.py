from modulos import * 
from data.datafont import DataOrigin

class MainUIBuilder(DataOrigin):
    def setup_UI(self):
        self.choice_DB()
        print(self.functionExport)
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
            command=lambda: self.display_df(filter_status_atraso_db() if self.functionExport == "Banco de dados" else filter_status_atraso_local(self.df), "Vendas em Atraso")
        )
        self.btn_ano = ttk.Button(
            filters_frame,
            text="Ano 2025",
            command=lambda: self.display_df(filter_by_year_db(2025) if self.functionExport == "Banco de dados" else filter_by_year_local(self.df, 2025), "Vendas 2025")
        )
        self.btn_total = ttk.Button(
            filters_frame,
            text="Total Líq. por Vendedor",
            command=lambda: self.display_df(total_liquido_por_vendedor_db() if self.functionExport == "Banco de dados" else total_liquido_por_vendedor_local(self.df), "Total Líquido")
        )
        self.btn_total_consorcio = ttk.Button(
            filters_frame,
            text="Total Líq. por Consorcio e Vendedor",
            command=lambda: self.display_df(total_liquido_por_consorcio_vendedor_db() if self.functionExport == "Banco de dados" else total_liquido_por_consorcio_vendedor_local(self.df), "Total Líquido")
        )
        self.btn_total_consorcio_relatorio = ttk.Button(
            filters_frame,
            text="Relatório Consorciados",
            command=lambda: self.display_df(
                RelatorioToDf.generate(relatorio_por_consorciado_db() if self.functionExport == "Banco de dados" else relatorio_por_consorciado_local(self.df)),
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