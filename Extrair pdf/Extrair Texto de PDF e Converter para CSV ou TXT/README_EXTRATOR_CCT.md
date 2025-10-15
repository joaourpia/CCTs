# Extrator de Cláusulas de Convenções Coletivas de Trabalho (CCT)

Script Python para extrair cláusulas de PDFs de Convenções Coletivas de Trabalho e gerar arquivos CSV ou TXT estruturados.

## Características

- **Extração automática** de cláusulas de PDFs
- **Suporte a PDFs com texto** (nativos)
- **Suporte a PDFs escaneados** (via OCR - opcional)
- **Exportação em CSV** no formato compatível com Streamlit
- **Exportação em TXT** formatado para leitura
- **Identificação inteligente** de títulos e numeração de cláusulas
- **Geração automática de resumos** para cada cláusula

## Requisitos

### Requisitos Básicos (PDFs com texto)

```bash
pip3 install pdfplumber
```

### Requisitos para OCR (PDFs escaneados/imagens)

```bash
# Instalar bibliotecas Python
pip3 install pdf2image pytesseract

# Instalar dependências do sistema (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-por poppler-utils
```

## Instalação

1. Baixe o script `extrator_clausulas_cct.py`
2. Torne-o executável:
   ```bash
   chmod +x extrator_clausulas_cct.py
   ```
3. Instale as dependências necessárias (veja seção Requisitos)

## Uso

### Sintaxe Básica

```bash
python3 extrator_clausulas_cct.py -i <PDF_ENTRADA> -o <ARQUIVO_SAIDA> [OPÇÕES]
```

### Exemplos

#### 1. Extração básica para CSV

```bash
python3 extrator_clausulas_cct.py -i convencao.pdf -o clausulas.csv
```

#### 2. Com informações de sindicato e convenção

```bash
python3 extrator_clausulas_cct.py \
    -i CCTFISIOTERAPIA2025-2026HCM.pdf \
    -o clausulas_fisio.csv \
    -s "FISIOTERAPEUTAS/T.O." \
    -c "MARINGÁ 2025/2026"
```

#### 3. Extrair apenas as primeiras 18 cláusulas

```bash
python3 extrator_clausulas_cct.py \
    -i convencao.pdf \
    -o clausulas.csv \
    --limite 18
```

#### 4. Para PDFs escaneados (usar OCR)

```bash
python3 extrator_clausulas_cct.py \
    -i convencao_escaneada.pdf \
    -o clausulas.csv \
    --ocr
```

#### 5. Exportar em formato TXT

```bash
python3 extrator_clausulas_cct.py \
    -i convencao.pdf \
    -o clausulas.txt \
    -s "FARMACÊUTICOS" \
    -c "MARINGA 2023"
```

## Parâmetros

| Parâmetro | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `-i`, `--input` | Sim | Arquivo PDF de entrada (convenção coletiva) |
| `-o`, `--output` | Sim | Arquivo de saída (CSV ou TXT) |
| `-s`, `--sindicato` | Não | Nome do sindicato |
| `-c`, `--convencao` | Não | Nome/ano da convenção (ex: MARINGA 2023) |
| `--ocr` | Não | Forçar uso de OCR para PDFs escaneados |
| `--limite` | Não | Limitar número de cláusulas extraídas |

## Formato de Saída

### CSV

O arquivo CSV gerado contém as seguintes colunas:

| Coluna | Descrição |
|--------|-----------|
| Sindicato | Nome do sindicato |
| Convenção | Nome/ano da convenção |
| Título da Cláusula | Título completo da cláusula (ex: CLÁUSULA PRIMEIRA - VIGÊNCIA) |
| Resumo | Resumo automático da cláusula (primeiras linhas) |
| Cláusula Completa | Texto completo da cláusula |

Exemplo:
```csv
Sindicato,Convenção,Título da Cláusula,Resumo,Cláusula Completa
FISIOTERAPEUTAS/T.O.,MARINGÁ 2025/2026,CLÁUSULA PRIMEIRA - VIGÊNCIA E DATA-BASE,"As partes fixam a vigência...","As partes fixam a vigência da presente Convenção..."
```

