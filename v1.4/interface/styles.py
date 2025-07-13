from tkinter import ttk
class StyleDefault:
    def setup_style(self):
        # Cria Style sem referenciar um widget
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('.', background='#f0f2f5', font=('Segoe UI', 10))
        self.style.configure('TButton', padding=8, relief='flat', background='#007bff', foreground='white')
        self.style.map(
            'TButton',
            foreground=[('active', 'white'), ('disabled', 'gray')],
            background=[('active', '#0056b3'), ('!disabled', '#007bff')]
        )
        self.style.configure('TLabel', background='#f0f2f5', foreground='#333333')
        self.style.configure('Header.TLabel', font=('Segoe UI', 12, 'bold'), foreground='#2c3e50')
        self.style.configure('TCombobox', padding=5)
        self.style.configure('TCheckbutton', background='#f0f2f5')
        self.style.configure('TEntry', padding=5, relief='flat')
        self.style.configure('TFrame', background='#f0f2f5')
        self.style.configure('TLabelframe', background='#f0f2f5', relief='groove', borderwidth=2)
        self.style.configure('TLabelframe.Label', background='#f0f2f5', foreground='#2c3e50')
        # Estilo do botão principal
        self.style.configure('Accent.TButton', background='#28a745', foreground='white')
        self.style.map(
            'Accent.TButton',
            background=[('active', '#218838'), ('!disabled', '#28a745')]
        )