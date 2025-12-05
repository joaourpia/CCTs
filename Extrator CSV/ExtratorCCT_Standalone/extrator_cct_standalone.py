#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrator de Dados de Convenções Coletivas de Trabalho (CCTs) - Versão Standalone
Autor: Manus AI
Descrição: Versão portátil com configuração de API key via interface
"""

import os
import sys
import re
import csv
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io
from openai import OpenAI
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk



# Código adicional para v4.0
# Adicionar ao extrator_cct_standalone.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import shutil
from pathlib import Path


class BarraProgresso:
    """Barra de progresso visual"""
    
    def __init__(self, titulo="Processando..."):
        self.titulo = titulo
        self.janela = None
        self.progresso = None
        self.label_status = None
        self.label_porcentagem = None
        
    def criar_janela(self):
        """Cria janela de progresso"""
        self.janela = tk.Toplevel()
        self.janela.title(self.titulo)
        self.janela.geometry("500x150")
        self.janela.resizable(False, False)
        
        # Centralizar
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (150 // 2)
        self.janela.geometry(f"+{x}+{y}")
        
        # Frame principal
        frame = tk.Frame(self.janela, padx=30, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo_label = tk.Label(frame, text=self.titulo, font=("Arial", 12, "bold"))
        titulo_label.pack(pady=(0, 15))
        
        # Barra de progresso
        self.progresso = ttk.Progressbar(frame, length=440, mode='determinate', maximum=100)
        self.progresso.pack(pady=(0, 10))
        
        # Status
        self.label_status = tk.Label(frame, text="Iniciando...", font=("Arial", 9))
        self.label_status.pack()
        
        # Porcentagem
        self.label_porcentagem = tk.Label(frame, text="0%", font=("Arial", 10, "bold"))
        self.label_porcentagem.pack(pady=(5, 0))
        
        self.janela.update()
        
    def atualizar(self, valor, status=""):
        """Atualiza progresso"""
        if self.janela and self.janela.winfo_exists():
            self.progresso['value'] = valor
            if status:
                self.label_status.config(text=status)
            self.label_porcentagem.config(text=f"{int(valor)}%")
            self.janela.update()
    
    def fechar(self):
        """Fecha janela"""
        if self.janela and self.janela.winfo_exists():
            self.janela.destroy()


def janela_confirmacao_csv(csv_path, total_clausulas, convencao):
    """Mostra janela de confirmação após extração"""
    
    dialog = tk.Toplevel()
    dialog.title("Extração Concluída")
    dialog.geometry("600x400")  # Aumentado de 300 para 400 para mostrar botões
    dialog.resizable(False, False)
    
    # Centralizar
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
    y = (dialog.winfo_screenheight() // 2) - (300 // 2)
    dialog.geometry(f"+{x}+{y}")
    
    # Frame principal
    main_frame = tk.Frame(dialog, padx=30, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Ícone de sucesso
    success_label = tk.Label(main_frame, text="✅", font=("Arial", 48))
    success_label.pack(pady=(0, 10))
    
    # Título
    title_label = tk.Label(main_frame, text="Extração Concluída com Sucesso!", font=("Arial", 14, "bold"))
    title_label.pack(pady=(0, 15))
    
    # Informações
    info_frame = tk.Frame(main_frame)
    info_frame.pack(pady=(0, 20))
    
    info_text = f"""
Arquivo CSV gerado: {Path(csv_path).name}

Total de cláusulas extraídas: {total_clausulas}
Convenção: {convencao}

