from modulos import * 

class FileManager:
    def load_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Arquivos Suportados", "*.csv *.xls *.xlsx *.pdf")]
        )
        if not path:
            return

        try:
            df = DataLoader_db.load_db(path) if self.functionExport == "Banco de dados" else DataLoader_local.load_local(path)
            batch_id = insert_upload_and_vendas(df, path) if self.functionExport == "Banco de dados" else None
            self.df = df
            self.current_batch_id = batch_id if self.functionExport == "Banco de dados" else None
            self.numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
            # self.combo_columns['values'] = df.columns.tolist()
            self.file_var.set(path)

            for btn in [
                self.btn_atraso,
                self.btn_ano,
                self.btn_total,
                self.btn_total_consorcio,
                self.btn_total_consorcio_relatorio,
                self.btn_clientes_inadimplentes
            ]:
                btn.grid()

            messagebox.showinfo("Sucesso", "Arquivo carregado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar arquivo:\n{e}")

    # def load_values(self, event=None):
    #     col = self.combo_columns.get()
    #     if col and hasattr(self, 'df') and not self.df.empty:
    #         vals = sorted(self.df[col].dropna().astype(str).unique().tolist())
    #         self.combo_values['values'] = vals