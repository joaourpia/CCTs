#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrator de Dados de Convenções Coletivas de Trabalho (CCTs) - Versão 6
Autor: Manus AI
Descrição: Versão com PyMuPDF, normalização completa do sindicato e limpeza rigorosa de artefatos
"""

import os
import re
import csv
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import fitz  # PyMuPDF
from openai import OpenAI

# Configuração do cliente OpenAI (usa variáveis de ambiente pré-configuradas)
client = OpenAI()


class ExtratorCCT:
    """Classe para extrair dados de PDFs de Convenções Coletivas de Trabalho"""
    
    def __init__(self, pdf_path: str, usar_ia: bool = True, modelo: str = "gpt-4.1-mini"):
        """
        Inicializa o extrator
        
        Args:
            pdf_path: Caminho para o arquivo PDF
            usar_ia: Se True, usa IA para gerar resumos automáticos
            modelo: Modelo de IA a ser usado (gpt-4.1-mini, gpt-4.1-nano, gemini-2.5-flash)
        """
        self.pdf_path = pdf_path
        self.usar_ia = usar_ia
        self.modelo = modelo
        self.texto_completo = ""
        self.sindicato = ""
        self.convencao = ""
        self.clausulas = []
        
    def extrair_texto_pdf(self) -> str:
        """
        Extrai texto do PDF usando PyMuPDF (melhor qualidade)
        
        Returns:
            Texto completo extraído do PDF
        """
        print(f"📄 Extraindo texto do PDF: {self.pdf_path}")
        texto_completo = []
        
        try:
            doc = fitz.open(self.pdf_path)
            
            for i, page in enumerate(doc, 1):
                texto = page.get_text()
                if texto:
                    texto_completo.append(texto)
                    print(f"   ✓ Página {i}/{len(doc)} extraída")
                else:
                    print(f"   ⚠ Página {i}/{len(doc)} sem texto extraível")
            
            doc.close()
            
            self.texto_completo = "\n".join(texto_completo)
            print(f"✓ Extração concluída: {len(self.texto_completo)} caracteres\n")
            return self.texto_completo
            
        except Exception as e:
            print(f"❌ Erro ao extrair texto do PDF: {e}")
            raise
    
    def normalizar_sindicato(self, sindicato_bruto: str) -> str:
        """
        Normaliza o nome do sindicato corrigindo erros de OCR
        
        Args:
            sindicato_bruto: Nome do sindicato com erros de OCR
            
        Returns:
            Nome normalizado
        """
        # Remove quebras de linha
        sindicato = ' '.join(sindicato_bruto.split())
        
        # Correções específicas de OCR no nome do sindicato
        correcoes_sindicato = {
            # Correção de "slNDlcATo" para "SlNDlCATO"
            r'[sS][lI1][NnMm][DdOo][lI1][cCGg][AaÀá][TtÍí][OoQq0]': 'SlNDlCATO',
            
            # Correção de "Dos" para "DOS"
            r'\bDos\b': 'DOS',
            r'\bDo\b': 'DO',
            
            # Correção de "MÉDtcos" para "MÉDICOS"
            r'[MmNn][ÉéEe][DdOo][tTíÍiI1][cCGg][oOQq0][sS]': 'MÉDICOS',
            
            # Correção de "BAHTA" para "BAHIA"
            r'\bBAHTA\b': 'BAHIA',
            
            # Correção de "S|NDIMED" para "SINDIMED"
            r'S\|NDIMED': 'SINDIMED',
            r'S\|ND[IilL1]MED': 'SINDIMED',
        }
        
        for padrao, substituicao in correcoes_sindicato.items():
            sindicato = re.sub(padrao, substituicao, sindicato)
        
        # Garante capitalização correta de palavras-chave
        sindicato = sindicato.upper()
        
        # Correções finais
        sindicato = sindicato.replace('SLNDICATO', 'SINDICATO')
        sindicato = sindicato.replace('SLNDLCATO', 'SINDICATO')
        
        return sindicato.strip()
    
    def identificar_sindicato_convencao(self) -> Tuple[str, str]:
        """
        Identifica o sindicato DOS EMPREGADOS e o período da convenção no texto
        
        Returns:
            Tupla (sindicato, convenção)
        """
        print("🔍 Identificando sindicato e convenção...")
        
        linhas_iniciais = self.texto_completo[:3000]
        
        # Estratégia 1: Buscar sindicato dos empregados no cabeçalho
        padrao_empregado = r'(?:do outro lado|e,?\s+do outro lado)\s+[oa]\s+([Ss][lI1][NnMm][DdOo][lI1][cCGg][AaÀá][TtÍí][OoQq0].*?(?:SINDIMED|S\|NDIMED)).*?(?:,\s+sito|,\s+CNPJ|,\s+neste)'
        match_empregado = re.search(padrao_empregado, linhas_iniciais, re.IGNORECASE | re.DOTALL)
        
        if match_empregado:
            sindicato_bruto = match_empregado.group(1).strip()
            # Normaliza o sindicato corrigindo erros de OCR
            self.sindicato = self.normalizar_sindicato(sindicato_bruto)
            print(f"   ✓ Sindicato encontrado e normalizado")
        
        # Estratégia 2: Buscar apenas SINDIMED com contexto
        if not self.sindicato:
            padrao_sindimed = r'([Ss][lI1][NnMm][DdOo][lI1][cCGg][AaÀá][TtÍí][OoQq0]\s+[DdOo][OoQq0][Ss]\s+[MmNn][ÉéEe][DdOo][tTíÍiI1][cCGg][oOQq0][sS].*?(?:SINDIMED|S\|NDIMED))'
            match_sindimed = re.search(padrao_sindimed, linhas_iniciais)
            
            if match_sindimed:
                sindicato_bruto = match_sindimed.group(1)
                self.sindicato = self.normalizar_sindicato(sindicato_bruto)
                print(f"   ✓ Sindicato encontrado e normalizado")
        
        # Estratégia 3: Buscar no corpo do texto (fallback)
        if not self.sindicato:
            padrao_corpo = r'(?:representados pelo|pelo)\s+(Sindicato\s+dos?\s+[A-ZÀ-ÿ\s]+?(?:SINDIMED|[-–]\s*SINDIMED))'
            match_corpo = re.search(padrao_corpo, linhas_iniciais, re.IGNORECASE)
            
            if match_corpo:
                sindicato_bruto = match_corpo.group(1).strip()
                self.sindicato = self.normalizar_sindicato(sindicato_bruto)
                print(f"   ✓ Sindicato encontrado (fallback)")
        
        # Padrão para período/ano da convenção
        padrao_periodo = r'(?:CONVENÇÃO\s+COLETIVA.*?)?(\d{4}[-/tl]\d{4})'
        match_periodo = re.search(padrao_periodo, linhas_iniciais, re.IGNORECASE)
        
        if match_periodo:
            periodo_bruto = match_periodo.group(1)
            # Normaliza separadores
            self.convencao = periodo_bruto.replace('/', '-').replace('t', '-').replace('l', '-')
        else:
            padrao_ano = r'(\d{4})'
            anos = re.findall(padrao_ano, linhas_iniciais)
            if len(anos) >= 2:
                self.convencao = f"{anos[0]}-{anos[1]}"
            elif len(anos) == 1:
                self.convencao = anos[0]
        
        # Fallback: usa nome do arquivo
        if not self.sindicato or not self.convencao:
            nome_arquivo = Path(self.pdf_path).stem
            if not self.convencao:
                match_ano_arquivo = re.search(r'(\d{4}[-/]?\d{4})', nome_arquivo)
                if match_ano_arquivo:
                    self.convencao = match_ano_arquivo.group(1).replace('/', '-')
        
        if not self.sindicato:
            self.sindicato = "SINDICATO NÃO IDENTIFICADO"
        if not self.convencao:
            self.convencao = "ANO NÃO IDENTIFICADO"
        
        print(f"   Sindicato: {self.sindicato}")
        print(f"   Convenção: {self.convencao}\n")
        
        return self.sindicato, self.convencao
    
    def limpar_artefatos(self, texto: str) -> str:
        """
        Remove artefatos e caracteres estranhos do texto extraído
        
        Args:
            texto: Texto com possíveis artefatos
            
        Returns:
            Texto limpo
        """
        # Remove linhas com apenas 1-3 caracteres isolados (artefatos comuns)
        linhas = texto.split('\n')
        linhas_limpas = []
        
        for linha in linhas:
            linha_strip = linha.strip()
            
            # Ignora linhas que são claramente artefatos
            if linha_strip and not re.match(r'^[A-Z],\w+$', linha_strip):  # Remove "A,l"
                if linha_strip not in ['w', '«', '»', '4-', '/-', '.0', '141']:  # Remove artefatos conhecidos
                    if not re.match(r'^\d+-?$', linha_strip):  # Remove números isolados com hífen
                        if len(linha_strip) > 1 or linha_strip.isalnum():  # Mantém apenas se > 1 char ou alfanumérico
                            linhas_limpas.append(linha)
        
        texto_limpo = '\n'.join(linhas_limpas)
        
        # Remove múltiplas quebras de linha
        texto_limpo = re.sub(r'\n{3,}', '\n\n', texto_limpo)
        
        # Remove espaços múltiplos
        texto_limpo = re.sub(r' {2,}', ' ', texto_limpo)
        
        return texto_limpo
    
    def corrigir_ocr_texto(self, texto: str) -> str:
        """
        Corrige erros comuns de OCR no texto extraído
        
        Args:
            texto: Texto com possíveis erros de OCR
            
        Returns:
            Texto corrigido
        """
        # Dicionário de correções de OCR comuns
        correcoes_ocr = {
            # Correção de datas mal formatadas
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
            
            # Correção de datas com caracteres estranhos
            r'\bmaiot2O2\'': 'maio/2025',
            r'\bjulhol2025': 'julho/2025',
            r'\bagosto/2O25': 'agosto/2025',
            r'\bsetembro/2O25': 'setembro/2025',
            r'\boutubro/2O25': 'outubro/2025',
            
            # Correção de anos com O em vez de 0
            r'/2O(\d{2})\b': r'/20\1',
            r'\b2O(\d{2})\b': r'20\1',
            
            # Correção de números com l em vez de 1
            r'\bl2(\d{3})\b': r'1/2\1',
            
            # Correção de "íorma" para "forma"
            r'\bíorma\b': 'forma',
            
            # Correção de "perÍodo" para "período"
            r'\bperÍodo\b': 'período',
            
            # Correção de "trânsferência" para "transferência"
            r'\btrânsferência\b': 'transferência',
            
            # Correção de "essês" para "esses"
            r'\bessês\b': 'esses',
            
            # Correção de espaços antes de pontuação
            r'\s+([,\.;:!?])': r'\1',
            
            # Correção de múltiplos espaços
            r'\s{2,}': ' ',
        }
        
        # Aplica todas as correções
        texto_corrigido = texto
        for padrao, substituicao in correcoes_ocr.items():
            texto_corrigido = re.sub(padrao, substituicao, texto_corrigido, flags=re.IGNORECASE)
        
        return texto_corrigido
    
    def normalizar_titulo_clausula(self, titulo: str) -> str:
        """
        Normaliza o título da cláusula para o padrão correto
        
        Args:
            titulo: Título bruto extraído do PDF
            
        Returns:
            Título normalizado no padrão correto
        """
        # Remove espaços extras
        titulo = ' '.join(titulo.split())
        
        # Dicionário de correções de erros de OCR e padronização
        correcoes = {
            # Correção de "CLAUSULA" para "CLÁUSULA"
            r'^CLAUSULA\s+': 'CLÁUSULA ',
            r'^clausula\s+': 'CLÁUSULA ',
            r'^CúUSULA\s+': 'CLÁUSULA ',
            r'^cúUSULA\s+': 'CLÁUSULA ',
            r'^C[úu]USULA\s+': 'CLÁUSULA ',
            r'^c[úu]usula\s+': 'CLÁUSULA ',
            
            # Correção de ordinais com erros de OCR
            r'\bOUARTA\b': 'QUARTA',
            r'\bQuarta\b': 'QUARTA',
            r'\boITAVA\b': 'OITAVA',
            r'\bSEGUNOA\b': 'SEGUNDA',
            r'\boÉcIMA\b': 'DÉCIMA',
            r'\bDÉcIMA\b': 'DÉCIMA',
            r'\bvIGÉSIMA\b': 'VIGÉSIMA',
            r'\bVIGESIMA\b': 'VIGÉSIMA',
            r'\bVIGÉSIUN\b': 'VIGÉSIMA',
            r'\bTRIGESSIMA\b': 'TRIGÉSIMA',
            r'\bTRIGÉSSIMA\b': 'TRIGÉSIMA',
            r'\bQUADRAGESIMA\b': 'QUADRAGÉSIMA',
            r'\bQUADRAGÉSIMA\b': 'QUADRAGÉSIMA',
            r'\bQUINQUAGESIMA\b': 'QUINQUAGÉSIMA',
            r'\bQUINQUAGÉSIMA\b': 'QUINQUAGÉSIMA',
            r'\bOrave\b': 'OITAVA',
            r'\bQUIXTN\b': 'QUINTA',
            
            # Correção de "coMIsSÃo" para "COMISSÃO"
            r'\bcoMIsSÃo\b': 'COMISSÃO',
            r'\bcoMIssÃo\b': 'COMISSÃO',
            
            # Correção de "TRÂBALHO" para "TRABALHO"
            r'\bTRÂBALHO\b': 'TRABALHO',
            
            # Outras correções
            r'\bALIMENTAçÃO\b': 'ALIMENTAÇÃO',
            r'\bINSALUBRIDAOE\b': 'INSALUBRIDADE',
            r'\bDIRIGENÍE\b': 'DIRIGENTE',
            r'\bAOICIONAL\b': 'ADICIONAL',
            r'\bAUxíLIo\b': 'AUXÍLIO',
            r'\bcREcHE\b': 'CRECHE',
            r'\bFÉRhS\b': 'FÉRIAS',
            r'\bLIBERAÇÂO\b': 'LIBERAÇÃO',
            r'\bCONDIçÔES\b': 'CONDIÇÕES',
            r'\bATUALIZAçÃO\b': 'ATUALIZAÇÃO',
            r'\bMEDIAçÃO\b': 'MEDIAÇÃO',
            r'\bOEFICIÊNCIA\b': 'DEFICIÊNCIA',
            r'\bPERíODO\b': 'PERÍODO',
            r'\bASSÉOIO\b': 'ASSÉDIO',
            r'\bSETIMA\b': 'SÉTIMA',
            r'\bDECIMA\b': 'DÉCIMA',
        }
        
        # Aplica todas as correções
        for padrao, substituicao in correcoes.items():
            titulo = re.sub(padrao, substituicao, titulo, flags=re.IGNORECASE)
        
        # Remove pontos extras antes do hífen
        titulo = re.sub(r'\s*\.\s*-', ' -', titulo)
        titulo = re.sub(r'\s*\.\s+([A-Z])', r' - \1', titulo)
        
        # Garante que há hífen entre o ordinal e o título
        if re.match(r'^CLÁUSULA\s+\w+\s+[A-Z]', titulo) and ' - ' not in titulo:
            match = re.match(r'^(CLÁUSULA\s+(?:\w+\s+)*\w+)\s+([A-Z])', titulo)
            if match:
                titulo = f"{match.group(1)} - {match.group(2)}{titulo[match.end():]}"
        
        # Capitaliza corretamente
        titulo = titulo.upper()
        
        return titulo.strip()
    
    def extrair_clausulas(self) -> List[Dict[str, str]]:
        """
        Extrai todas as cláusulas do texto usando múltiplas estratégias
        
        Returns:
            Lista de dicionários com dados das cláusulas
        """
        print("📋 Extraindo cláusulas...")
        
        # Divide o texto em linhas para processamento linha por linha
        linhas = self.texto_completo.split('\n')
        
        clausulas_encontradas = []
        i = 0
        
        while i < len(linhas):
            linha = linhas[i].strip()
            
            # Verifica se a linha começa com variações de "CLÁUSULA"
            if re.match(r'^(?:CL[ÁAÚúaáu]USULA|cl[áaúu]usula|C[úáaU]USULA|c[úáau]usula)\s+', linha, re.IGNORECASE):
                # Captura o título completo da cláusula
                titulo_clausula = linha
                inicio_conteudo = i + 1
                
                # Encontra o fim da cláusula (próxima cláusula ou fim do texto)
                j = i + 1
                while j < len(linhas):
                    proxima_linha = linhas[j].strip()
                    if re.match(r'^(?:CL[ÁAÚúaáu]USULA|cl[áaúu]usula|C[úáaU]USULA|c[úáau]usula)\s+', proxima_linha, re.IGNORECASE):
                        break
                    j += 1
                
                # Extrai o conteúdo da cláusula
                conteudo_linhas = linhas[inicio_conteudo:j]
                conteudo_completo = '\n'.join(conteudo_linhas).strip()
                
                # Limpa artefatos
                conteudo_completo = self.limpar_artefatos(conteudo_completo)
                
                # Limpa o conteúdo
                conteudo_completo = self._limpar_conteudo(conteudo_completo)
                
                # Aplica correções de OCR no conteúdo
                conteudo_completo = self.corrigir_ocr_texto(conteudo_completo)
                
                if conteudo_completo:  # Só adiciona se tiver conteúdo
                    # Normaliza o título da cláusula
                    titulo_normalizado = self.normalizar_titulo_clausula(titulo_clausula)
                    
                    clausulas_encontradas.append({
                        'titulo': titulo_normalizado,
                        'conteudo': conteudo_completo,
                        'linha_inicio': i
                    })
                
                i = j  # Pula para a próxima cláusula
            else:
                i += 1
        
        print(f"   Encontradas {len(clausulas_encontradas)} cláusulas\n")
        
        # Processa cada cláusula encontrada
        clausulas = []
        for idx, clausula_info in enumerate(clausulas_encontradas, 1):
            titulo = clausula_info['titulo']
            conteudo = clausula_info['conteudo']
            
            # Gera resumo
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
            print(f"   ✓ Cláusula {idx}/{len(clausulas_encontradas)}: {titulo[:60]}...")
        
        self.clausulas = clausulas
        print(f"\n✓ Total de {len(clausulas)} cláusulas extraídas\n")
        return clausulas
    
    def _limpar_conteudo(self, texto: str) -> str:
        """
        Remove ruídos e formata o conteúdo da cláusula
        
        Args:
            texto: Texto bruto da cláusula
            
        Returns:
            Texto limpo
        """
        # Remove múltiplas quebras de linha
        texto = re.sub(r'\n{3,}', '\n\n', texto)
        
        # Remove linhas com apenas caracteres especiais ou números de página
        linhas = texto.split('\n')
        linhas_limpas = []
        
        for linha in linhas:
            linha_strip = linha.strip()
            # Ignora linhas muito curtas, apenas números, ou símbolos de assinatura
            if len(linha_strip) > 2 and not re.match(r'^[\d\s\-–—_\.]+$', linha_strip):
                # Remove símbolos de assinatura comuns no final do documento
                if not re.search(r'(?:Presidente|Diretor|Salvador,?\s+\d|^\s*[A-Z][a-z]+\s+[A-Z][a-z]+\s*$|^\d{10,}$)', linha_strip):
                    linhas_limpas.append(linha)
        
        texto_limpo = '\n'.join(linhas_limpas).strip()
        
        # Remove espaços múltiplos
        texto_limpo = re.sub(r' {2,}', ' ', texto_limpo)
        
        # Remove linhas que parecem ser artefatos de assinatura no final
        linhas_finais = texto_limpo.split('\n')
        while linhas_finais and (len(linhas_finais[-1].strip()) < 5 or 
                                 re.match(r'^[^\w\s]+$', linhas_finais[-1].strip())):
            linhas_finais.pop()
        
        texto_limpo = '\n'.join(linhas_finais)
        
        return texto_limpo
    
    def _gerar_resumo_simples(self, conteudo: str) -> str:
        """
        Gera um resumo simples pegando as primeiras frases
        
        Args:
            conteudo: Conteúdo completo da cláusula
            
        Returns:
            Resumo simples
        """
        if len(conteudo) <= 150:
            return conteudo
        
        # Procura o primeiro ponto final
        match_ponto = re.search(r'\.(?:\s|$)', conteudo[:300])
        if match_ponto:
            return conteudo[:match_ponto.end()].strip()
        
        # Fallback: primeiros 150 caracteres + "..."
        return conteudo[:150].strip() + "..."
    
    def _gerar_resumo_ia(self, titulo: str, conteudo: str) -> str:
        """
        Gera resumo usando IA (GPT)
        
        Args:
            titulo: Título da cláusula
            conteudo: Conteúdo completo da cláusula
            
        Returns:
            Resumo gerado pela IA
        """
        try:
            prompt = f"""Você é um especialista em direito trabalhista brasileiro. Analise a seguinte cláusula de uma Convenção Coletiva de Trabalho e gere um resumo conciso e objetivo em uma única frase (máximo 200 caracteres).