Deseja conferir o arquivo e integrá-lo à planilha mãe?
    """
    
    info_label = tk.Label(info_frame, text=info_text, font=("Arial", 10), justify=tk.LEFT)
    info_label.pack()
    
    # Resultado
    result = {"acao": None}
    
    def abrir_csv():
        """Abre CSV no aplicativo padrão"""
        import os
        import platform
        
        try:
            if platform.system() == 'Windows':
                os.startfile(csv_path)
            elif platform.system() == 'Darwin':  # macOS
                os.system(f'open "{csv_path}"')
            else:  # Linux
                os.system(f'xdg-open "{csv_path}"')
            
            # Mostrar mensagem de confirmação
            messagebox.showinfo(
                "Arquivo Aberto",
                "O arquivo CSV foi aberto no aplicativo padrão.\n\nVocê ainda pode integrar com a planilha mãe ou fechar.",
                parent=dialog
            )
        except Exception as e:
            messagebox.showerror(
                "Erro",
                f"Não foi possível abrir o arquivo:\n{str(e)}",
                parent=dialog
            )
    
    def integrar():
        result["acao"] = "integrar"
        dialog.destroy()
    
    def fechar():
        result["acao"] = "fechar"
        dialog.destroy()
    
    # Botões
    button_frame = tk.Frame(main_frame)
    button_frame.pack()
    
    tk.Button(button_frame, text="📄 Abrir CSV", command=abrir_csv, font=("Arial", 10), padx=15, pady=8).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="✅ Integrar com Planilha Mãe", command=integrar, font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", padx=15, pady=8).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Fechar", command=fechar, font=("Arial", 10), padx=15, pady=8).pack(side=tk.LEFT, padx=5)
    
    # Aguardar usuário
    dialog.transient()
    dialog.grab_set()
    dialog.wait_window()
    
    return result["acao"]


def selecionar_planilha_mae():
    """Permite usuário selecionar planilha mãe"""
    
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    arquivo = filedialog.askopenfilename(
        title="Selecione a Planilha Mãe (CSV)",
        filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")],
        initialdir=os.getcwd()
    )
    
    root.destroy()
    return arquivo


def integrar_com_planilha_mae(csv_extraido, csv_mae):
    """Integra dados extraídos na planilha mãe"""
    
    try:
        # 1. Fazer backup da planilha mãe
        backup_path = str(Path(csv_mae).with_suffix('.backup.csv'))
        shutil.copy2(csv_mae, backup_path)
        print(f"✓ Backup criado: {backup_path}")
        
        # 2. Ler CSV extraído (pular cabeçalho)
        with open(csv_extraido, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Pular cabeçalho
            dados_extraidos = list(reader)
        
        # 3. Adicionar ao CSV mãe
        with open(csv_mae, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerows(dados_extraidos)
        
        print(f"✓ {len(dados_extraidos)} cláusulas adicionadas à planilha mãe")
        
        # Mensagem de sucesso
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        messagebox.showinfo(
            "Integração Concluída",
            f"✅ Sucesso!\n\n"
            f"{len(dados_extraidos)} cláusulas foram adicionadas à planilha mãe.\n\n"
            f"Backup criado: {Path(backup_path).name}"
        )
        
        root.destroy()
        return True
        
    except Exception as e:
        # Mensagem de erro
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        messagebox.showerror(
            "Erro na Integração",
            f"❌ Erro ao integrar dados:\n\n{str(e)}"
        )
        
        root.destroy()
        return False



class ConfigManager:
    """Gerencia configurações do aplicativo"""
    
    def __init__(self):
        # Diretório de configuração no AppData do usuário
        if sys.platform == 'win32':
            self.config_dir = Path(os.getenv('APPDATA')) / 'ExtratorCCT'
        else:
            self.config_dir = Path.home() / '.extrator_cct'
        
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / 'config.json'
        self.config = self.load_config()
    
    def load_config(self) -> dict:
        """Carrega configurações"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_config(self):
        """Salva configurações"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
    
    def get_api_key(self) -> Optional[str]:
        """Obtém API key"""
        return self.config.get('openai_api_key')
    
    def set_api_key(self, api_key: str):
        """Define API key"""
        self.config['openai_api_key'] = api_key
        self.save_config()
    
    def get_tesseract_path(self) -> Optional[str]:
        """Obtém caminho do Tesseract"""
        return self.config.get('tesseract_path')
    
    def set_tesseract_path(self, path: str):
        """Define caminho do Tesseract"""
        self.config['tesseract_path'] = path
        self.save_config()


class ConfigDialog:
    """Diálogo de configuração"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.result = None
        
    def show(self):
        """Mostra diálogo de configuração"""
        root = tk.Tk()
        root.title("Configuração - Extrator de CCTs")
        root.geometry("500x300")
        root.resizable(False, False)
        
        # Centralizar janela
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (500 // 2)
        y = (root.winfo_screenheight() // 2) - (300 // 2)
        root.geometry(f"500x300+{x}+{y}")
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = ttk.Label(main_frame, text="Configuração Inicial", font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # API Key da OpenAI
        ttk.Label(main_frame, text="API Key da OpenAI:", font=('Arial', 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(main_frame, text="(Opcional - para resumos com IA)", font=('Arial', 8), foreground='gray').grid(row=2, column=0, sticky=tk.W)
        
        api_key_var = tk.StringVar(value=self.config_manager.get_api_key() or "")
        api_key_entry = ttk.Entry(main_frame, textvariable=api_key_var, width=50, show="*")
        api_key_entry.grid(row=3, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        # Botão para mostrar/ocultar API key
        show_key_var = tk.BooleanVar(value=False)
        
        def toggle_show_key():
            if show_key_var.get():
                api_key_entry.config(show="")
            else:
                api_key_entry.config(show="*")
        
        show_key_check = ttk.Checkbutton(main_frame, text="Mostrar API key", variable=show_key_var, command=toggle_show_key)
        show_key_check.grid(row=4, column=0, sticky=tk.W, pady=5)
        
        # Link para obter API key
        link_label = ttk.Label(main_frame, text="Obter API key: https://platform.openai.com/api-keys", 
                              font=('Arial', 8), foreground='blue', cursor='hand2')
        link_label.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        def open_link(event):
            import webbrowser
            webbrowser.open("https://platform.openai.com/api-keys")
        
        link_label.bind("<Button-1>", open_link)
        
        # Separador
        ttk.Separator(main_frame, orient='horizontal').grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=20)
        
        # Nota sobre Tesseract
        note_label = ttk.Label(main_frame, 
                              text="Nota: O Tesseract OCR será configurado automaticamente\nse estiver instalado no sistema.",
                              font=('Arial', 9), foreground='gray', justify=tk.LEFT)
        note_label.grid(row=7, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=(20, 0))
        
        def save_and_close():
            api_key = api_key_var.get().strip()
            if api_key:
                self.config_manager.set_api_key(api_key)
            self.result = True
            root.destroy()
        
        def skip():
            self.result = True
            root.destroy()
        
        ttk.Button(button_frame, text="Salvar", command=save_and_close, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Pular (usar sem IA)", command=skip, width=20).pack(side=tk.LEFT, padx=5)
        
        root.mainloop()
        return self.result


def find_tesseract():
    """Tenta encontrar Tesseract instalado no sistema"""
    # Locais comuns no Windows
    common_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        r"C:\Tesseract-OCR\tesseract.exe",
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    # Tentar encontrar no PATH
    import shutil
    tesseract_path = shutil.which("tesseract")
    if tesseract_path:
        return tesseract_path
    
    return None


def selecionar_pdf():
    """Abre janela do Windows Explorer para selecionar PDF"""
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo PDF da CCT",
        filetypes=[("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")],
        initialdir=os.getcwd()
    )
    
    root.destroy()
    return arquivo


def selecionar_csv_saida(pdf_path):
    """Abre janela do Windows Explorer para salvar CSV"""
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    nome_base = Path(pdf_path).stem
    nome_sugerido = f"{nome_base}_extraido.csv"
    
    arquivo = filedialog.asksaveasfilename(
        title="Salvar CSV como",
        defaultextension=".csv",
        filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")],
        initialfile=nome_sugerido,
        initialdir=os.path.dirname(pdf_path) or os.getcwd()
    )
    
    root.destroy()
    return arquivo


class ExtratorCCT:
    """Classe para extrair dados de PDFs usando Tesseract OCR"""
    
    def __init__(self, pdf_path: str, config_manager: ConfigManager):
        self.pdf_path = pdf_path
        self.config_manager = config_manager
        self.texto_completo = ""
        self.sindicato = ""
        self.convencao = ""
        self.clausulas = []
        
        # Configurar OpenAI se disponível
        api_key = config_manager.get_api_key()
        self.usar_ia = False
        if api_key:
            try:
                self.client = OpenAI(api_key=api_key)
                self.usar_ia = True
            except:
                self.usar_ia = False
        
        # Configurar Tesseract
        tesseract_path = config_manager.get_tesseract_path()
        if not tesseract_path:
            tesseract_path = find_tesseract()
            if tesseract_path:
                config_manager.set_tesseract_path(tesseract_path)
        
        if tesseract_path and os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
    def extrair_texto_pdf_ocr(self) -> str:
        """Extrai texto do PDF usando Tesseract OCR"""
        print(f"\n📄 Extraindo texto do PDF com OCR de alta qualidade...")
        print("   ⏳ Este processo pode demorar alguns minutos...")
        print()
        
        texto_completo = []
        
        try:
            doc = fitz.open(self.pdf_path)
            total_paginas = len(doc)
            
            for i, page in enumerate(doc, 1):
                print(f"   Processando página {i}/{total_paginas}... ", end='', flush=True)
                
                # Converter página para imagem em alta resolução
                pix = page.get_pixmap(dpi=300)
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                
                # Executar OCR
                texto_pagina = pytesseract.image_to_string(img, lang='por')
                
                if texto_pagina.strip():
                    texto_completo.append(texto_pagina)
                    print("✓")
                else:
                    print("(vazia)")
            
            doc.close()
            
            self.texto_completo = "\n".join(texto_completo)
            print(f"\n✓ Extração concluída: {len(self.texto_completo)} caracteres\n")
            return self.texto_completo
            
        except Exception as e:
            print(f"\n❌ Erro ao extrair texto do PDF: {e}")
            raise
    
    def _buscar_todos_sindicatos(self, texto: str) -> list:
        """Busca todos os sindicatos mencionados no texto"""
        padrão = r'(SINDICATO\s+DOS?\s+[A-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ\s]+?)(?=\s*[-—,]|\s+CNPJ|\s+sito|\s+neste)'
        matches = re.findall(padrão, texto, re.IGNORECASE)
        
        # Normalizar e remover duplicatas
        sindicatos = []
        vistos = set()
        
        for match in matches:
            normalizado = ' '.join(match.split()).upper()
            if normalizado not in vistos and len(normalizado) > 20:
                sindicatos.append(normalizado)
                vistos.add(normalizado)
        
        return sindicatos[:10]  # Máximo 10 opções
    
    def _confirmar_sindicato(self, sindicato_detectado: str, todos_sindicatos: list) -> str:
        """Permite usuário escolher/editar o sindicato"""
        
        # Criar janela de seleção
        dialog = tk.Toplevel()
        dialog.title("Confirmar Sindicato")
        dialog.geometry("700x500")  # Reduzido para caber o botão
        dialog.resizable(True, True)
        
        # Centralizar janela
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (700 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Frame principal com scroll
        main_frame = tk.Frame(dialog, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="Confirme ou Escolha o Sindicato dos Empregados",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=(0, 15))
        
        # Sindicato detectado
        if sindicato_detectado and sindicato_detectado != "SINDICATO NÃO IDENTIFICADO":
            detected_frame = tk.LabelFrame(main_frame, text="Sindicato Detectado Automaticamente", font=("Arial", 10, "bold"))
            detected_frame.pack(fill=tk.X, pady=(0, 15))
            
            detected_label = tk.Label(
                detected_frame,
                text=sindicato_detectado,
                font=("Arial", 10),
                wraplength=640,
                justify=tk.LEFT,
                fg="#006400"
            )
            detected_label.pack(padx=10, pady=10)
        
        # Variável para armazenar sindicato selecionado (ANTES do if para evitar bugs)
        selected_var = tk.StringVar(value=sindicato_detectado if sindicato_detectado else "")
        
        # Opções encontradas
        if todos_sindicatos:
            options_frame = tk.LabelFrame(main_frame, text="Outros Sindicatos Encontrados no PDF", font=("Arial", 10, "bold"))
            options_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
            
            # Scrollbar
            canvas = tk.Canvas(options_frame)
            scrollbar = tk.Scrollbar(options_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            for sind in todos_sindicatos:
                rb = tk.Radiobutton(
                    scrollable_frame,
                    text=sind,
                    variable=selected_var,
                    value=sind,
                    font=("Arial", 9),
                    wraplength=600,
                    justify=tk.LEFT
                )
                rb.pack(anchor=tk.W, padx=10, pady=5)
            
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Campo de edição manual
        edit_frame = tk.LabelFrame(main_frame, text="Ou Digite Manualmente", font=("Arial", 10, "bold"))
        edit_frame.pack(fill=tk.X, pady=(0, 15))
        
        edit_entry = tk.Entry(edit_frame, textvariable=selected_var, font=("Arial", 10))
        edit_entry.pack(fill=tk.X, padx=10, pady=10)
        
        # Resultado
        result = {"sindicato": sindicato_detectado if sindicato_detectado else "SINDICATO NÃO IDENTIFICADO"}
        
        def on_confirm():
            valor_selecionado = selected_var.get().strip()
            print(f"\n[DEBUG] Valor capturado do radiobutton/campo: '{valor_selecionado}'")
            
            if valor_selecionado and valor_selecionado != "SINDICATO NÃO IDENTIFICADO":
                result["sindicato"] = valor_selecionado
                print(f"[DEBUG] Sindicato confirmado: '{result['sindicato']}'")
            else:
                result["sindicato"] = sindicato_detectado if sindicato_detectado else "SINDICATO NÃO IDENTIFICADO"
                print(f"[DEBUG] Usando sindicato detectado: '{result['sindicato']}'")
            
            dialog.destroy()
        
        # Botões
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        confirm_btn = tk.Button(
            button_frame,
            text="✅ Confirmar",
            command=on_confirm,
            font=("Arial", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10
        )
        confirm_btn.pack(side=tk.RIGHT)
        
        # Aguardar usuário
        dialog.transient()
        dialog.grab_set()
        dialog.wait_window()
        
        return result["sindicato"]
    
    def _detectar_sindicato_empregado(self, texto: str) -> str:
        """Detecta sindicato dos empregados com múltiplos padrões"""
        
        # Padrão 1: "do outro lado" + SINDICATO (mais comum)
        padrao1 = r'(?:e|,)\s*do outro lado[,\s]+o?\s*(SINDICATO\s+DOS\s+(?:TRABALHADORES|ENFERMEIROS|EMPREGADOS|BANCÁRIOS|COMERCIÁRIOS).*?)(?:,\s*(?:sito|CNPJ|neste))'
        match1 = re.search(padrao1, texto, re.IGNORECASE | re.DOTALL)
        if match1:
            return ' '.join(match1.group(1).split())
        
        # Padrão 2: "representados pelo SINDICATO"
        padrao2 = r'representados pelo\s+(SINDICATO\s+DOS\s+(?:TRABALHADORES|ENFERMEIROS|EMPREGADOS|BANCÁRIOS|COMERCIÁRIOS).*?)(?:,\s*(?:com|na|para))'
        match2 = re.search(padrao2, texto, re.IGNORECASE | re.DOTALL)
        if match2:
            return ' '.join(match2.group(1).split())
        
        # Padrão 3: Segundo SINDICATO mencionado (fallback)
        padroes_sind = re.findall(
            r'(SINDICATO\s+DOS\s+(?:TRABALHADORES|ENFERMEIROS|EMPREGADOS|BANCÁRIOS|COMERCIÁRIOS)[A-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ\s]+?)(?=\s*[-—,]|\s+CNPJ|\s+sito)',
            texto,
            re.IGNORECASE
        )
        if len(padroes_sind) >= 2:
            return ' '.join(padroes_sind[1].split())
        
        return "SINDICATO NÃO IDENTIFICADO"
    
    def normalizar_sindicato(self, sindicato_bruto: str) -> str:
        """Normaliza o nome do sindicato"""
        sindicato = ' '.join(sindicato_bruto.split())
        sindicato = sindicato.upper()
        
        # Correções básicas
        correcoes = {
            r'\bDos\b': 'DOS',
            r'\bDo\b': 'DO',
            r'\bDas\b': 'DAS',
            r'\bDa\b': 'DA',
            r'\bEm\b': 'EM',
            r'SAUDE': 'SAÚDE',
            r'\bBAHTA\b': 'BAHIA',
        }
        
        for padrao, substituicao in correcoes.items():
            sindicato = re.sub(padrao, substituicao, sindicato, flags=re.IGNORECASE)
        
        return sindicato.strip()
    
    def identificar_sindicato_convencao(self) -> Tuple[str, str]:
        """Identifica o sindicato e o período da convenção"""
        print("🔍 Identificando sindicato e convenção...")
        
        linhas_iniciais = self.texto_completo[:8000]
        
        # Buscar convenção no topo
        padrao_conv_topo = r'CONVENÇÃO\s+COLETIVA\s+DE\s+TRABALHO\s+(\d{4}[-/]\d{4})'
        match_conv = re.search(padrao_conv_topo, linhas_iniciais, re.IGNORECASE)
        
        if match_conv:
            periodo = match_conv.group(1).replace('/', '-')
            self.convencao = periodo
            print(f"   ✓ Convenção encontrada: {self.convencao}")
        
        # Buscar sindicato com múltiplos padrões
        sindicato_detectado = self._detectar_sindicato_empregado(linhas_iniciais)
        
        if sindicato_detectado and sindicato_detectado != "SINDICATO NÃO IDENTIFICADO":
            self.sindicato = self.normalizar_sindicato(sindicato_detectado)
            print(f"   ✓ Sindicato detectado automaticamente")
        
        # Buscar todos os sindicatos mencionados no texto
        todos_sindicatos = self._buscar_todos_sindicatos(linhas_iniciais)
        
        # Permitir usuário escolher/editar sindicato
        # IMPORTANTE: Passar sindicato_detectado (não self.sindicato que pode estar vazio)
        sindicato_confirmado = self._confirmar_sindicato(sindicato_detectado, todos_sindicatos)
        print(f"\n[DEBUG] Sindicato retornado de _confirmar_sindicato: '{sindicato_confirmado}'")
        
        # Atualizar apenas se não for vazio ou "NÃO IDENTIFICADO"
        if sindicato_confirmado and sindicato_confirmado != "SINDICATO NÃO IDENTIFICADO":
            self.sindicato = sindicato_confirmado
            print(f"[DEBUG] self.sindicato atualizado para: '{self.sindicato}'")
        
        # Fallbacks
        if not self.convencao:
            nome_arquivo = Path(self.pdf_path).stem
            match_ano = re.search(r'(\d{4})[-_]?(\d{4})', nome_arquivo)
            if match_ano:
                ano1, ano2 = sorted(match_ano.groups())
                self.convencao = f"{ano1}-{ano2}"
        
        if not self.sindicato or self.sindicato == "SINDICATO NÃO IDENTIFICADO":
            self.sindicato = "SINDICATO NÃO IDENTIFICADO"
        if not self.convencao:
            self.convencao = "ANO NÃO IDENTIFICADO"
        
        print(f"   Sindicato: {self.sindicato[:80]}{'...' if len(self.sindicato) > 80 else ''}")
        print(f"   Convenção: {self.convencao}\n")
        
        return self.sindicato, self.convencao
    
    def normalizar_titulo_clausula(self, titulo: str) -> str:
        """Normaliza título da cláusula"""
        titulo = ' '.join(titulo.split())
        titulo = titulo.upper()
        titulo = re.sub(r'^CLAUSULA\s+', 'CLÁUSULA ', titulo)
        titulo = re.sub(r'\s*[-—]\s*', ' - ', titulo)
        titulo = re.sub(r'\s+', ' ', titulo)
        return titulo.strip()
    
    def extrair_clausulas(self) -> List[Dict[str, str]]:
        """Extrai cláusulas do texto"""
        print("📋 Extraindo cláusulas...")
        
        linhas = self.texto_completo.split('\n')
        clausulas_encontradas = []
        i = 0
        
        while i < len(linhas):
            linha = linhas[i].strip()
            
            if re.match(r'^CL[ÁA]USULA\s+', linha, re.IGNORECASE):
                titulo_clausula = linha
                inicio_conteudo = i + 1
                
                j = i + 1
                while j < len(linhas):
                    proxima_linha = linhas[j].strip()
                    if re.match(r'^CL[ÁA]USULA\s+', proxima_linha, re.IGNORECASE):
                        break
                    j += 1
                
                conteudo_linhas = linhas[inicio_conteudo:j]
                conteudo_completo = '\n'.join(conteudo_linhas).strip()
                conteudo_completo = self._limpar_conteudo(conteudo_completo)
                
                if conteudo_completo:
                    titulo_normalizado = self.normalizar_titulo_clausula(titulo_clausula)
                    
                    clausulas_encontradas.append({
                        'titulo': titulo_normalizado,
                        'conteudo': conteudo_completo
                    })
                
                i = j
            else:
                i += 1
        
        print(f"   Encontradas {len(clausulas_encontradas)} cláusulas")
        print()
        
        clausulas = []
        total = len(clausulas_encontradas)
        
        for idx, clausula_info in enumerate(clausulas_encontradas, 1):
            titulo = clausula_info['titulo']
            conteudo = clausula_info['conteudo']
            
            if idx % 5 == 0 or idx == total:
                print(f"   Processando cláusulas... {idx}/{total}")
            
            if self.usar_ia and conteudo:
                resumo = self._gerar_resumo_ia(titulo, conteudo)
            else:
                resumo = self._gerar_resumo_simples(conteudo)
            
            clausula_dict = {
                'Sindicato': self.sindicato,
                'Convenção': self.convencao,
                'Título da Cláusula': titulo,
                'Resumo': resumo,
                'Cláusula Completa': conteudo
            }
            
            clausulas.append(clausula_dict)
        
        self.clausulas = clausulas
        print(f"\n✓ Total de {len(clausulas)} cláusulas extraídas\n")
        return clausulas
    
    def _limpar_conteudo(self, texto: str) -> str:
        """Limpa conteúdo da cláusula"""
        texto = re.sub(r'\n{3,}', '\n\n', texto)
        linhas = texto.split('\n')
        linhas_limpas = []
        
        for linha in linhas:
            linha_strip = linha.strip()
            if len(linha_strip) > 2 and not re.match(r'^[\d\s\-–—_\.]+$', linha_strip):
                if not re.search(r'(?:Presidente|Diretor|Salvador)', linha_strip):
                    linhas_limpas.append(linha)
        
        texto_limpo = '\n'.join(linhas_limpas).strip()
        texto_limpo = re.sub(r' {2,}', ' ', texto_limpo)
        return texto_limpo
    
    def _gerar_resumo_simples(self, conteudo: str) -> str:
        """Gera resumo simples"""
        if len(conteudo) <= 150:
            return conteudo
        
        match_ponto = re.search(r'\.(?:\s|$)', conteudo[:300])
        if match_ponto:
            return conteudo[:match_ponto.end()].strip()
        
        return conteudo[:150].strip() + "..."
    
    def _gerar_resumo_ia(self, titulo: str, conteudo: str) -> str:
        """Gera resumo usando IA"""
        try:
            prompt = f"""Analise a seguinte cláusula de CCT e gere um resumo conciso em uma frase (máximo 200 caracteres).

Título: {titulo}
Conteúdo: {conteudo[:1500]}

Resumo:"""

            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "Você é especialista em direito trabalhista. Gere resumos concisos de cláusulas de CCTs."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=100
            )
            
            resumo = response.choices[0].message.content.strip().strip('"\'')
            if resumo and not resumo.endswith('.'):
                resumo += '.'
            
            return resumo
            
        except Exception as e:
            return self._gerar_resumo_simples(conteudo)
    
    def _limpar_para_csv(self, texto: str) -> str:
        """Limpa texto para CSV"""
        if not isinstance(texto, str):
            return str(texto)
        
        texto = texto.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
        texto = ' '.join(texto.split())
        texto = ''.join(char for char in texto if ord(char) >= 32 or char in '\t\n\r')
        
        return texto.strip()
    
    def salvar_csv(self, output_path: str) -> None:
        """Salva cláusulas em CSV"""
        print(f"💾 Salvando dados em CSV: {output_path}")
        
        if not self.clausulas:
            print("❌ Nenhuma cláusula para salvar!")
            return
        
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Sindicato', 'Convenção', 'Título da Cláusula', 'Resumo', 'Cláusula Completa']
                writer = csv.DictWriter(
                    csvfile, 
                    fieldnames=fieldnames,
                    quoting=csv.QUOTE_ALL,
                    escapechar='\\',
                    doublequote=True
                )
                
                writer.writeheader()
                
                clausulas_limpas = []
                for clausula in self.clausulas:
                    clausula_limpa = {}
                    for key, value in clausula.items():
                        clausula_limpa[key] = self._limpar_para_csv(value)
                    clausulas_limpas.append(clausula_limpa)
                
                writer.writerows(clausulas_limpas)
            
            print(f"✓ Arquivo CSV salvo com sucesso!")
            print(f"   Total de linhas: {len(self.clausulas)}")
            print(f"   Tamanho: {os.path.getsize(output_path) / 1024:.2f} KB\n")
            
        except Exception as e:
            print(f"❌ Erro ao salvar CSV: {e}")
            raise
    
    def processar(self, output_path: str, barra_progresso=None) -> None:
        """Executa processo completo"""
        print("\n" + "=" * 70)
        print("🚀 EXTRATOR DE DADOS DE CCTs - VERSÃO STANDALONE")
        print("=" * 70)
        
        if barra_progresso:
            barra_progresso.atualizar(10, "Extraindo texto do PDF...")
        self.extrair_texto_pdf_ocr()
        if barra_progresso:
            barra_progresso.atualizar(30, "Identificando sindicato e convenção...")
        self.identificar_sindicato_convencao()
        if barra_progresso:
            barra_progresso.atualizar(50, "Extraindo cláusulas...")
        self.extrair_clausulas()
        if barra_progresso:
            barra_progresso.atualizar(90, "Salvando CSV...")
        self.salvar_csv(output_path)
        
        if barra_progresso:
            barra_progresso.atualizar(100, "Processo concluído!")
        
        print("=" * 70)
        print("✅ PROCESSO CONCLUÍDO COM SUCESSO!")
        print("=" * 70)
        print()


def main():
    """Função principal"""
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  EXTRATOR DE DADOS DE CONVENÇÕES COLETIVAS DE TRABALHO (CCTs)  ".center(68) + "║")
    print("║" + "  Versão Standalone - Portátil  ".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    try:
        # Gerenciador de configurações
        config_manager = ConfigManager()
        
        # Verificar se é primeira execução
        if not config_manager.get_api_key() and not config_manager.config.get('configured'):
            print("👋 Primeira execução detectada!")
            print("   Vamos configurar o aplicativo...\n")
            
            dialog = ConfigDialog(config_manager)
            if not dialog.show():
                print("❌ Configuração cancelada.")
                return 1
            
            config_manager.config['configured'] = True
            config_manager.save_config()
        
        # Verificar Tesseract
        tesseract_path = config_manager.get_tesseract_path()
        if not tesseract_path:
            tesseract_path = find_tesseract()
            if tesseract_path:
                config_manager.set_tesseract_path(tesseract_path)
        
        if not tesseract_path or not os.path.exists(tesseract_path):
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            
            resposta = messagebox.askyesno(
                "Tesseract OCR não encontrado",
                "O Tesseract OCR não foi encontrado no sistema.\n\n"
                "Este programa requer o Tesseract para funcionar.\n\n"
                "Deseja abrir a página de download do Tesseract?"
            )
            
            if resposta:
                import webbrowser
                webbrowser.open("https://github.com/UB-Mannheim/tesseract/wiki")
            
            root.destroy()
            return 1
        
        # 1. Selecionar arquivo PDF
        print("📄 Selecione o arquivo PDF da CCT...")
        pdf_path = selecionar_pdf()
        
        if not pdf_path:
            print("❌ Nenhum arquivo selecionado. Operação cancelada.")
            return 1
        
        print(f"✓ Arquivo selecionado: {os.path.basename(pdf_path)}\n")
        
        # 2. Selecionar onde salvar CSV
        print("💾 Selecione onde salvar o arquivo CSV...")
        output_path = selecionar_csv_saida(pdf_path)
        
        if not output_path:
            print("❌ Nenhum local selecionado. Operação cancelada.")
            return 1
        
        print(f"✓ Será salvo em: {os.path.basename(output_path)}\n")
        
        # 3. Verificar se IA está disponível
        if config_manager.get_api_key():
            print("🤖 OpenAI configurada - Usando IA para gerar resumos\n")
        else:
            print("⚠️  OpenAI não configurada - Usando resumos simples\n")
        
        # 4. Processar com barra de progresso
        extrator = ExtratorCCT(pdf_path=pdf_path, config_manager=config_manager)
        
        # Criar barra de progresso
        barra = BarraProgresso("Extraindo Dados da CCT")
        barra.criar_janela()
        
        try:
            extrator.processar(output_path, barra_progresso=barra)
        finally:
            barra.fechar()
        
        # 5. Janela de confirmação
        print(f"📄 Arquivo gerado: {output_path}")
        print()
        
        acao = janela_confirmacao_csv(output_path, len(extrator.clausulas), extrator.convencao)
        
        if acao == "integrar":
            print("\n📊 Integrando com planilha mãe...")
            
            # Selecionar planilha mãe
            csv_mae = selecionar_planilha_mae()
            
            if csv_mae:
                # Integrar
                sucesso = integrar_com_planilha_mae(output_path, csv_mae)
                if sucesso:
                    print("✅ Integração concluída com sucesso!")
                else:
                    print("❌ Erro na integração.")
            else:
                print("❌ Nenhuma planilha mãe selecionada.")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n❌ Operação cancelada pelo usuário.")
        return 1
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        
        # Mostrar mensagem de erro
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        messagebox.showerror("Erro", f"Ocorreu um erro:\n\n{str(e)}")
        root.destroy()
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
