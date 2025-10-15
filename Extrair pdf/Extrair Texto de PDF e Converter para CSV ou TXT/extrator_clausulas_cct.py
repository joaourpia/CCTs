#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Extração de Cláusulas de Convenções Coletivas de Trabalho (CCT)
Extrai cláusulas de PDFs (texto ou imagem) e gera arquivo CSV

Autor: Assistente Python
Data: 2025
"""

import re
import csv
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Tuple

try:
    import pdfplumber
except ImportError:
    print("ERRO: Biblioteca 'pdfplumber' não encontrada.")
    print("Instale com: pip3 install pdfplumber")
    sys.exit(1)

try:
    from pdf2image import convert_from_path
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("AVISO: OCR não disponível. Instale com:")
    print("  pip3 install pdf2image pytesseract")
    print("  sudo apt-get install tesseract-ocr tesseract-ocr-por poppler-utils")


class ExtratorClausulasCCT:
    """Classe para extrair cláusulas de PDFs de Convenções Coletivas"""
    
    def __init__(self, pdf_path: str, sindicato: str = "", convencao: str = ""):
        """
        Inicializa o extrator
        
        Args:
            pdf_path: Caminho para o arquivo PDF
            sindicato: Nome do sindicato (opcional)
            convencao: Nome/ano da convenção (opcional)
        """
        self.pdf_path = Path(pdf_path)
        self.sindicato = sindicato
        self.convencao = convencao
        self.clausulas = []
        
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {pdf_path}")
    
    def extrair_texto_pdf(self) -> str:
        """
        Extrai texto do PDF usando pdfplumber
        
        Returns:
            Texto completo do PDF
        """
        texto_completo = []
        
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for pagina in pdf.pages:
                    texto = pagina.extract_text()
                    if texto:
                        texto_completo.append(texto)
        except Exception as e:
            print(f"Erro ao extrair texto com pdfplumber: {e}")
            return ""
        
        return "\n".join(texto_completo)
    
    def extrair_texto_ocr(self) -> str:
        """
        Extrai texto do PDF usando OCR (para PDFs com imagens)
        
        Returns:
            Texto completo extraído via OCR
        """
        if not OCR_AVAILABLE:
            print("ERRO: OCR não disponível. Não é possível processar PDF com imagens.")
            return ""
        
        texto_completo = []
        
        try:
            # Converte PDF em imagens
            imagens = convert_from_path(str(self.pdf_path))
            
            # Aplica OCR em cada página
            for i, imagem in enumerate(imagens):
                print(f"  Processando página {i+1}/{len(imagens)} com OCR...")
                texto = pytesseract.image_to_string(imagem, lang='por')
                texto_completo.append(texto)
        
        except Exception as e:
            print(f"Erro ao extrair texto com OCR: {e}")
            return ""
        
        return "\n".join(texto_completo)
    
    def extrair_texto(self, usar_ocr: bool = False) -> str:
        """
        Extrai texto do PDF (tenta texto nativo primeiro, depois OCR se necessário)
        
        Args:
            usar_ocr: Forçar uso de OCR
            
        Returns:
            Texto completo do PDF
        """
        print(f"Extraindo texto de: {self.pdf_path.name}")
        
        if usar_ocr:
            return self.extrair_texto_ocr()
        
        # Tenta extrair texto nativo primeiro
        texto = self.extrair_texto_pdf()
        
        # Se não conseguiu texto suficiente, tenta OCR
        if len(texto.strip()) < 100:
            print("  Pouco texto extraído. Tentando OCR...")
            texto = self.extrair_texto_ocr()
        
        return texto
    
    def identificar_clausulas(self, texto: str) -> List[Dict[str, str]]:
        """
        Identifica e extrai cláusulas do texto
        
        Args:
            texto: Texto completo do PDF
            
        Returns:
            Lista de dicionários com informações das cláusulas
        """
        clausulas = []
        
        # Padrões para identificar cláusulas
        # Exemplos: "CLÁUSULA PRIMEIRA", "CLÁUSULA DÉCIMA SEGUNDA", etc.
        padrao_clausula = r'CLÁUSULA\s+(PRIMEIRA|SEGUNDA|TERCEIRA|QUARTA|QUINTA|SEXTA|SÉTIMA|OITAVA|NONA|DÉCIMA(?:\s+PRIMEIRA|\s+SEGUNDA|\s+TERCEIRA|\s+QUARTA|\s+QUINTA|\s+SEXTA|\s+SÉTIMA|\s+OITAVA|\s+NONA)?|VIGÉSIMA(?:\s+PRIMEIRA|\s+SEGUNDA|\s+TERCEIRA|\s+QUARTA|\s+QUINTA|\s+SEXTA|\s+SÉTIMA|\s+OITAVA|\s+NONA)?|TRIGÉSIMA(?:\s+PRIMEIRA|\s+SEGUNDA|\s+TERCEIRA|\s+QUARTA|\s+QUINTA|\s+SEXTA|\s+SÉTIMA|\s+OITAVA|\s+NONA)?|QUADRAGÉSIMA(?:\s+PRIMEIRA|\s+SEGUNDA|\s+TERCEIRA|\s+QUARTA|\s+QUINTA|\s+SEXTA|\s+SÉTIMA|\s+OITAVA|\s+NONA)?|QUINQUAGÉSIMA(?:\s+PRIMEIRA|\s+SEGUNDA|\s+TERCEIRA|\s+QUARTA|\s+QUINTA|\s+SEXTA|\s+SÉTIMA|\s+OITAVA|\s+NONA)?)\s*-\s*([^\n]+)'
        
        # Encontra todas as cláusulas
        matches = list(re.finditer(padrao_clausula, texto, re.IGNORECASE))
        
        for i, match in enumerate(matches):
            numero_extenso = match.group(1).strip()
            titulo = match.group(2).strip()
            
            # Posição inicial da cláusula
            inicio = match.start()
            
            # Posição final da cláusula (início da próxima ou fim do texto)
            if i < len(matches) - 1:
                fim = matches[i + 1].start()
            else:
                fim = len(texto)
            
            # Extrai o texto completo da cláusula
            texto_clausula = texto[inicio:fim].strip()
            
            # Remove o título da cláusula do texto completo
            texto_clausula = re.sub(
                r'^CLÁUSULA\s+' + re.escape(numero_extenso) + r'\s*-\s*' + re.escape(titulo) + r'\s*',
                '',
                texto_clausula,
                flags=re.IGNORECASE
            ).strip()
            
            # Gera um resumo (primeiras 150 caracteres do texto)
            resumo = self.gerar_resumo(texto_clausula)
            
            # Monta o título completo
            titulo_completo = f"CLÁUSULA {numero_extenso} - {titulo}"
            
            clausulas.append({
                'numero_extenso': numero_extenso,
                'titulo': titulo,
                'titulo_completo': titulo_completo,
                'resumo': resumo,
                'texto_completo': texto_clausula
            })
        
        return clausulas
    
    def gerar_resumo(self, texto: str, max_chars: int = 150) -> str:
        """
        Gera um resumo do texto da cláusula
        
        Args:
            texto: Texto completo da cláusula
            max_chars: Número máximo de caracteres do resumo
            
        Returns:
            Resumo do texto
        """
        # Remove quebras de linha múltiplas e espaços extras
        texto_limpo = re.sub(r'\s+', ' ', texto).strip()
        
        # Pega a primeira frase ou até max_chars
        if len(texto_limpo) <= max_chars:
            return texto_limpo
        
        # Tenta cortar em uma frase completa
        resumo = texto_limpo[:max_chars]
        
        # Procura pelo último ponto antes do limite
        ultimo_ponto = resumo.rfind('.')
        if ultimo_ponto > max_chars * 0.6:  # Se o ponto está em pelo menos 60% do limite
            return resumo[:ultimo_ponto + 1].strip()
        
        # Caso contrário, corta na última palavra
        ultimo_espaco = resumo.rfind(' ')
        if ultimo_espaco > 0:
            return resumo[:ultimo_espaco].strip() + "..."
        
        return resumo + "..."
    
    def processar(self, usar_ocr: bool = False) -> List[Dict[str, str]]:
        """
        Processa o PDF e extrai todas as cláusulas
        
        Args:
            usar_ocr: Forçar uso de OCR
            
        Returns:
            Lista de cláusulas extraídas
        """
        # Extrai texto
        texto = self.extrair_texto(usar_ocr)
        
        if not texto.strip():
            print("ERRO: Não foi possível extrair texto do PDF.")
            return []
        
        # Identifica cláusulas
        print(f"Identificando cláusulas...")
        self.clausulas = self.identificar_clausulas(texto)
        
        print(f"Total de cláusulas encontradas: {len(self.clausulas)}")
        
        return self.clausulas
    
    def salvar_csv(self, output_path: str, clausulas: List[Dict[str, str]] = None):
        """
        Salva as cláusulas em arquivo CSV
        
        Args:
            output_path: Caminho do arquivo CSV de saída
            clausulas: Lista de cláusulas (usa self.clausulas se não fornecido)
        """
        if clausulas is None:
            clausulas = self.clausulas
        
        if not clausulas:
            print("AVISO: Nenhuma cláusula para salvar.")
            return
        
        output_file = Path(output_path)
        
        # Cria o diretório se não existir
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Escreve o CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Cabeçalho
            writer.writerow([
                'Sindicato',
                'Convenção',
                'Título da Cláusula',
                'Resumo',
                'Cláusula Completa'
            ])
            
            # Dados
            for clausula in clausulas:
                writer.writerow([
                    self.sindicato,
                    self.convencao,
                    clausula['titulo_completo'],
                    clausula['resumo'],
                    clausula['texto_completo']
                ])
        
        print(f"\nArquivo CSV salvo: {output_file}")
        print(f"Total de cláusulas exportadas: {len(clausulas)}")
    
    def salvar_txt(self, output_path: str, clausulas: List[Dict[str, str]] = None):
        """
        Salva as cláusulas em arquivo TXT formatado
        
        Args:
            output_path: Caminho do arquivo TXT de saída
            clausulas: Lista de cláusulas (usa self.clausulas se não fornecido)
        """
        if clausulas is None:
            clausulas = self.clausulas
        
        if not clausulas:
            print("AVISO: Nenhuma cláusula para salvar.")
            return
        
        output_file = Path(output_path)
        
        # Cria o diretório se não existir
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Escreve o TXT
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"CONVENÇÃO COLETIVA DE TRABALHO\n")
            f.write(f"Sindicato: {self.sindicato}\n")
            f.write(f"Convenção: {self.convencao}\n")
            f.write(f"{'=' * 80}\n\n")
            
            for i, clausula in enumerate(clausulas, 1):
                f.write(f"{clausula['titulo_completo']}\n")
                f.write(f"{'-' * 80}\n")
                f.write(f"Resumo: {clausula['resumo']}\n\n")
                f.write(f"Texto Completo:\n{clausula['texto_completo']}\n")
                f.write(f"\n{'=' * 80}\n\n")
        
        print(f"\nArquivo TXT salvo: {output_file}")
        print(f"Total de cláusulas exportadas: {len(clausulas)}")


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description='Extrai cláusulas de PDFs de Convenções Coletivas de Trabalho',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  
  # Extração básica para CSV
  python3 extrator_clausulas_cct.py -i convencao.pdf -o clausulas.csv
  
  # Com informações de sindicato e convenção
  python3 extrator_clausulas_cct.py -i convencao.pdf -o clausulas.csv \\
      -s "FARMACÊUTICOS" -c "MARINGA 2023"
  
  # Forçar uso de OCR (para PDFs escaneados)
  python3 extrator_clausulas_cct.py -i convencao.pdf -o clausulas.csv --ocr
  
  # Salvar em formato TXT
  python3 extrator_clausulas_cct.py -i convencao.pdf -o clausulas.txt
  
  # Limitar número de cláusulas extraídas
  python3 extrator_clausulas_cct.py -i convencao.pdf -o clausulas.csv --limite 18
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='Arquivo PDF de entrada (convenção coletiva)'
    )
    
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Arquivo de saída (CSV ou TXT)'
    )
    
    parser.add_argument(
        '-s', '--sindicato',
        default='',
        help='Nome do sindicato'
    )
    
    parser.add_argument(
        '-c', '--convencao',
        default='',
        help='Nome/ano da convenção (ex: MARINGA 2023)'
    )
    
    parser.add_argument(
        '--ocr',
        action='store_true',
        help='Forçar uso de OCR (para PDFs escaneados/com imagens)'
    )
    
    parser.add_argument(
        '--limite',
        type=int,
        default=None,
        help='Limitar número de cláusulas extraídas (ex: 18 para extrair até a décima oitava)'
    )
    
    args = parser.parse_args()
    
    try:
        # Cria o extrator
        extrator = ExtratorClausulasCCT(
            pdf_path=args.input,
            sindicato=args.sindicato,
            convencao=args.convencao
        )
        
        # Processa o PDF
        clausulas = extrator.processar(usar_ocr=args.ocr)
        
        if not clausulas:
            print("\nERRO: Nenhuma cláusula foi encontrada no PDF.")
            print("Dicas:")
            print("  - Verifique se o PDF contém cláusulas no formato esperado")
            print("  - Se o PDF for escaneado, tente usar a opção --ocr")
            sys.exit(1)
        
        # Aplica limite se especificado
        if args.limite and args.limite > 0:
            clausulas = clausulas[:args.limite]
            print(f"\nLimitando extração às primeiras {args.limite} cláusulas.")
        
        # Salva no formato apropriado
        output_path = Path(args.output)
        
        if output_path.suffix.lower() == '.csv':
            extrator.salvar_csv(args.output, clausulas)
        elif output_path.suffix.lower() == '.txt':
            extrator.salvar_txt(args.output, clausulas)
        else:
            print(f"AVISO: Extensão não reconhecida '{output_path.suffix}'. Salvando como CSV.")
            extrator.salvar_csv(args.output, clausulas)
        
        print("\n✓ Extração concluída com sucesso!")
        
    except FileNotFoundError as e:
        print(f"ERRO: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

