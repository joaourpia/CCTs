# Extrator de Dados de CCTs (Convenções Coletivas de Trabalho)

## 📋 Descrição

Este script Python foi desenvolvido para **extrair automaticamente** dados de arquivos PDF de Convenções Coletivas de Trabalho (CCTs) e gerar arquivos CSV compatíveis com sua planilha mãe do Streamlit.

O script identifica automaticamente:
- **Sindicato(s)** envolvido(s) na convenção
- **Ano/Período** da convenção (ex: 2025-2026)
- **Cláusulas** individuais com seus títulos completos
- **Resumos** automáticos de cada cláusula (usando IA ou método simples)
- **Teor completo** de cada cláusula

## 🚀 Funcionalidades

### ✨ Principais Recursos

1. **Extração Robusta de Texto**
   - Utiliza `pdfplumber` para extrair texto de PDFs
   - Lida com diferentes formatos e qualidades de PDF
   - Tolerante a erros de OCR comuns

2. **Identificação Automática**
   - Detecta automaticamente sindicatos e período da convenção
   - Identifica todas as cláusulas, mesmo com variações de formatação
   - Suporta erros de OCR (ex: "CúUSULA" em vez de "CLÁUSULA")

3. **Geração de Resumos**
   - **Com IA**: Resumos concisos e objetivos gerados por GPT
   - **Sem IA**: Resumos simples baseados nas primeiras frases (mais rápido)

4. **Formato CSV Compatível**
   - Gera CSV no formato exato da sua planilha mãe
   - Colunas: `Sindicato`, `Convenção`, `Título da Cláusula`, `Resumo`, `Cláusula Completa`
   - Pronto para copiar e colar na planilha principal

## 📦 Requisitos

### Dependências Python

```bash
pip install pdfplumber openai
```

### Variáveis de Ambiente

O script utiliza a API da OpenAI para gerar resumos. Certifique-se de ter a variável `OPENAI_API_KEY` configurada:

```bash
export OPENAI_API_KEY="sua-chave-api-aqui"
```

## 🔧 Instalação

1. **Clone ou baixe os arquivos**:
   - `extrator_cct_v2.py` (versão recomendada)
   - `extrator_cct.py` (versão alternativa)

2. **Instale as dependências**:
   ```bash
   pip install pdfplumber openai
   ```

3. **Torne o script executável** (opcional):
   ```bash
   chmod +x extrator_cct_v2.py
   ```

## 💻 Uso

### Sintaxe Básica

```bash
python extrator_cct_v2.py <arquivo_pdf> -o <arquivo_csv_saida>
```

### Exemplos Práticos

#### 1. Extração com IA (Recomendado)

```bash
python extrator_cct_v2.py "CCT_2025-2026.pdf" -o "cct_2025_2026.csv"
```

**Vantagens**:
- Resumos mais precisos e profissionais
- Melhor compreensão do conteúdo jurídico
- Ideal para documentação final

#### 2. Extração Rápida (Sem IA)

```bash
python extrator_cct_v2.py "CCT_2025-2026.pdf" -o "cct_2025_2026.csv" --sem-ia
```

**Vantagens**:
- Processamento muito mais rápido
- Não requer API da OpenAI
- Ideal para testes e processamento em lote

#### 3. Escolher Modelo de IA

```bash
# Modelo mais rápido e econômico
python extrator_cct_v2.py "CCT_2025-2026.pdf" -o "output.csv" --modelo gpt-4.1-nano

# Modelo padrão (balanceado)
python extrator_cct_v2.py "CCT_2025-2026.pdf" -o "output.csv" --modelo gpt-4.1-mini

# Modelo alternativo (Google)
python extrator_cct_v2.py "CCT_2025-2026.pdf" -o "output.csv" --modelo gemini-2.5-flash
```

#### 4. Processar Múltiplos Arquivos

**Bash/Linux/Mac**:
```bash
for file in *.pdf; do
    python extrator_cct_v2.py "$file" -o "${file%.pdf}.csv"
done
```