Título: {titulo}

Conteúdo:
{conteudo[:1500]}

Resumo (uma frase objetiva):"""

            response = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {"role": "system", "content": "Você é um especialista em direito trabalhista brasileiro. Gere resumos concisos e objetivos de cláusulas de CCTs."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=100
            )
            
            resumo = response.choices[0].message.content.strip()
            
            # Remove aspas se houver
            resumo = resumo.strip('"\'')
            
            # Garante que termina com ponto
            if resumo and not resumo.endswith('.'):
                resumo += '.'
            
            return resumo
            
        except Exception as e:
            print(f"   ⚠ Erro ao gerar resumo com IA: {e}")
            return self._gerar_resumo_simples(conteudo)
    
    def _limpar_para_csv(self, texto: str) -> str:
        """
        Limpa texto para ser salvo no CSV sem problemas de parsing
        
        Args:
            texto: Texto a ser limpo
            
        Returns:
            Texto limpo e seguro para CSV
        """
        if not isinstance(texto, str):
            return str(texto)
        
        # Remove quebras de linha e substitui por espaço
        texto = texto.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
        
        # Remove múltiplos espaços
        texto = ' '.join(texto.split())
        
        # Remove caracteres de controle problemáticos
        texto = ''.join(char for char in texto if ord(char) >= 32 or char in '\t\n\r')
        
        return texto.strip()
    
    def salvar_csv(self, output_path: str) -> None:
        """
        Salva as cláusulas extraídas em arquivo CSV com escape adequado para pandas
        
        Args:
            output_path: Caminho do arquivo CSV de saída
        """
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
                    quoting=csv.QUOTE_ALL,  # Força aspas em todos os campos
                    escapechar='\\',  # Caractere de escape
                    doublequote=True  # Duplica aspas internas
                )
                
                writer.writeheader()
                
                # Limpa dados antes de escrever para evitar problemas de parsing
                clausulas_limpas = []
                for clausula in self.clausulas:
                    clausula_limpa = {}
                    for key, value in clausula.items():
                        clausula_limpa[key] = self._limpar_para_csv(value)
                    clausulas_limpas.append(clausula_limpa)
                
                writer.writerows(clausulas_limpas)
            
            print(f"✓ Arquivo CSV salvo com sucesso!")
            print(f"   Total de linhas: {len(self.clausulas)}")
            print(f"   Tamanho do arquivo: {os.path.getsize(output_path) / 1024:.2f} KB\n")
            
        except Exception as e:
            print(f"❌ Erro ao salvar CSV: {e}")
            raise
    
    def processar(self, output_path: str) -> None:
        """
        Executa o processo completo de extração
        
        Args:
            output_path: Caminho do arquivo CSV de saída
        """
        print("=" * 70)
        print("🚀 EXTRATOR DE DADOS DE CCTs - VERSÃO 6 (PYMUPDF + CLEAN)")
        print("=" * 70)
        print()
        
        # 1. Extrair texto do PDF
        self.extrair_texto_pdf()
        
        # 2. Identificar sindicato e convenção
        self.identificar_sindicato_convencao()
        
        # 3. Extrair cláusulas
        self.extrair_clausulas()
        
        # 4. Salvar em CSV
        self.salvar_csv(output_path)
        
        print("=" * 70)
        print("✅ PROCESSO CONCLUÍDO COM SUCESSO!")
        print("=" * 70)


def main():
    """Função principal para execução via linha de comando"""
    parser = argparse.ArgumentParser(
        description='Extrator de Dados de Convenções Coletivas de Trabalho (CCTs) - Versão 6',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  
  # Extrair com resumos automáticos (IA):
  python extrator_cct_v6.py input.pdf -o output.csv
  
  # Extrair sem IA (resumos simples, mais rápido):
  python extrator_cct_v6.py input.pdf -o output.csv --sem-ia
        """
    )
    
    parser.add_argument('pdf_path', help='Caminho para o arquivo PDF da CCT')
    parser.add_argument('-o', '--output', required=True, help='Caminho para o arquivo CSV de saída')
    parser.add_argument('--sem-ia', action='store_true', help='Não usar IA para gerar resumos (mais rápido)')
    parser.add_argument('--modelo', default='gpt-4.1-mini', 
                       choices=['gpt-4.1-mini', 'gpt-4.1-nano', 'gemini-2.5-flash'],
                       help='Modelo de IA a ser usado (padrão: gpt-4.1-mini)')
    
    args = parser.parse_args()
    
    # Valida se o arquivo PDF existe
    if not os.path.exists(args.pdf_path):
        print(f"❌ Erro: Arquivo PDF não encontrado: {args.pdf_path}")
        return 1
    
    # Cria o extrator e processa
    try:
        extrator = ExtratorCCT(
            pdf_path=args.pdf_path,
            usar_ia=not args.sem_ia,
            modelo=args.modelo
        )
        extrator.processar(args.output)
        return 0
        
    except Exception as e:
        print(f"\n❌ ERRO FATAL: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