### TXT

O arquivo TXT é formatado para fácil leitura, com separadores visuais entre as cláusulas.

## Como Funciona

1. **Extração de Texto**: O script primeiro tenta extrair texto nativo do PDF usando `pdfplumber`
2. **OCR (se necessário)**: Se o PDF for escaneado ou tiver pouco texto, pode usar OCR com `pytesseract`
3. **Identificação de Cláusulas**: Usa expressões regulares para identificar padrões como "CLÁUSULA PRIMEIRA", "CLÁUSULA DÉCIMA SEGUNDA", etc.
4. **Extração de Conteúdo**: Extrai o texto completo de cada cláusula (do título até a próxima cláusula)
5. **Geração de Resumo**: Cria automaticamente um resumo das primeiras linhas de cada cláusula
6. **Exportação**: Salva os dados no formato CSV ou TXT

## Padrões Reconhecidos

O script reconhece cláusulas numeradas por extenso:

- PRIMEIRA, SEGUNDA, TERCEIRA, ..., NONA
- DÉCIMA, DÉCIMA PRIMEIRA, ..., DÉCIMA NONA
- VIGÉSIMA, VIGÉSIMA PRIMEIRA, ..., VIGÉSIMA NONA
- TRIGÉSIMA, TRIGÉSIMA PRIMEIRA, ..., TRIGÉSIMA NONA
- QUADRAGÉSIMA, QUADRAGÉSIMA PRIMEIRA, ..., QUADRAGÉSIMA NONA
- QUINQUAGÉSIMA, QUINQUAGÉSIMA PRIMEIRA, ..., QUINQUAGÉSIMA NONA

## Integração com Streamlit

O formato CSV gerado é ideal para uso em aplicações Streamlit:

```python
import streamlit as st
import pandas as pd

# Carregar dados
df = pd.read_csv('clausulas.csv')

# Filtrar por sindicato
sindicato = st.selectbox('Selecione o Sindicato', df['Sindicato'].unique())
df_filtrado = df[df['Sindicato'] == sindicato]

# Exibir cláusulas
for idx, row in df_filtrado.iterrows():
    st.subheader(row['Título da Cláusula'])
    st.write(f"**Resumo:** {row['Resumo']}")
    with st.expander("Ver texto completo"):
        st.write(row['Cláusula Completa'])
```

## Solução de Problemas

### Nenhuma cláusula encontrada

- Verifique se o PDF contém cláusulas no formato esperado (CLÁUSULA PRIMEIRA, etc.)
- Se o PDF for escaneado, use a opção `--ocr`
- Verifique se o PDF não está protegido ou corrompido

### Texto extraído está incompleto ou incorreto

- Para PDFs escaneados, sempre use `--ocr`
- Verifique a qualidade da digitalização do PDF
- Para PDFs com layout complexo, pode ser necessário ajustar o script

### Erro de OCR

- Certifique-se de que o Tesseract está instalado: `tesseract --version`
- Instale o pacote de idioma português: `sudo apt-get install tesseract-ocr-por`
- Verifique se o poppler-utils está instalado: `pdftoppm -v`

## Limitações

- O script identifica cláusulas baseado em padrões de texto. PDFs com formatação muito diferente podem requerer ajustes
- OCR pode não ser 100% preciso, especialmente para PDFs de baixa qualidade
- Cláusulas com numeração diferente do padrão (ex: números arábicos) não serão reconhecidas automaticamente

## Melhorias Futuras

- Suporte a mais padrões de numeração de cláusulas
- Detecção automática de sindicato e convenção a partir do PDF
- Interface gráfica (GUI)
- Processamento em lote de múltiplos PDFs
- Exportação para outros formatos (Excel, JSON, etc.)

## Licença

Este script é fornecido como está, sem garantias. Sinta-se livre para modificar e adaptar às suas necessidades.

## Suporte

Para dúvidas ou problemas, verifique:
1. Se todas as dependências estão instaladas corretamente
2. Se o PDF está acessível e não corrompido
3. Se o formato do PDF segue os padrões esperados

---

**Desenvolvido para facilitar a organização e consulta de Convenções Coletivas de Trabalho**