**PowerShell/Windows**:
```powershell
Get-ChildItem *.pdf | ForEach-Object {
    python extrator_cct_v2.py $_.FullName -o "$($_.BaseName).csv"
}
```

## 📊 Estrutura do CSV Gerado

O CSV gerado possui a seguinte estrutura:

| Coluna | Descrição | Exemplo |
|--------|-----------|---------|
| **Sindicato** | Nome(s) do(s) sindicato(s) | "SINDICATO DOS MÉDICOS x SINDICATO DAS SANTAS CASAS" |
| **Convenção** | Ano ou período da convenção | "2025-2026" |
| **Título da Cláusula** | Título completo da cláusula | "CLÁUSULA PRIMEIRA - VIGÊNCIA E DATA-BASE" |
| **Resumo** | Resumo conciso da cláusula | "Define o período de vigência da convenção de 01/05/2025 a 30/04/2026." |
| **Cláusula Completa** | Texto completo da cláusula | "As partes fixam a vigência da presente Convenção..." |

### Exemplo de Saída

```csv
Sindicato,Convenção,Título da Cláusula,Resumo,Cláusula Completa
SINDICATO DOS MÉDICOS x SINDICATO DAS SANTAS CASAS,2025-2026,CLÁUSULA PRIMEIRA - VIGÊNCIA,"Define vigência de 01/05/2025 a 30/04/2026.","As partes fixam a vigência..."
```

## 🔍 Como Funciona

### Fluxo de Processamento

```
1. Extração de Texto
   ↓
2. Identificação de Sindicato e Convenção
   ↓
3. Detecção de Cláusulas
   ↓
4. Limpeza de Conteúdo
   ↓
5. Geração de Resumos
   ↓
6. Exportação para CSV
```

### Detalhes Técnicos

1. **Extração de Texto**:
   - Usa `pdfplumber` para extrair texto página por página
   - Preserva quebras de linha e formatação básica

2. **Identificação de Cláusulas**:
   - Busca padrões como "CLÁUSULA PRIMEIRA", "CLAUSULA SEGUNDA", etc.
   - Tolerante a erros de OCR (CúUSULA, cláusula, etc.)
   - Processa linha por linha para maior precisão

3. **Limpeza de Conteúdo**:
   - Remove assinaturas e artefatos
   - Elimina linhas vazias excessivas
   - Preserva parágrafos e estrutura

4. **Geração de Resumos**:
   - **Com IA**: Usa GPT para gerar resumos contextualizados
   - **Sem IA**: Extrai primeiras frases ou primeiros 150 caracteres

## 🎯 Integração com Streamlit

### Workflow Recomendado

1. **Processar Nova CCT**:
   ```bash
   python extrator_cct_v2.py "nova_cct.pdf" -o "nova_cct.csv"
   ```

2. **Abrir o CSV Gerado**:
   - Use Excel, LibreOffice ou Google Sheets
   - Revise os dados extraídos

3. **Copiar e Colar na Planilha Mãe**:
   - Abra `clausulas_farmaceuticos.csv`
   - Selecione e copie todas as linhas do novo CSV (exceto cabeçalho)
   - Cole no final da planilha mãe

4. **Atualizar Streamlit**:
   - Salve a planilha mãe atualizada
   - Reinicie o aplicativo Streamlit
   - As novas cláusulas estarão disponíveis

### Exemplo de Código Streamlit

```python
import pandas as pd
import streamlit as st

# Carregar dados
df = pd.read_csv("clausulas_farmaceuticos.csv", encoding="utf-8")

# Filtrar por sindicato
sindicato_escolhido = st.selectbox("Selecione o sindicato:", df["Sindicato"].unique())
df_filtrado = df[df["Sindicato"] == sindicato_escolhido]

# Exibir cláusulas
for _, row in df_filtrado.iterrows():
    st.markdown(f"### {row['Título da Cláusula']}")
    st.write(f"**Resumo:** {row['Resumo']}")
    st.write(row['Cláusula Completa'])
```

