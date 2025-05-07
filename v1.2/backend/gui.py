import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from dataloader import DataLoader
from filters import filter_status_atraso, filter_high_commission, filter_by_year, total_liquido_por_vendedor
from report_generator import ReportGenerator
import pandas as pd

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerador de Relatório de Vendas")
        self.geometry("900x600")
        self.report_gen = ReportGenerator()
        self.df = pd.DataFrame()
        self.numeric_columns = []
        self._build_ui()

    def _build_ui(self):
        frame = ttk.Frame(self, padding=10)
        frame.pack(expand=True, fill='both')

        ttk.Label(frame, text="Filtros rápidos:").grid(row=0,column=0,sticky='w')
        ttk.Button(frame,text="Em Atraso",command=lambda:self.display_df(filter_status_atraso(self.df),"Vendas em Atraso")).grid(row=1,column=0,sticky='ew')
        ttk.Button(frame,text="> Comissão 8%",command=lambda:self.display_df(filter_high_commission(self.df),"Comissão >8%")).grid(row=2,column=0,sticky='ew')
        ttk.Button(frame,text="Ano 2025",command=lambda:self.display_df(filter_by_year(self.df,2025),"Vendas 2025")).grid(row=3,column=0,sticky='ew')
        ttk.Button(frame,text="Total Líq. por Vendedor",command=lambda:self.display_df(total_liquido_por_vendedor(self.df),"Total Líquido" )).grid(row=4,column=0,sticky='ew')

        ttk.Label(frame,text="Selecione o arquivo:").grid(row=5,column=0,sticky='w')
        ttk.Button(frame,text="Procurar Arquivo",command=self.load_file).grid(row=6,column=0,sticky='ew')

        ttk.Label(frame,text="Coluna para filtrar:").grid(row=7,column=0,sticky='w')
        self.combo_columns=ttk.Combobox(frame,state='readonly')
        self.combo_columns.grid(row=8,column=0,sticky='ew')
        self.combo_columns.bind("<<ComboboxSelected>>",self.load_values)

        ttk.Label(frame,text="Valor para filtrar:").grid(row=9,column=0,sticky='w')
        self.combo_values=ttk.Combobox(frame,state='readonly')
        self.combo_values.grid(row=10,column=0,sticky='ew')

        self.var_media_date=tk.BooleanVar(); self.var_media_all=tk.BooleanVar()
        ttk.Checkbutton(frame,text="Incluir média por data",variable=self.var_media_date).grid(row=11,column=0,sticky='w')
        ttk.Checkbutton(frame,text="Incluir média geral",variable=self.var_media_all).grid(row=12,column=0,sticky='w')

        ttk.Button(frame,text="Gerar Relatório",command=self.generate).grid(row=13,column=0,pady=20,sticky='ew')

    def load_file(self):
        path=filedialog.askopenfilename(filetypes=[("Todos","*.csv *.xls *.xlsx *.pdf")])
        if not path: return
        try:
            self.df=DataLoader.load(path)
            self.numeric_columns=self.df.select_dtypes(include=['number']).columns.tolist()
            self.combo_columns['values']=self.df.columns.tolist()
        except Exception as e:
            messagebox.showerror("Erro",str(e))

    def load_values(self,event=None):
        col=self.combo_columns.get()
        if col and not self.df.empty:
            vals=sorted(self.df[col].dropna().unique().tolist())
            self.combo_values['values']=vals

    def display_df(self, df: pd.DataFrame, title: str):
        win=tk.Toplevel(self)
        win.title(title)
        tv=ttk.Treeview(win,show='headings')
        tv.pack(expand=True,fill='both')
        tv['columns']=list(df.columns)
        for col in df.columns:
            tv.heading(col,text=col)
            tv.column(col,anchor='center')
        for _, row in df.iterrows():
            tv.insert('', 'end', values=list(row))
        # add scrollbar
        sb=ttk.Scrollbar(win,orient='vertical',command=tv.yview)
        sb.pack(side='right',fill='y')
        tv.configure(yscrollcommand=sb.set)

    def generate(self):
        col, val=self.combo_columns.get(),self.combo_values.get()
        if not(col and val): messagebox.showerror("Erro","Selecione coluna/valor"); return
        if not self.numeric_columns: messagebox.showerror("Erro","Nenhuma coluna numérica"); return
        media_col=self.numeric_columns[0]
        df_filtered=self.df[self.df[col]==val]
        data={'filtro':f"{col}: {val}",'nome_vendedor':'N/A','media_total':f"R$ {df_filtered[media_col].mean():.2f}",'media_regiao':{},'media_periodo':{},'media_data':{} if self.var_media_date.get() else None,'media_geral':f"R$ {self.df[media_col].mean():.2f}" if self.var_media_all.get() else None,'observacoes':''}
        try:self.report_gen.generate(data,'relatorio_vendas.docx');messagebox.showinfo("Sucesso","Relatório gerado!")
        except Exception as e:messagebox.showerror("Erro",f"Falha: {e}")