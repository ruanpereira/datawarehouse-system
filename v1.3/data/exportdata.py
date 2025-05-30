from modulos import * 

class ExportFile:
    def export_to_excel(self, df: pd.DataFrame, title: str):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Arquivos Excel", "*.xlsx")]
        )
        if not filepath:
            return

        df_export = df.copy()
        if 'NOME CONSORCIADO' in df_export.columns and 'CONSORCIADO' not in df_export.columns:
            df_export.rename(columns={'NOME CONSORCIADO': 'CONSORCIADO'}, inplace=True)

        for col in ['DATA VENDA', 'DATA ALOCAÇÃO']:
            if col in df_export.columns:
                df_export[col] = pd.to_datetime(df_export[col], errors='coerce')

        with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
            workbook = writer.book
            sheet_name = title[:31]

            if 'CONSORCIADO' not in df_export.columns:
                df_export.to_excel(writer, sheet_name=sheet_name, index=False)
            else:
                worksheet = workbook.add_worksheet(sheet_name)
                writer.sheets[sheet_name] = worksheet

                header_fmt = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#D7E4BC', 'border': 1})
                group_fmt = workbook.add_format({'bold': True, 'font_size': 12, 'bg_color': '#F7F7F7'})
                date_fmt = workbook.add_format({'num_format': 'dd/mm/yyyy'})

                row = 0
                for cons, group in df_export.groupby('CONSORCIADO'):
                    data_info = ''
                    if 'DATA VENDA' in group.columns:
                        datas = group['DATA VENDA'].dropna()
                        if not datas.empty:
                            data_info = f" - {datas.min().strftime('%d/%m/%Y')}"

                    display_group = group.drop(columns=[c for c in ['CONSORCIADO', 'DATA VENDA'] if c in group.columns])
                    date_cols = [c for c in display_group.columns if pd.api.types.is_datetime64_any_dtype(display_group[c])]  
                    worksheet.merge_range(row, 0, row, len(display_group.columns)-1, f"{cons}{data_info}", group_fmt)
                    row += 1

                    for col_num, name in enumerate(display_group.columns):
                        worksheet.write(row, col_num, name, header_fmt)
                    row += 1

                    for rec in display_group.itertuples(index=False):
                        for col_num, val in enumerate(rec):
                            fmt = date_fmt if display_group.columns[col_num] in date_cols else None
                            if fmt:
                                worksheet.write(row, col_num, val, fmt)
                            else:
                                worksheet.write(row, col_num, val)
                        row += 1
                    row += 1

                for idx, col in enumerate(display_group.columns):
                    max_len = max(display_group[col].astype(str).map(len).max(), len(col))
                    worksheet.set_column(idx, idx, max_len + 2)

        messagebox.showinfo("Sucesso", f"Dados exportados!\n{filepath}")

    # def generate(self):
    #     col = self.combo_columns.get()
    #     val = self.combo_values.get()

    #     if not col or not val:
    #         messagebox.showerror("Erro", "Selecione uma coluna e um valor para filtrar!")
    #         return

    #     if not self.numeric_columns:
    #         messagebox.showerror("Erro", "Nenhuma coluna numérica encontrada!")
    #         return

    #     try:
    #         media_col = self.numeric_columns[0]
    #         df_filtered = self.df[self.df[col].astype(str) == val]

    #         data = {
    #             'filtro': f"{col}: {val}",
    #             'media_total': f"R$ {df_filtered[media_col].mean():.2f}",
    #             'media_geral': f"R$ {self.df[media_col].mean():.2f}" if self.var_media_all.get() else None,
    #             'Total de credito em atraso': f"{total_credito_em_atraso(self.df)}" if self.var_total_credito_atraso.get() else None,
    #             'Numero de inadimplentes no relatorio': f"{count_inadimplentes(self.df)}" if self.var_numero_inadimplentes.get() else None,
    #             'observacoes': ''
    #         }
    #         self.report_gen.generate(data, 'relatorio_vendas.docx')
    #         messagebox.showinfo("Sucesso", "Relatório gerado com sucesso!")
    #     except Exception as e:
    #         messagebox.showerror("Erro", f"Falha ao gerar relatório:\n{e}")