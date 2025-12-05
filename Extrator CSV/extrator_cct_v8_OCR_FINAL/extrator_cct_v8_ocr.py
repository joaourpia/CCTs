#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrator de Dados de Convenções Coletivas de Trabalho (CCTs) - Versão 8 OCR
Autor: Manus AI
Descrição: Versão com Tesseract OCR para extração de texto de alta qualidade
"""

import os
import re
import csv
from pathlib import Path
from typing import List, Dict, Tuple
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io
from openai import OpenAI
import tkinter as tk
from tkinter import filedialog, messagebox

# Configuração do cliente OpenAI
try:
    client = OpenAI()
    IA_DISPONIVEL = True
except:
    IA_DISPONIVEL = False


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
    
    def __init__(self, pdf_path: str, usar_ia: bool = True):
        self.pdf_path = pdf_path
        self.usar_ia = usar_ia
        self.texto_completo = ""
        self.sindicato = ""
        self.convencao = ""
        self.clausulas = []
        
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
    
    def normalizar_sindicato(self, sindicato_bruto: str) -> str:
        """Normaliza o nome do sindicato"""
        sindicato = ' '.join(sindicato_bruto.split())
        
        # Correções básicas (Tesseract é muito melhor, precisa menos correções)
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
        
        sindicato = sindicato.upper()
        
        return sindicato.strip()
    
    def identificar_sindicato_convencao(self) -> Tuple[str, str]:
        """Identifica o sindicato e o período da convenção"""
        print("🔍 Identificando sindicato e convenção...")
        
        linhas_iniciais = self.texto_completo[:8000]
        
        # Buscar convenção PRIMEIRO (no topo do documento)
        padrao_conv_topo = r'CONVENÇÃO\s+COLETIVA\s+DE\s+TRABALHO\s+(\d{4}[-/]\d{4})'
        match_conv = re.search(padrao_conv_topo, linhas_iniciais, re.IGNORECASE)
        
        if match_conv:
            periodo = match_conv.group(1).replace('/', '-')
            self.convencao = periodo
            print(f"   ✓ Convenção encontrada no topo: {self.convencao}")
        
        # Buscar sindicato "do outro lado"
        padrao_empregado = r'do outro lado,?\s+o\s+(SINDICATO\s+DOS\s+TRABALHADORES.*?)(?:,\s+sito|,\s+CNPJ|,\s+neste)'
        match_empregado = re.search(padrao_empregado, linhas_iniciais, re.IGNORECASE | re.DOTALL)
        
        if match_empregado:
            sindicato_bruto = match_empregado.group(1).strip()
            self.sindicato = self.normalizar_sindicato(sindicato_bruto)
            print(f"   ✓ Sindicato encontrado ({len(self.sindicato)} caracteres)")
        
        # Fallback para convenção
        if not self.convencao:
            anos = re.findall(r'\b(20\d{2})\b', linhas_iniciais[:2000])
            if len(anos) >= 2:
                anos_unicos = []
                for ano in anos:
                    if ano not in anos_unicos:
                        anos_unicos.append(ano)
                    if len(anos_unicos) == 2:
                        break
                
                if len(anos_unicos) == 2:
                    ano1, ano2 = sorted(anos_unicos)
                    self.convencao = f"{ano1}-{ano2}"
        
        # Fallback para nome do arquivo
        if not self.convencao:
            nome_arquivo = Path(self.pdf_path).stem
            match_ano = re.search(r'(\d{4})[-_]?(\d{4})', nome_arquivo)
            if match_ano:
                ano1, ano2 = sorted(match_ano.groups())
                self.convencao = f"{ano1}-{ano2}"
        
        # Fallback final
        if not self.sindicato:
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
        
        # Garantir acentuação correta
        titulo = re.sub(r'^CLAUSULA\s+', 'CLÁUSULA ', titulo)
        
        # Normalizar números ordinais
        correcoes_ordinais = {
            r'\bPRIMEIRA\b': 'PRIMEIRA',
            r'\bSEGUNDA\b': 'SEGUNDA',
            r'\bTERCEIRA\b': 'TERCEIRA',
            r'\bQUARTA\b': 'QUARTA',
            r'\bQUINTA\b': 'QUINTA',
            r'\bSEXTA\b': 'SEXTA',
            r'\bSETIMA\b': 'SÉTIMA',
            r'\bOITAVA\b': 'OITAVA',
            r'\bNONA\b': 'NONA',
            r'\bDECIMA\b': 'DÉCIMA',
            r'\bVIGESIMA\b': 'VIGÉSIMA',
            r'\bTRIGESIMA\b': 'TRIGÉSIMA',
        }
        
        for padrao, substituicao in correcoes_ordinais.items():
            titulo = re.sub(padrao, substituicao, titulo)
        
        # Limpar pontuação
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
            
            # Padrão mais robusto para cláusulas
            if re.match(r'^CL[ÁA]USULA\s+', linha, re.IGNORECASE):
                titulo_clausula = linha
                inicio_conteudo = i + 1
                
                # Buscar próxima cláusula
                j = i + 1
                while j < len(linhas):
                    proxima_linha = linhas[j].strip()
                    if re.match(r'^CL[ÁA]USULA\s+', proxima_linha, re.IGNORECASE):
                        break
                    j += 1
                
                # Extrair conteúdo
                conteudo_linhas = linhas[inicio_conteudo:j]
                conteudo_completo = '\n'.join(conteudo_linhas).strip()
                
                # Limpar conteúdo
                conteudo_completo = self._limpar_conteudo(conteudo_completo)
                
                if conteudo_completo:
                    titulo_normalizado = self.normalizar_titulo_clausula(titulo_clausula)
                    
                    clausulas_encontradas.append({
                        'titulo': titulo_normalizado,
                        'conteudo': conteudo_completo,
                        'linha_inicio': i
                    })
                
                i = j
            else:
                i += 1
        
        print(f"   Encontradas {len(clausulas_encontradas)} cláusulas")
        print()
        
        # Processar cada cláusula
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
        # Remove quebras de linha excessivas
        texto = re.sub(r'\n{3,}', '\n\n', texto)
        
        # Remove linhas com apenas números/símbolos
        linhas = texto.split('\n')
        linhas_limpas = []
        
        for linha in linhas:
            linha_strip = linha.strip()
            # Mantém linhas com conteúdo significativo
            if len(linha_strip) > 2 and not re.match(r'^[\d\s\-–—_\.]+$', linha_strip):
                # Remove assinaturas e cabeçalhos
                if not re.search(r'(?:Presidente|Diretor|Salvador|^\s*[A-Z][a-z]+\s+[A-Z][a-z]+\s*$)', linha_strip):
                    linhas_limpas.append(linha)
        
        texto_limpo = '\n'.join(linhas_limpas).strip()
        
        # Remove espaços múltiplos
        texto_limpo = re.sub(r' {2,}', ' ', texto_limpo)
        
        return texto_limpo
    
    def _gerar_resumo_simples(self, conteudo: str) -> str:
        """Gera resumo simples"""
        if len(conteudo) <= 150:
            return conteudo
        
        # Pega primeira frase
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

            response = client.chat.completions.create(
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
            print(f"   ⚠ Erro ao gerar resumo com IA: {e}")
            return self._gerar_resumo_simples(conteudo)
    
    def _limpar_para_csv(self, texto: str) -> str:
        """Limpa texto para CSV"""
        if not isinstance(texto, str):
            return str(texto)
        
        # Remove quebras de linha
        texto = texto.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
        
        # Remove espaços múltiplos
        texto = ' '.join(texto.split())
        
        # Remove caracteres de controle
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
    
    def processar(self, output_path: str) -> None:
        """Executa processo completo"""
        print("\n" + "=" * 70)
        print("🚀 EXTRATOR DE DADOS DE CCTs - VERSÃO 8 OCR")
        print("=" * 70)
        
        self.extrair_texto_pdf_ocr()
        self.identificar_sindicato_convencao()
        self.extrair_clausulas()
        self.salvar_csv(output_path)
        
        print("=" * 70)
        print("✅ PROCESSO CONCLUÍDO COM SUCESSO!")
        print("=" * 70)
        print()


def main():
    """Função principal com interface gráfica"""
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  EXTRATOR DE DADOS DE CONVENÇÕES COLETIVAS DE TRABALHO (CCTs)  ".center(68) + "║")
    print("║" + "  Versão 8 - OCR de Alta Qualidade  ".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    try:
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
        if IA_DISPONIVEL:
            print("🤖 OpenAI configurada - Usando IA para gerar resumos\n")
            usar_ia = True
        else:
            print("⚠️  OpenAI não disponível - Usando resumos simples\n")
            usar_ia = False
        
        # 4. Processar
        extrator = ExtratorCCT(pdf_path=pdf_path, usar_ia=usar_ia)
        extrator.processar(output_path)
        
        # 5. Mensagem final
        print(f"📄 Arquivo gerado: {output_path}")
        print()
        
        # Mostrar mensagem de sucesso
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        messagebox.showinfo(
            "Sucesso!",
            f"CSV gerado com sucesso!\n\n"
            f"Arquivo: {os.path.basename(output_path)}\n"
            f"Cláusulas extraídas: {len(extrator.clausulas)}\n"
            f"Convenção: {extrator.convencao}"
        )
        root.destroy()
        
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
    exit(main())
