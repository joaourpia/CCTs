import pdfplumber
import pandas as pd
import re
import os
from pathlib import Path
from typing import List, Dict
import warnings
warnings.filterwarnings('ignore')


class ExtractorClausulasCCT:
    """
    Extrator de cláusulas de Convenções Coletivas de Trabalho (CCT) em PDF
    """
    
    def __init__(self, pasta_pdfs: str = "pdfs_entrada"):
        self.pasta_pdfs = pasta_pdfs
        self.dados_extraidos = []
        
        # Criar pasta se não existir
        if not os.path.exists(pasta_pdfs):
            os.makedirs(pasta_pdfs)
            print(f"✅ Pasta '{pasta_pdfs}' criada. Coloque os PDFs nela.")
    
    def extrair_texto_pdf(self, caminho_pdf: str) -> str:
        """Extrai todo o texto do PDF"""
        texto_completo = ""
        try:
            with pdfplumber.open(caminho_pdf) as pdf:
                for pagina in pdf.pages:
                    texto = pagina.extract_text()
                    if texto:
                        texto_completo += texto + "\n"
            return texto_completo
        except Exception as e:
            print(f"❌ Erro ao ler {caminho_pdf}: {str(e)}")
            return ""
    
    def identificar_sindicato(self, texto: str) -> str:
        """Identifica o nome do sindicato no texto"""
        # Padrões comuns
        padroes = [
            r'SINDICATO\s+DOS?\s+([A-ZÀÁÂÃÇÉÊÍÓÔÕÚ\s]+?)(?=\s+E\s+|$)',
            r'SINDICATO\s+([A-ZÀÁÂÃÇÉÊÍÓÔÕÚ\s]+?)(?=\s+CNPJ|$)',
            r'(?:SINDICATO|SINDIC\.)\s+([A-ZÀÁÂÃÇÉÊÍÓÔÕÚ\s]+?)(?:\n|,)',
        ]
        
        for padrao in padroes:
            match = re.search(padrao, texto[:2000], re.IGNORECASE)
            if match:
                sindicato = match.group(1).strip()
                # Limpar nome
                sindicato = re.sub(r'\s+', ' ', sindicato)
                return sindicato[:100]  # Limitar tamanho
        
        return "SINDICATO NÃO IDENTIFICADO"
    
    def identificar_convencao(self, texto: str, nome_arquivo: str) -> str:
        """Identifica o nome/ano da convenção"""
        # Tentar extrair do texto
        padroes = [
            r'CONVENÇÃO\s+COLETIVA\s+DE\s+TRABALHO\s+(\d{4}[/-]\d{4}|\d{4})',
            r'CCT\s+(\d{4}[/-]\d{4}|\d{4})',
            r'ACORDO\s+COLETIVO\s+(\d{4}[/-]\d{4}|\d{4})',
        ]
        
        for padrao in padroes:
            match = re.search(padrao, texto[:3000], re.IGNORECASE)
            if match:
                return f"CONVENÇÃO COLETIVA {match.group(1)}"
        
        # Fallback: usar nome do arquivo
        ano = re.search(r'(20\d{2})', nome_arquivo)
        if ano:
            return f"CONVENÇÃO COLETIVA {ano.group(1)}"
        
        return "CONVENÇÃO COLETIVA"
    
    def extrair_clausulas(self, texto: str) -> List[Dict]:
        """Extrai as cláusulas do texto"""
        clausulas = []
        
        # Padrões para identificar cláusulas
        # Exemplo: "CLÁUSULA PRIMEIRA", "CLÁUSULA 1ª", "CLÁUSULA DÉCIMA SEGUNDA"
        padrao_clausula = r'CLÁUSULA\s+(?:PRIMEIRA|SEGUNDA|TERCEIRA|QUARTA|QUINTA|SEXTA|SÉTIMA|OITAVA|NONA|DÉCIMA|DÉCIMA\s+PRIMEIRA|DÉCIMA\s+SEGUNDA|DÉCIMA\s+TERCEIRA|VIGÉSIMA|TRIGÉSIMA|QUADRAGÉSIMA|QUINQUAGÉSIMA|[0-9]+[ªº]?)\s*[-–—]*\s*([^\n]+)'
        
        matches = list(re.finditer(padrao_clausula, texto, re.IGNORECASE | re.MULTILINE))
        
        for i, match in enumerate(matches):
            # Título da cláusula
            titulo_completo = match.group(0).strip()
            titulo = match.group(1).strip()
            
            # Início do conteúdo
            inicio = match.end()
            
            # Fim do conteúdo (próxima cláusula ou fim do texto)
            if i < len(matches) - 1:
                fim = matches[i + 1].start()
            else:
                fim = len(texto)
            
            # Conteúdo completo
            conteudo = texto[inicio:fim].strip()
            
            # Limpar conteúdo
            conteudo = re.sub(r'\n+', ' ', conteudo)
            conteudo = re.sub(r'\s+', ' ', conteudo)
            
            # Gerar resumo (primeiras 150 caracteres ou primeira frase)
            resumo = self.gerar_resumo(conteudo)
            
            clausulas.append({
                'titulo': titulo,
                'resumo': resumo,
                'conteudo_completo': conteudo[:5000]  # Limitar tamanho
            })
        
        return clausulas
    
    def gerar_resumo(self, texto: str, max_chars: int = 150) -> str:
        """Gera um resumo do texto"""
        # Pegar primeira frase ou primeiros N caracteres
        primeira_frase = re.match(r'^[^.!?]+[.!?]', texto)
        
        if primeira_frase and len(primeira_frase.group(0)) <= max_chars:
            return primeira_frase.group(0).strip()
        
        # Cortar em max_chars
        if len(texto) <= max_chars:
            return texto
        
        resumo = texto[:max_chars]
        ultimo_espaco = resumo.rfind(' ')
        if ultimo_espaco > 0:
            resumo = resumo[:ultimo_espaco]
        
        return resumo + "..."
    
    def processar_pdf(self, caminho_pdf: str) -> int:
        """Processa um único PDF e retorna número de cláusulas extraídas"""
        print(f"\n📄 Processando: {os.path.basename(caminho_pdf)}")
        
        # Extrair texto
        texto = self.extrair_texto_pdf(caminho_pdf)
        if not texto:
            print(f"   ⚠️ Nenhum texto extraído")
            return 0
        
        # Identificar sindicato e convenção
        sindicato = self.identificar_sindicato(texto)
        convencao = self.identificar_convencao(texto, os.path.basename(caminho_pdf))
        
        print(f"   📌 Sindicato: {sindicato}")
        print(f"   📌 Convenção: {convencao}")
        
        # Extrair cláusulas
        clausulas = self.extrair_clausulas(texto)
        
        if not clausulas:
            print(f"   ⚠️ Nenhuma cláusula encontrada")
            return 0
        
        print(f"   ✅ {len(clausulas)} cláusulas extraídas")
        
        # Adicionar aos dados
        for clausula in clausulas:
            self.dados_extraidos.append({
                'Sindicato': sindicato,
                'Convenção': convencao,
                'Título da Cláusula': clausula['titulo'],
                'Resumo': clausula['resumo'],
                'Cláusula Completa': clausula['conteudo_completo']
            })
        
        return len(clausulas)
    
    def processar_todos_pdfs(self) -> pd.DataFrame:
        """Processa todos os PDFs da pasta"""
        arquivos_pdf = list(Path(self.pasta_pdfs).glob("*.pdf"))
        
        if not arquivos_pdf:
            print(f"❌ Nenhum arquivo PDF encontrado na pasta '{self.pasta_pdfs}'")
            return pd.DataFrame()
        
        print(f"\n🔍 Encontrados {len(arquivos_pdf)} arquivos PDF\n")
        print("="*60)
        
        total_clausulas = 0
        for pdf in arquivos_pdf:
            num_clausulas = self.processar_pdf(str(pdf))
            total_clausulas += num_clausulas
        
        print("\n" + "="*60)
        print(f"\n✅ PROCESSAMENTO CONCLUÍDO!")
        print(f"   📊 Total de cláusulas extraídas: {total_clausulas}")
        print(f"   📁 Total de PDFs processados: {len(arquivos_pdf)}")
        
        return pd.DataFrame(self.dados_extraidos)
    
    def salvar_csv(self, df: pd.DataFrame, nome_arquivo: str = "clausulas_extraidas.csv"):
        """Salva o DataFrame em CSV"""
        if df.empty:
            print("\n❌ Nenhum dado para salvar")
            return
        
        df.to_csv(nome_arquivo, index=False, encoding='utf-8')
        print(f"\n💾 Arquivo salvo: {nome_arquivo}")
        print(f"   📈 Total de linhas: {len(df)}")
    
    def mesclar_com_csv_existente(self, df_novo: pd.DataFrame, 
                                  csv_existente: str = "clausulas_farmaceuticos.csv"):
        """Mescla novos dados com CSV existente"""
        if os.path.exists(csv_existente):
            df_existente = pd.read_csv(csv_existente, encoding='utf-8')
            df_final = pd.concat([df_existente, df_novo], ignore_index=True)
            
            # Remover duplicatas
            df_final = df_final.drop_duplicates(
                subset=['Sindicato', 'Convenção', 'Título da Cláusula'],
                keep='last'
            )
            
            print(f"\n🔄 Mesclando com arquivo existente...")
            print(f"   📊 Registros existentes: {len(df_existente)}")
            print(f"   ➕ Novos registros: {len(df_novo)}")
            print(f"   📈 Total final: {len(df_final)}")
            
            return df_final
        else:
            return df_novo


def main():
    """Função principal"""
    print("="*60)
    print("🔧 EXTRATOR DE CLÁUSULAS DE CONVENÇÕES COLETIVAS")
    print("="*60)
    
    # Criar extrator
    extrator = ExtractorClausulasCCT(pasta_pdfs="pdfs_entrada")
    
    # Processar PDFs
    df = extrator.processar_todos_pdfs()
    
    if not df.empty:
        # Salvar novo arquivo
        extrator.salvar_csv(df, "clausulas_extraidas.csv")
        
        # Opção: mesclar com arquivo existente
        resposta = input("\n❓ Deseja mesclar com 'clausulas_farmaceuticos.csv'? (s/n): ")
        if resposta.lower() == 's':
            df_final = extrator.mesclar_com_csv_existente(df)
            extrator.salvar_csv(df_final, "clausulas_farmaceuticos.csv")
        
        print("\n✅ Processo concluído com sucesso!")
    else:
        print("\n⚠️ Nenhum dado foi extraído")


if __name__ == "__main__":
    main()