## ⚙️ Opções Avançadas

### Argumentos da Linha de Comando

```
usage: extrator_cct_v2.py [-h] -o OUTPUT [--sem-ia] [--modelo {gpt-4.1-mini,gpt-4.1-nano,gemini-2.5-flash}] pdf_path

positional arguments:
  pdf_path              Caminho para o arquivo PDF da CCT

optional arguments:
  -h, --help            Mostra esta mensagem de ajuda
  -o OUTPUT, --output OUTPUT
                        Caminho para o arquivo CSV de saída
  --sem-ia              Não usar IA para gerar resumos (mais rápido)
  --modelo {gpt-4.1-mini,gpt-4.1-nano,gemini-2.5-flash}
                        Modelo de IA a ser usado (padrão: gpt-4.1-mini)
```

### Modelos de IA Disponíveis

| Modelo | Velocidade | Qualidade | Custo | Recomendado Para |
|--------|-----------|-----------|-------|------------------|
| `gpt-4.1-nano` | ⚡⚡⚡ Muito Rápido | ⭐⭐⭐ Bom | 💰 Baixo | Processamento em lote |
| `gpt-4.1-mini` | ⚡⚡ Rápido | ⭐⭐⭐⭐ Ótimo | 💰💰 Médio | **Uso geral (padrão)** |
| `gemini-2.5-flash` | ⚡⚡⚡ Muito Rápido | ⭐⭐⭐⭐ Ótimo | 💰 Baixo | Alternativa ao GPT |

## 🐛 Solução de Problemas

### Problema: "Nenhuma cláusula encontrada"

**Causas possíveis**:
- PDF com imagens em vez de texto
- Formatação muito diferente do padrão

**Soluções**:
1. Verifique se o PDF contém texto selecionável
2. Tente usar OCR antes (ex: Adobe Acrobat, Tesseract)
3. Ajuste os padrões regex no código

### Problema: "Erro ao gerar resumo com IA"

**Causas possíveis**:
- API key não configurada
- Limite de requisições excedido
- Problema de conexão

**Soluções**:
1. Verifique a variável `OPENAI_API_KEY`
2. Use `--sem-ia` para processar sem IA
3. Aguarde alguns minutos e tente novamente

### Problema: "CSV com caracteres estranhos"

**Causas possíveis**:
- Problema de encoding

**Soluções**:
1. Abra o CSV com encoding UTF-8
2. No Excel: Dados → De Texto/CSV → Encoding: UTF-8
3. No Google Sheets: importa automaticamente

## 📝 Notas Importantes

### Limitações

1. **Qualidade do PDF**: O script depende da qualidade do texto extraído do PDF
2. **Formatação Variável**: PDFs com formatação muito diferente podem exigir ajustes
3. **Custos de API**: Usar IA consome créditos da OpenAI (valores baixos, mas considere)

### Boas Práticas

1. **Sempre revise** os dados extraídos antes de integrar à planilha mãe
2. **Faça backup** da planilha mãe antes de adicionar novos dados
3. **Use --sem-ia** para testes rápidos, depois processe com IA para produção
4. **Mantenha** os PDFs originais como referência

## 🆘 Suporte

### Problemas Comuns

- **PDF protegido**: Remova a proteção antes de processar
- **PDF muito grande**: Considere dividir em partes menores
- **Erros de encoding**: Use UTF-8 ao abrir os CSVs

### Melhorias Futuras

- [ ] Suporte a PDFs escaneados (OCR integrado)
- [ ] Interface gráfica (GUI)
- [ ] Detecção automática de parágrafos e subitens
- [ ] Exportação para outros formatos (Excel, JSON)

## 📄 Licença

Este script foi desenvolvido para uso interno. Sinta-se livre para modificar e adaptar conforme suas necessidades.

## 👨‍💻 Autor

Desenvolvido por **Manus AI** para automatização de extração de dados de CCTs.

---

**Versão**: 2.0  
**Data**: Dezembro 2024  
**Compatibilidade**: Python 3.7+
