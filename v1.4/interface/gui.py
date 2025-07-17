from interface.styles import StyleDefault
from interface.components import MainUIBuilder
from interface.search_db import TableSelect
from interface.dataframeview import DataFrameViewer
from data.filesmanager import FileManager
from data.exportdata import ExportFile
import tkinter as tk
from backend.report_generator import ReportGenerator
import pandas as pd




class App(
    tk.Tk,
    StyleDefault,
    MainUIBuilder,
    FileManager,
    DataFrameViewer,
    ExportFile,
    TableSelect,
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