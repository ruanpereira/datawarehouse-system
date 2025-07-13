import tkinter as tk
from tkinter import ttk
import pandas as pd

class DataFrameViewer:
    def display_df(self, df: pd.DataFrame, title: str, visualizer: bool = False):
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

        # Caixa de pesquisa
        search_label = ttk.Label(control_frame, text="Pesquisar:")
        search_label.pack(side='left')

        search_entry = ttk.Entry(control_frame, width=20)
        search_entry.pack(side='left', padx=5)

        # Frame para seleção de colunas (apenas quando visualizer=True)
        if visualizer:
            col_frame = ttk.LabelFrame(container, text="Colunas Visíveis")
            col_frame.grid(row=2, column=0, sticky='nsew', pady=5)
            col_frame.columnconfigure(0, weight=1)
            col_frame.rowconfigure(0, weight=1)  # Permite expansão vertical
            
            # Container rolável com scroll vertical
            canvas = tk.Canvas(col_frame, height=150)
            scrollbar = ttk.Scrollbar(col_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Layout dos elementos de rolagem
            canvas.grid(row=0, column=0, sticky='nsew')
            scrollbar.grid(row=0, column=1, sticky='ns')
            
            # Variáveis para os checkboxes
            col_vars = {}
            for col in df.columns:
                col_vars[col] = tk.BooleanVar(value=True)
            
            # Organiza os checkboxes em uma única coluna (rolagem vertical)
            for i, column_name in enumerate(df.columns):
                cb = ttk.Checkbutton(
                    scrollable_frame,
                    text=column_name,
                    variable=col_vars[column_name],
                )
                cb.grid(row=i, column=0, sticky='w', padx=5, pady=2)
            
            # Controles de seleção rápida
            btn_frame = ttk.Frame(col_frame)
            btn_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky='e')
            
            ttk.Button(btn_frame, text="Selecionar Tudo",
                    command=lambda: [var.set(True) for var in col_vars.values()]).pack(side='left', padx=5)
            ttk.Button(btn_frame, text="Desmarcar Tudo",
                    command=lambda: [var.set(False) for var in col_vars.values()]).pack(side='left', padx=5)

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

        tv.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        # DataFrame filtrado inicialmente
        filtered_df = df
        visible_columns = list(df.columns)

        # Inserir dados iniciais
        for _, row in filtered_df.iterrows():
            tv.insert('', 'end', values=list(row))

        def filter_df(event=None):
            nonlocal filtered_df
            query = search_entry.get().strip()
            if query:
                mask = df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)
                filtered_df = df[mask]
            else:
                filtered_df = df
            
            refresh_treeview()

        def refresh_treeview():
            tv.delete(*tv.get_children())
            
            if visualizer:
                nonlocal visible_columns
                visible_columns = [col for col in df.columns if col_vars[col].get()]
            
            tv["columns"] = visible_columns
            for col in visible_columns:
                tv.heading(col, text=col)
            
            for _, row in filtered_df.iterrows():
                tv.insert('', 'end', values=list(row[visible_columns]))

        def update_columns():
            if visualizer:
                refresh_treeview()

        if visualizer:
            for var in col_vars.values():
                var.trace_add("write", lambda *args: update_columns())

        search_entry.bind("<KeyRelease>", filter_df)

        ttk.Button(
            control_frame,
            text="Exportar para Excel",
            command=lambda: [win.destroy(), self.export_to_excel(filtered_df, title)]
        ).pack(side='right')