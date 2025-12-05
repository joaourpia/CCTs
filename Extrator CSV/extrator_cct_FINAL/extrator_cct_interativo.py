#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrator de Dados de Convenções Coletivas de Trabalho (CCTs) - Versão Interativa
Autor: Manus AI
Descrição: Versão com interface interativa e melhor detecção de sindicatos longos
"""

import os
import re
import csv
import glob
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import fitz  # PyMuPDF
from openai import OpenAI

# Configuração do cliente OpenAI (usa variáveis de ambiente pré-configuradas)
try:
    client = OpenAI()
    IA_DISPONIVEL = True
except:
    IA_DISPONIVEL = False


def listar_pdfs(diretorio="."):
    """Lista todos os arquivos PDF no diretório"""
    pdfs = glob.glob(os.path.join(diretorio, "*.pdf"))
    return sorted(pdfs)


def selecionar_arquivo_pdf():
    """Interface interativa para selecionar arquivo PDF"""
    print("=" * 70)
    print("📄 SELEÇÃO DE ARQUIVO PDF")
    print("=" * 70)
    print()
    
    # Listar PDFs no diretório atual
    pdfs = listar_pdfs()
    
    if pdfs:
        print("PDFs encontrados no diretório atual:")
        for i, pdf in enumerate(pdfs, 1):
            nome = os.path.basename(pdf)
            tamanho = os.path.getsize(pdf) / 1024
            print(f"  {i}. {nome} ({tamanho:.1f} KB)")
        print()
        
        while True:
            escolha = input("Digite o número do PDF ou o caminho completo: ").strip()
            
            # Verifica se é um número
            if escolha.isdigit():
                idx = int(escolha) - 1
                if 0 <= idx < len(pdfs):
                    return pdfs[idx]
                else:
                    print(f"❌ Número inválido! Digite entre 1 e {len(pdfs)}")
            # Verifica se é um caminho
            elif os.path.exists(escolha) and escolha.lower().endswith('.pdf'):
                return escolha
            else:
                print("❌ Arquivo não encontrado! Tente novamente.")
    else:
        print("Nenhum PDF encontrado no diretório atual.")
        print()
        while True:
            caminho = input("Digite o caminho completo do arquivo PDF: ").strip()
            if os.path.exists(caminho) and caminho.lower().endswith('.pdf'):
                return caminho
            else:
                print("❌ Arquivo não encontrado! Tente novamente.")


def solicitar_nome_saida(pdf_path):
    """Interface interativa para definir nome do arquivo de saída"""
    print()
    print("=" * 70)
    print("💾 NOME DO ARQUIVO DE SAÍDA")
    print("=" * 70)
    print()
    
    # Sugerir nome baseado no PDF
    nome_base = Path(pdf_path).stem
    sugestao = f"{nome_base}_extraido.csv"
    
    print(f"Sugestão: {sugestao}")
    print()
    
    escolha = input("Pressione ENTER para usar a sugestão ou digite outro nome: ").strip()
    
    if not escolha:
        return sugestao
    
    # Garante extensão .csv
    if not escolha.lower().endswith('.csv'):
        escolha += '.csv'
    
    return escolha


def perguntar_usar_ia():
    """Pergunta se deve usar IA para gerar resumos"""
    print()
    print("=" * 70)
    print("🤖 GERAÇÃO DE RESUMOS")
    print("=" * 70)
    print()
    
    if not IA_DISPONIVEL:
        print("⚠️  IA não disponível (OpenAI API não configurada)")
        print("   Resumos serão gerados de forma simples.")
        input("\nPressione ENTER para continuar...")
        return False
    
    print("Deseja usar IA (GPT) para gerar resumos automáticos?")
    print("  [S] Sim - Resumos mais elaborados (mais lento, requer API key)")
    print("  [N] Não - Resumos simples (mais rápido, gratuito)")
    print()
    
    while True:
        escolha = input("Sua escolha [S/N]: ").strip().upper()
        if escolha in ['S', 'SIM', 'Y', 'YES']:
            return True
        elif escolha in ['N', 'NAO', 'NÃO', 'NO']:
            return False
        else:
            print("❌ Opção inválida! Digite S ou N")


class ExtratorCCT:
    """Classe para extrair dados de PDFs de Convenções Coletivas de Trabalho"""
    
    def __init__(self, pdf_path: str, usar_ia: bool = True, modelo: str = "gpt-4.1-mini"):
        self.pdf_path = pdf_path
        self.usar_ia = usar_ia
        self.modelo = modelo
        self.texto_completo = ""
        self.sindicato = ""
        self.convencao = ""
        self.clausulas = []
        
    def extrair_texto_pdf(self) -> str:
        """Extrai texto do PDF usando PyMuPDF"""
        print(f"\n📄 Extraindo texto do PDF...")
        texto_completo = []
        
        try:
            doc = fitz.open(self.pdf_path)
            total_paginas = len(doc)
            
            for i, page in enumerate(doc, 1):
                texto = page.get_text()
                if texto:
                    texto_completo.append(texto)
                    # Mostra progresso a cada 5 páginas ou na última
                    if i % 5 == 0 or i == total_paginas:
                        print(f"   Processando... {i}/{total_paginas} páginas")
            
            doc.close()
            
            self.texto_completo = "\n".join(texto_completo)
            print(f"✓ Extração concluída: {len(self.texto_completo)} caracteres\n")
            return self.texto_completo
            
        except Exception as e:
            print(f"❌ Erro ao extrair texto do PDF: {e}")
            raise
    
    def normalizar_sindicato(self, sindicato_bruto: str) -> str:
        """Normaliza o nome do sindicato corrigindo erros de OCR"""
        # Remove quebras de linha
        sindicato = ' '.join(sindicato_bruto.split())
        
        # Correções específicas de OCR
        correcoes = {
            # Sindicato
            r'[sS][lI1][NnMm][DdOo][lI1tT][cCGg][AaÀá][TtÍí][OoQq0]': 'SINDICATO',
            
            # Preposições
            r'\bDos\b': 'DOS',
            r'\bDo\b': 'DO',
            r'\bDas\b': 'DAS',
            r'\bDa\b': 'DA',
            r'\bEm\b': 'EM',
            
            # Trabalhadores (com hífen indevido)
            r'TRABAI-HADORES': 'TRABALHADORES',
            r'TRABALHA-DORES': 'TRABALHADORES',
            
            # Médicos
            r'[MmNn][ÉéEe][DdOo][tTíÍiI1][cCGg][oOQq0][sS]': 'MÉDICOS',
            
            # Entidades
            r'ENT\|DADES': 'ENTIDADES',
            r'ENTLDADES': 'ENTIDADES',
            
            # Estabelecimentos
            r'ESÍABELECIMENTOS': 'ESTABELECIMENTOS',
            r'ESTABELEC[IilL1]MENTOS': 'ESTABELECIMENTOS',
            
            # Serviços
            r'SERVIçOS': 'SERVIÇOS',
            r'SERVICOS': 'SERVIÇOS',
            
            # Beneficentes
            r'BENEFLCENTES': 'BENEFICENTES',
            
            # Saúde
            r'SAÚDE': 'SAÚDE',
            r'SAUDE': 'SAÚDE',
            
            # Estados
            r'\bBAHTA\b': 'BAHIA',
            
            # Siglas
            r'S\|NDIMED': 'SINDIMED',
            r'S\|ND[IilL1]MED': 'SINDIMED',
            r'S\|NDISAÚDE': 'SINDISAÚDE',
            r'S\|NDISAUDE': 'SINDISAÚDE',
            r'SINDISAUDE': 'SINDISAÚDE',
        }
        
        for padrao, substituicao in correcoes.items():
            sindicato = re.sub(padrao, substituicao, sindicato, flags=re.IGNORECASE)
        
        # Capitaliza
        sindicato = sindicato.upper()
        
        # Correções finais
        sindicato = sindicato.replace('SLNDICATO', 'SINDICATO')
        sindicato = sindicato.replace('SLNDLCATO', 'SINDICATO')
        
        return sindicato.strip()
    
    def identificar_sindicato_convencao(self) -> Tuple[str, str]:
        """Identifica o sindicato DOS EMPREGADOS e o período da convenção"""
        print("🔍 Identificando sindicato e convenção...")
        
        linhas_iniciais = self.texto_completo[:5000]  # Aumentado para 5000 caracteres
        
        # Estratégia 1: Buscar "do outro lado" (sindicato dos empregados)
        # Padrão mais flexível para capturar sindicatos longos
        padrao_empregado = r'do outro lado,?\s+o\s+((?:SINDICATO|[Ss][lI1][NnMm][DdOo][lI1tT][cCGg][AaÀá][TtÍí][OoQq0]).*?)(?:,\s+sito|,\s+CNPJ|,\s+neste)'
        match_empregado = re.search(padrao_empregado, linhas_iniciais, re.IGNORECASE | re.DOTALL)
        
        if match_empregado:
            sindicato_bruto = match_empregado.group(1).strip()
            self.sindicato = self.normalizar_sindicato(sindicato_bruto)
            print(f"   ✓ Sindicato encontrado ({len(self.sindicato)} caracteres)")
        
        # Estratégia 2: Buscar por siglas conhecidas (SINDIMED, SINDISAÚDE, etc.)
        if not self.sindicato:
            siglas = ['SINDIMED', 'SINDISAÚDE', 'SINDISAUDE', 'S\\|NDIMED', 'S\\|NDISAÚDE']
            for sigla in siglas:
                padrao = f'((?:SINDICATO|[Ss][lI1][NnMm][DdOo][lI1tT][cCGg][AaÀá][TtÍí][OoQq0]).*?{sigla})'
                match = re.search(padrao, linhas_iniciais, re.IGNORECASE | re.DOTALL)
                if match:
                    sindicato_bruto = match.group(1)
                    # Limita a 300 caracteres para evitar capturar texto extra
                    if len(sindicato_bruto) < 300:
                        self.sindicato = self.normalizar_sindicato(sindicato_bruto)
                        print(f"   ✓ Sindicato encontrado via sigla ({len(self.sindicato)} caracteres)")
                        break
        
        # Padrão para período/ano da convenção
        padrao_periodo = r'(?:CONVENÇÃO\s+COLETIVA.*?)?(\d{4}[-/tl_]\d{4})'
        match_periodo = re.search(padrao_periodo, linhas_iniciais, re.IGNORECASE)
        
        if match_periodo:
            periodo_bruto = match_periodo.group(1)
            self.convencao = periodo_bruto.replace('/', '-').replace('t', '-').replace('l', '-').replace('_', '-')
        else:
            # Buscar anos separados
            padrao_ano = r'(\d{4})'
            anos = re.findall(padrao_ano, linhas_iniciais)
            if len(anos) >= 2:
                self.convencao = f"{anos[0]}-{anos[1]}"
            elif len(anos) == 1:
                self.convencao = anos[0]
        
        # Fallback
        if not self.sindicato:
            self.sindicato = "SINDICATO NÃO IDENTIFICADO"
        if not self.convencao:
            # Tenta extrair do nome do arquivo
            nome_arquivo = Path(self.pdf_path).stem
            match_ano = re.search(r'(\d{4}[-_]?\d{4})', nome_arquivo)
            if match_ano:
                self.convencao = match_ano.group(1).replace('_', '-')
            else:
                self.convencao = "ANO NÃO IDENTIFICADO"
        
        print(f"   Sindicato: {self.sindicato[:80]}{'...' if len(self.sindicato) > 80 else ''}")
        print(f"   Convenção: {self.convencao}\n")
        
        return self.sindicato, self.convencao
    
    def limpar_artefatos(self, texto: str) -> str:
        """Remove artefatos e caracteres estranhos do texto"""
        linhas = texto.split('\n')
        linhas_limpas = []
        
        for linha in linhas:
            linha_strip = linha.strip()
            
            if linha_strip and not re.match(r'^[A-Z],\w+$', linha_strip):
                if linha_strip not in ['w', '«', '»', '4-', '/-', '.0', '141', 'l']:
                    if not re.match(r'^\d+-?$', linha_strip):
                        if len(linha_strip) > 1 or linha_strip.isalnum():
                            linhas_limpas.append(linha)
        
        texto_limpo = '\n'.join(linhas_limpas)
        texto_limpo = re.sub(r'\n{3,}', '\n\n', texto_limpo)
        texto_limpo = re.sub(r' {2,}', ' ', texto_limpo)
        
        return texto_limpo
    
    def corrigir_ocr_texto(self, texto: str) -> str:
        """Corrige erros comuns de OCR no texto"""
        correcoes_ocr = {
            # Datas
            r'\babrill?(\d{4})\b': r'abril/\1',
            r'\bmaiol?(\d{4})\b': r'maio/\1',
            r'\bjunhol?(\d{4})\b': r'junho/\1',
            r'\bjulhol?(\d{4})\b': r'julho/\1',
            r'\bagostol?(\d{4})\b': r'agosto/\1',
            r'\bsetemb?rol?(\d{4})\b': r'setembro/\1',
            r'\boutubl?rol?(\d{4})\b': r'outubro/\1',
            r'\bnovembl?rol?(\d{4})\b': r'novembro/\1',
            r'\bdezembl?rol?(\d{4})\b': r'dezembro/\1',
            r'\bjaneirl?ol?(\d{4})\b': r'janeiro/\1',
            r'\bfevereirl?ol?(\d{4})\b': r'fevereiro/\1',
            r'\bmarçol?(\d{4})\b': r'março/\1',
            r'/2O(\d{2})\b': r'/20\1',
            r'\b2O(\d{2})\b': r'20\1',
            r'\bl2(\d{3})\b': r'1/2\1',
            
            # Palavras
            r'\bíorma\b': 'forma',
            r'\bperÍodo\b': 'período',
            r'\btrânsferência\b': 'transferência',
            r'\bessês\b': 'esses',
            
            # Formatação
            r'\s+([,\.;:!?])': r'\1',
            r'\s{2,}': ' ',
        }
        
        texto_corrigido = texto
        for padrao, substituicao in correcoes_ocr.items():
            texto_corrigido = re.sub(padrao, substituicao, texto_corrigido, flags=re.IGNORECASE)
        
        return texto_corrigido
    
    def normalizar_titulo_clausula(self, titulo: str) -> str:
        """Normaliza o título da cláusula"""
        titulo = ' '.join(titulo.split())
        
        correcoes = {
            r'^CLAUSULA\s+': 'CLÁUSULA ',
            r'^clausula\s+': 'CLÁUSULA ',
            r'^CúUSULA\s+': 'CLÁUSULA ',
            r'^cúUSULA\s+': 'CLÁUSULA ',
            r'\bOUARTA\b': 'QUARTA',
            r'\boITAVA\b': 'OITAVA',
            r'\bSETIMA\b': 'SÉTIMA',
            r'\bDECIMA\b': 'DÉCIMA',
            r'\bVIGESIMA\b': 'VIGÉSIMA',
            r'\bTRIGESIMA\b': 'TRIGÉSIMA',
        }
        
        for padrao, substituicao in correcoes.items():
            titulo = re.sub(padrao, substituicao, titulo, flags=re.IGNORECASE)
        
        titulo = re.sub(r'\s*\.\s*-', ' -', titulo)
        titulo = titulo.upper()
        
        return titulo.strip()
    
    def extrair_clausulas(self) -> List[Dict[str, str]]:
        """Extrai todas as cláusulas do texto"""
        print("📋 Extraindo cláusulas...")
        
        linhas = self.texto_completo.split('\n')
        clausulas_encontradas = []
        i = 0
        
        while i < len(linhas):
            linha = linhas[i].strip()
            
            if re.match(r'^(?:CL[ÁAÚúaáu]USULA|cl[áaúu]usula|C[úáaU]USULA|c[úáau]usula)\s+', linha, re.IGNORECASE):
                titulo_clausula = linha
                inicio_conteudo = i + 1
                
                j = i + 1
                while j < len(linhas):
                    proxima_linha = linhas[j].strip()
                    if re.match(r'^(?:CL[ÁAÚúaáu]USULA|cl[áaúu]usula|C[úáaU]USULA|c[úáau]usula)\s+', proxima_linha, re.IGNORECASE):
                        break
                    j += 1
                
                conteudo_linhas = linhas[inicio_conteudo:j]
                conteudo_completo = '\n'.join(conteudo_linhas).strip()
                conteudo_completo = self.limpar_artefatos(conteudo_completo)
                conteudo_completo = self._limpar_conteudo(conteudo_completo)
                conteudo_completo = self.corrigir_ocr_texto(conteudo_completo)
                
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
        
        # Processa cada cláusula
        clausulas = []
        total = len(clausulas_encontradas)
        
        for idx, clausula_info in enumerate(clausulas_encontradas, 1):
            titulo = clausula_info['titulo']
            conteudo = clausula_info['conteudo']
            
            # Mostra progresso
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
        """Remove ruídos do conteúdo"""
        texto = re.sub(r'\n{3,}', '\n\n', texto)
        linhas = texto.split('\n')
        linhas_limpas = []
        
        for linha in linhas:
            linha_strip = linha.strip()
            if len(linha_strip) > 2 and not re.match(r'^[\d\s\-–—_\.]+$', linha_strip):
                if not re.search(r'(?:Presidente|Diretor|Salvador,?\s+\d|^\s*[A-Z][a-z]+\s+[A-Z][a-z]+\s*$|^\d{10,}$)', linha_strip):
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

            response = client.chat.completions.create(
                model=self.modelo,
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
        """Salva as cláusulas em CSV"""
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
        """Executa o processo completo"""
        print("\n" + "=" * 70)
        print("🚀 EXTRATOR DE DADOS DE CCTs - VERSÃO INTERATIVA")
        print("=" * 70)
        
        self.extrair_texto_pdf()
        self.identificar_sindicato_convencao()
        self.extrair_clausulas()
        self.salvar_csv(output_path)
        
        print("=" * 70)
        print("✅ PROCESSO CONCLUÍDO COM SUCESSO!")
        print("=" * 70)
        print()


def main():
    """Função principal com interface interativa"""
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  EXTRATOR DE DADOS DE CONVENÇÕES COLETIVAS DE TRABALHO (CCTs)  ".center(68) + "║")
    print("║" + "  Versão Interativa - by Manus AI  ".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    try:
        # 1. Selecionar arquivo PDF
        pdf_path = selecionar_arquivo_pdf()
        
        # 2. Definir nome do arquivo de saída
        output_path = solicitar_nome_saida(pdf_path)
        
        # 3. Perguntar sobre uso de IA
        usar_ia = perguntar_usar_ia()
        
        # 4. Processar
        extrator = ExtratorCCT(pdf_path=pdf_path, usar_ia=usar_ia)
        extrator.processar(output_path)
        
        # 5. Mensagem final
        print(f"📄 Arquivo gerado: {output_path}")
        print()
        input("Pressione ENTER para sair...")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n❌ Operação cancelada pelo usuário.")
        return 1
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        input("\nPressione ENTER para sair...")
        return 1


if __name__ == "__main__":
    exit(main())
