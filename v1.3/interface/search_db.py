import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy import select
import sys
import os

# Adiciona o diretório pai ao sys.path para importar o módulo corretamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data.db import Session, uploads, query_vendas_by_batch, query_vendas_by_name

class TableSelect():
    def __init__(self):

        self.title("Consulta por Arquivo e Data de Upload")
        self.geometry("600x400")
        self.df
        self.choiceTable()

    def load_batch_ids(self):
        session = Session()
        # Busca origem_arquivo e data_upload
        result = session.execute(select(uploads.c.origem_arquivo, uploads.c.data_upload)).all()
        session.close()
        print("resetou")
        # Exibe no combobox como "arquivo - data"
        display_values = [f"{row.origem_arquivo} - {row.data_upload.strftime('%Y-%m-%d')}" for row in result]
        self.batch_map = {f"{row.origem_arquivo} - {row.data_upload.strftime('%Y-%m-%d')}": row.origem_arquivo for row in result}

        self.combo_batch['values'] = display_values
        if display_values:
            self.combo_batch.set(display_values[0])

    def load_vendas(self):
        selected = self.combo_batch.get()
        messagebox.showinfo("Dados Selecionados!", "Esses dados vão ser usados para filtragem.")
        if not selected or selected not in self.batch_map:
            messagebox.showwarning("Atenção", "Selecione um item válido.")
            return

        origem_arquivo = self.batch_map[selected]
        self.df = query_vendas_by_name(origem_arquivo)
        if self.df.empty:
            messagebox.showinfo("DataFrame vazio ou com erro")

if __name__ == "__main__":
    app = TableSelect()
    app.mainloop()
