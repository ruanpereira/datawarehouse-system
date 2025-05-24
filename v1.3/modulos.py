import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from backend.dataloader_db import DataLoader_db
from backend.dataload_local import DataLoader_local
from backend.db_filters import (
    filter_status_atraso_db,
    filter_by_year_db,
    count_inadimplentes, # tem que arrumar dps
    total_liquido_por_vendedor_db,
    total_liquido_por_consorcio_vendedor_db,
    relatorio_por_consorciado_db,
    clientes_inadimplentes, # tem que arrumar dps
    total_credito_em_atraso # tem que arrumar dps
)
from backend.local_filters import (
    filter_status_atraso_local,
    filter_by_year_local,
    count_inadimplentes, # tem que arrumar dps
    total_liquido_por_vendedor_local,
    total_liquido_por_consorcio_vendedor_local,
    relatorio_por_consorciado_local,
    clientes_inadimplentes, # tem que arrumar dps
    total_credito_em_atraso # tem que arrumar dps
)
from backend.report_generator import ReportGenerator, RelatorioToDf
from data.db import insert_upload_and_vendas
import pandas as pd
