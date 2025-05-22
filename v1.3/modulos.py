import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from backend.dataloader import DataLoader
from backend.filters import (
    filter_status_atraso,
    filter_by_year,
    count_inadimplentes,
    total_liquido_por_vendedor,
    total_liquido_por_consorcio_vendedor,
    relatorio_por_consorciado,
    clientes_inadimplentes,
    total_credito_em_atraso
)
from backend.report_generator import ReportGenerator, RelatorioToDf
from data.db import insert_upload_and_vendas
import pandas as pd
