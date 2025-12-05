#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar executável do Extrator de CCTs
Usa PyInstaller para criar um executável standalone
"""

import os
import sys
import subprocess

def build_exe():
    """Gera executável com PyInstaller"""
    
    print("=" * 70)
    print("GERADOR DE EXECUTÁVEL - EXTRATOR DE CCTs")
    print("=" * 70)
    print()
    
    # Verificar se PyInstaller está instalado
    try:
        import PyInstaller
        print("✓ PyInstaller encontrado")
    except ImportError:
        print("❌ PyInstaller não encontrado!")
        print("   Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller instalado")
    
    print()
    
    # Parâmetros do PyInstaller
    params = [
        "pyinstaller",
        "--name=ExtratorCCT",
        "--onefile",  # Gera um único executável
        "--windowed",  # Sem console (comentar se quiser ver o console)
        "--icon=NONE",  # Adicione um ícone se tiver
        "--add-data=README_STANDALONE.md;.",  # Incluir README
        "--hidden-import=PIL._tkinter_finder",
        "--hidden-import=pytesseract",
        "--hidden-import=openai",
        "--collect-all=pytesseract",
        "--collect-all=PIL",
        "extrator_cct_standalone.py"
    ]
    
    print("🔨 Gerando executável...")
    print(f"   Comando: {' '.join(params)}")
    print()
    
    try:
        subprocess.check_call(params)
        print()
        print("=" * 70)
        print("✅ EXECUTÁVEL GERADO COM SUCESSO!")
        print("=" * 70)
        print()
        print("📁 Localização: dist/ExtratorCCT.exe")
        print()
        print("📝 Próximos passos:")
        print("   1. Teste o executável: dist/ExtratorCCT.exe")
        print("   2. Distribua o executável para outros computadores")
        print("   3. Certifique-se de que o Tesseract OCR está instalado")
        print()
        
    except subprocess.CalledProcessError as e:
        print()
        print("❌ ERRO ao gerar executável!")
        print(f"   {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(build_exe())
