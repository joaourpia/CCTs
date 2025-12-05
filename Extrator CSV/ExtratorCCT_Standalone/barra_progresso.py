import tkinter as tk
from tkinter import ttk
import threading

class BarraProgresso:
    """Janela de barra de progresso"""
    
    def __init__(self, titulo="Processando..."):
        self.window = None
        self.progress_var = None
        self.status_var = None
        self.titulo = titulo
        self.cancelado = False
        
    def criar_janela(self):
        """Cria a janela de progresso"""
        self.window = tk.Toplevel()
        self.window.title(self.titulo)
        self.window.geometry("500x200")
        self.window.resizable(False, False)
        
        # Centralizar
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.window.winfo_screenheight() // 2) - (200 // 2)
        self.window.geometry(f"+{x}+{y}")
        
        # Frame principal
        main_frame = tk.Frame(self.window, padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text=self.titulo,
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Status
        self.status_var = tk.StringVar(value="Iniciando...")
        status_label = tk.Label(
            main_frame,
            textvariable=self.status_var,
            font=("Arial", 10)
        )
        status_label.pack(pady=(0, 15))
        
        # Barra de progresso
        self.progress_var = tk.DoubleVar(value=0)
        progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100,
            length=440,
            mode='determinate'
        )
        progress_bar.pack(pady=(0, 15))
        
        # Label de porcentagem
        self.percent_var = tk.StringVar(value="0%")
        percent_label = tk.Label(
            main_frame,
            textvariable=self.percent_var,
            font=("Arial", 10, "bold")
        )
        percent_label.pack()
        
        # Impedir fechamento
        self.window.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Manter no topo
        self.window.attributes('-topmost', True)
        
        return self.window
    
    def atualizar(self, progresso, status=""):
        """Atualiza a barra de progresso"""
        if self.window and self.window.winfo_exists():
            self.progress_var.set(progresso)
            self.percent_var.set(f"{int(progresso)}%")
            if status:
                self.status_var.set(status)
            self.window.update()
    
    def fechar(self):
        """Fecha a janela"""
        if self.window and self.window.winfo_exists():
            self.window.destroy()
