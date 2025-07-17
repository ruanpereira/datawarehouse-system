from modulos import * 

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
            command=lambda: [win.destroy(), self.export_to_excel(df, title)]
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

