import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from data.db import *

class DataOrigin:
    def __init__(self):
        self.functionExport = None
    
    def setFunctionExport(self, value):
        self.functionExport = value
    def ExecuteFunction(self, *args, **kwargs):
        if self.functionExport: 
            return self.functionExport(*args, **kwargs)
        else: 
            print("Erro no choices[DataOrigin]")
            return None
    def choice_DB(self, title="Selecione a origem dos dados"):
        win = tk.Toplevel(self)
        win.title(title)
        win.geometry("500x400")
        win.minsize(300, 200)

        win.transient(self)
        win.grab_set()

        # Container principal
        container = ttk.Frame(win)
        container.pack(expand=True)  # Centraliza vertical e horizontal
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        # Inner frame centralizado
        inner_frame = ttk.Frame(container)
        inner_frame.grid(row=0, column=0)
        inner_frame.columnconfigure((0, 1), weight=1)

        # Botões com textos simétricos
        btn_local = ttk.Button(
            inner_frame,
            text="🔍 Arquivo Local",
            style='TButton',
            command=lambda: [print("Local selecionado!"), self.setFunctionExport("Local"), win.destroy()]
        )
        btn_local.grid(row=0, column=0, padx=20, pady=20)

        btn_db = ttk.Button(
            inner_frame,
            text="🗄️ Banco de Dados",
            style='TButton',
            command=lambda: [print("Banco selecionado!"), self.setFunctionExport("Banco de dados"), init_db(), win.destroy()]
        )
        btn_db.grid(row=0, column=1, padx=20, pady=20)

        self.wait_window(win)
