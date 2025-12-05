# 🚀 Guia Rápido de Uso

## Instalação Rápida

```bash
# 1. Instalar dependências
pip install pdfplumber openai

# 2. Configurar API OpenAI (se for usar IA)
export OPENAI_API_KEY="sua-chave-aqui"
```

## Uso Básico

### Comando Mais Simples

```bash
python extrator_cct_v2.py "sua_cct.pdf" -o "saida.csv"
```

### Sem IA (Mais Rápido)

```bash
python extrator_cct_v2.py "sua_cct.pdf" -o "saida.csv" --sem-ia
```

## Workflow Completo

### 1️⃣ Processar PDF

```bash
python extrator_cct_v2.py "CCT_Medicos_2025.pdf" -o "medicos_2025.csv"
```

**Saída esperada**:
```
======================================================================
🚀 EXTRATOR DE DADOS DE CCTs - VERSÃO 2
======================================================================

📄 Extraindo texto do PDF: CCT_Medicos_2025.pdf
   ✓ Página 1/10 extraída
   ✓ Página 2/10 extraída
   ...
✓ Extração concluída: 25296 caracteres

🔍 Identificando sindicato e convenção...
   Sindicato: SINDICATO DOS MÉDICOS x SINDICATO DAS SANTAS CASAS
   Convenção: 2025-2026

📋 Extraindo cláusulas...
   Encontradas 29 cláusulas

   ✓ Cláusula 1/29: CLÁUSULA PRIMEIRA - VIGÊNCIA...
   ✓ Cláusula 2/29: CLÁUSULA SEGUNDA - ABRANGÊNCIA...
   ...

✓ Total de 29 cláusulas extraídas

💾 Salvando dados em CSV: medicos_2025.csv
✓ Arquivo CSV salvo com sucesso!
   Total de linhas: 29
   Tamanho do arquivo: 32.50 KB

======================================================================
✅ PROCESSO CONCLUÍDO COM SUCESSO!
======================================================================
```

### 2️⃣ Verificar Resultado

Abra o arquivo CSV gerado em Excel, Google Sheets ou qualquer editor de planilhas.

**Verifique**:
- ✅ Sindicato identificado corretamente
- ✅ Ano/período correto
- ✅ Todas as cláusulas capturadas
- ✅ Resumos fazem sentido
- ✅ Conteúdo completo está presente

### 3️⃣ Integrar com Planilha Mãe

**Opção A: Copiar e Colar**

1. Abra `medicos_2025.csv`
2. Selecione todas as linhas **exceto o cabeçalho**
3. Copie (Ctrl+C)
4. Abra `clausulas_farmaceuticos.csv`
5. Vá até a última linha
6. Cole (Ctrl+V)
7. Salve

**Opção B: Concatenar via Comando**

```bash
# Remove cabeçalho e adiciona ao final da planilha mãe
tail -n +2 medicos_2025.csv >> clausulas_farmaceuticos.csv
```

### 4️⃣ Atualizar Streamlit

```bash
# Reinicie o aplicativo Streamlit
streamlit run app.py
```

Pronto! As novas cláusulas estarão disponíveis no aplicativo.

## Exemplos de Comandos

### Processar Vários PDFs

**Linux/Mac**:
```bash
for pdf in *.pdf; do
    echo "Processando: $pdf"
    python extrator_cct_v2.py "$pdf" -o "${pdf%.pdf}.csv"
done
```

**Windows (PowerShell)**:
```powershell
Get-ChildItem *.pdf | ForEach-Object {
    Write-Host "Processando: $($_.Name)"
    python extrator_cct_v2.py $_.FullName -o "$($_.BaseName).csv"
}
```

### Usar Modelo Mais Rápido

```bash
python extrator_cct_v2.py "cct.pdf" -o "saida.csv" --modelo gpt-4.1-nano
```

### Processar Sem IA (Teste Rápido)

```bash
python extrator_cct_v2.py "cct.pdf" -o "saida.csv" --sem-ia
```

## Dicas Importantes

### ✅ Faça Sempre

- ✅ **Backup** da planilha mãe antes de adicionar dados
- ✅ **Revise** os dados extraídos antes de integrar
- ✅ **Teste** com `--sem-ia` primeiro para verificar extração
- ✅ **Mantenha** os PDFs originais como referência

### ❌ Evite

- ❌ Processar PDFs protegidos ou com senha
- ❌ Adicionar dados sem revisar
- ❌ Usar IA para testes rápidos (gasta créditos)
- ❌ Deletar PDFs originais após processamento

## Solução Rápida de Problemas

| Problema | Solução |
|----------|---------|
| "Nenhuma cláusula encontrada" | Verifique se o PDF tem texto selecionável |
| "Erro de API OpenAI" | Use `--sem-ia` ou configure `OPENAI_API_KEY` |
| "Caracteres estranhos no CSV" | Abra com encoding UTF-8 |
| "Poucas cláusulas extraídas" | PDF pode ter formatação não padrão |

## Ajuda Rápida

```bash
# Ver todas as opções
python extrator_cct_v2.py --help

# Versão simples (sem IA)
python extrator_cct_v2.py arquivo.pdf -o saida.csv --sem-ia

# Versão completa (com IA)
python extrator_cct_v2.py arquivo.pdf -o saida.csv
```

## Estrutura do CSV Gerado

```
Sindicato | Convenção | Título da Cláusula | Resumo | Cláusula Completa
----------|-----------|-------------------|---------|-------------------
SIND...   | 2025-2026 | CLÁUSULA PRIMEIRA | Define...| As partes...
```

## Próximos Passos

1. ✅ Processar seu primeiro PDF
2. ✅ Verificar o CSV gerado
3. ✅ Integrar com a planilha mãe
4. ✅ Testar no Streamlit
5. ✅ Processar demais CCTs

---

**Dúvidas?** Consulte o `README.md` completo para mais detalhes.
