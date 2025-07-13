from data.datafont import DataOrigin
from tkinter import ttk
import tkinter as tk
from data.visualizar_dados import  visualizer_data_db, visualizer_data_local
from backend.db_filters import *
from backend.local_filters import *
from backend.report_generator import ReportGenerator, RelatorioToDf



class MainUIBuilder(DataOrigin):
    def reset_UI(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.setup_UI()

    def setup_UI(self):
        self.choice_DB()
        print(self.functionExport)

        # Constrói toda a interface gráfica
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(expand=True, fill='both')

        # Configurar grid principal
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=0)  # Modo
        main_frame.rowconfigure(1, weight=0)  # Seleção BD
        main_frame.rowconfigure(2, weight=0)  # Arquivo
        main_frame.rowconfigure(3, weight=1)  # Filtros
        main_frame.rowconfigure(4, weight=0)  # Visualizar dados

        # Botão de troca de modo
        btn_mode = ttk.Button(
            main_frame,
            text="Trocar Modo",
            command=self.reset_UI
        )
        btn_mode.grid(row=0, column=0, sticky='nw', padx=5, pady=5)

        # Se modo Banco de dados, mostra seleção
        if self.functionExport == "Banco de dados":
            lbl_select = ttk.LabelFrame(
                main_frame,
                text="Selecione um lote de vendas:",
                padding= 15
            )
            lbl_select.grid(row=1, column=0, sticky='w', padx=5, pady=(10, 2))
            lbl_select.columnconfigure(0, weight=1)
            lbl_select.columnconfigure(1, weight=0)
            
            self.combo_batch = ttk.Combobox(
                lbl_select,
                state="readonly",
                width=60,
                values=[]
            )
            self.combo_batch.grid(row=1, column=0, sticky='e', padx=5, pady=(2, 10))

            btn_load_vendas = ttk.Button(
                lbl_select,
                text="Carregar Vendas",
                command=self.load_vendas
            )
            btn_load_vendas.grid(row=1, column=1, sticky='se', padx=5, pady=(0, 5))

            # Inicializa lista de batches
            self.load_batch_ids()

        # Frame de Seleção de Arquivo
        file_frame = ttk.LabelFrame(
            main_frame,
            text=("Seleção de arquivo para upload no banco de dados" 
                  if self.functionExport == "Banco de dados" 
                  else "Seleção de Arquivo"),
            padding=15
        )
        file_frame.grid(row=2, column=0, padx=5, pady=10, sticky='ew')
        file_frame.columnconfigure(0, weight=1)
        file_frame.columnconfigure(1, weight=0)

        self.file_var = tk.StringVar(value="Nenhum arquivo selecionado")
        entry_file = ttk.Entry(
            file_frame,
            textvariable=self.file_var,
            state='readonly'
        )
        entry_file.grid(row=0, column=0, padx=(0, 10), sticky='ew')

        # Ao selecionar arquivo, atualiza combobox caso em modo BD
        def on_file_select():
            self.load_file()
            if self.functionExport == "Banco de dados":
                # recarrega os batch IDs incluindo novo upload
                self.load_batch_ids()
                # ajusta combobox para exibir o mais recente
                ids = list(self.combo_batch['values'])
                if ids:
                    self.combo_batch.set(ids[-1])

        btn_browse = ttk.Button(
            file_frame,
            text="Procurar",
            style='TButton',
            command=on_file_select
        )
        btn_browse.grid(row=0, column=1, sticky='e')

        # Frame de Filtros Rápidos
        filters_frame = ttk.LabelFrame(
            main_frame,
            text="Filtros Rápidos",
            padding=15
        )
        filters_frame.grid(row=3, column=0, padx=5, pady=10, sticky='nsew')
        filters_frame.columnconfigure(0, weight=1)
        filters_frame.columnconfigure(1, weight=1)

        # Botões de filtros rápidos
        self.btn_atraso = ttk.Button(
            filters_frame,
            text="Em Atraso",
            command=lambda: self.display_df(
                filter_status_atraso_db(self.df) if self.functionExport == "Banco de dados" else filter_status_atraso_local(self.df),
                "Vendas em Atraso"
            )
        )
        self.btn_ano = ttk.Button(
            filters_frame,
            text="Ano 2025",
            command=lambda: self.display_df(
                filter_by_year_db(self.df, 2025) if self.functionExport == "Banco de dados" else filter_by_year_local(self.df, 2025),
                "Vendas 2025"
            )
        )
        self.btn_total = ttk.Button(
            filters_frame,
            text="Total Líq. por Vendedor",
            command=lambda: self.display_df(
                total_liquido_por_vendedor_db(self.df) if self.functionExport == "Banco de dados" else total_liquido_por_vendedor_local(self.df),
                "Total Líquido"
            )
        )
        self.btn_total_consorcio = ttk.Button(
            filters_frame,
            text="Total Líq. por Consórcio e Vendedor",
            command=lambda: self.display_df(
                total_liquido_por_consorcio_vendedor_db(self.df) if self.functionExport == "Banco de dados" else total_liquido_por_consorcio_vendedor_local(self.df),
                "Total Líquido"
            )
        )
        self.btn_total_consorcio_relatorio = ttk.Button(
            filters_frame,
            text="Relatório Consorciados",
            command=lambda: self.display_df(
                RelatorioToDf.generate(
                    relatorio_por_consorciado_db(self.df) if self.functionExport == "Banco de dados" else relatorio_por_consorciado_local(self.df)
                ),
                "Total Líquido - Relatório"
            )
        )
        self.btn_clientes_inadimplentes = ttk.Button(
            filters_frame,
            text="Clientes Inadimplentes",
            command=lambda: self.display_df(
                clientes_inadimplentes(self.df),
                "Inadimplentes"
            )
        )

        buttons = [
            self.btn_atraso,
            self.btn_ano,
            self.btn_total,
            self.btn_total_consorcio,
            self.btn_total_consorcio_relatorio,
            self.btn_clientes_inadimplentes
        ]
        for btn in buttons:
            btn.grid_remove()

        num_rows = (len(buttons) + 1) // 2
        for row in range(num_rows):
            filters_frame.rowconfigure(row, pad=15)
        for idx, btn in enumerate(buttons):
            r, c = divmod(idx, 2)
            btn.grid(row=r, column=c, padx=5, pady=2, sticky='we')
        # Frame de Visualizar Dados
        visualizar_frame = ttk.LabelFrame(
            main_frame,
            text="Visualizar dados",
            padding=15
        )
        visualizar_frame.grid(row=4, column=0, padx=5, pady=10, sticky='ew')

        # Configurar a primeira coluna do visualizar_frame para expandir horizontalmente
        visualizar_frame.columnconfigure(0, weight=1)

        # Criar o botão
        btn_visualizar = ttk.Button(
            visualizar_frame,
            text="Visualizar",
            command=lambda: self.display_df(
                visualizer_data_db(self.df) if self.functionExport == "Banco de dados" else visualizer_data_local(self.df),
                "Dados", True
            )
        )

        # Posicionar o botão na linha 0, coluna 0 com sticky='ew' para expansão horizontal
        btn_visualizar.grid(row=0, column=0, sticky='ew', padx=5, pady=5)