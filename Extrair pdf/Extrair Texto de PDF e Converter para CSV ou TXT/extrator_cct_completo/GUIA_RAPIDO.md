# 🚀 Guia Rápido - Extrator de Cláusulas CCT

## Instalação Rápida

```bash
# 1. Instalar dependência principal
pip3 install pdfplumber

# 2. (Opcional) Para PDFs escaneados, instalar OCR
pip3 install pdf2image pytesseract
sudo apt-get install tesseract-ocr tesseract-ocr-por poppler-utils
```

## Uso Básico

### Extrair cláusulas de um PDF

```bash
python3 extrator_clausulas_cct.py \
    -i seu_arquivo.pdf \
    -o clausulas.csv \
    -s "NOME DO SINDICATO" \
    -c "ANO DA CONVENÇÃO"
```

### Exemplo Real

```bash
python3 extrator_clausulas_cct.py \
    -i CCTFISIOTERAPIA2025-2026HCM.pdf \
    -o clausulas_fisio.csv \
    -s "FISIOTERAPEUTAS/T.O." \
    -c "MARINGÁ 2025/2026"
```

### Extrair apenas primeiras N cláusulas

```bash
python3 extrator_clausulas_cct.py \
    -i convencao.pdf \
    -o clausulas.csv \
    --limite 18
```

### Para PDFs escaneados

```bash
python3 extrator_clausulas_cct.py \
    -i convencao_escaneada.pdf \
    -o clausulas.csv \
    --ocr
```

## Usar com Streamlit

### 1. Instalar Streamlit

```bash
pip3 install streamlit pandas
```

### 2. Executar a aplicação

```bash
streamlit run exemplo_streamlit_app.py
```

### 3. Usar a interface

1. Abra o navegador (geralmente abre automaticamente)
2. Faça upload do arquivo CSV gerado pelo extrator
3. Use os filtros para buscar cláusulas
4. Exporte os resultados filtrados se necessário

## Estrutura dos Arquivos

```
extrator_cct_completo.zip
├── extrator_clausulas_cct.py    # Script principal de extração
├── exemplo_streamlit_app.py      # Aplicação Streamlit de exemplo
├── README_EXTRATOR_CCT.md        # Documentação completa
└── clausulas_fisio_completo.csv  # Exemplo de saída (55 cláusulas)
```

## Formato do CSV Gerado

| Coluna | Descrição |
|--------|-----------|
| Sindicato | Nome do sindicato |
| Convenção | Nome/ano da convenção |
| Título da Cláusula | Título completo (ex: CLÁUSULA PRIMEIRA - VIGÊNCIA) |
| Resumo | Resumo automático da cláusula |
| Cláusula Completa | Texto completo da cláusula |

## Dicas

✅ **PDFs com texto**: Não precisa de OCR, extração é rápida  
✅ **PDFs escaneados**: Use `--ocr` para melhor resultado  
✅ **Múltiplos PDFs**: Rode o script para cada PDF e depois combine os CSVs  
✅ **Streamlit**: Ideal para criar interface de consulta para usuários finais  

## Solução de Problemas

**Nenhuma cláusula encontrada?**
- Verifique se as cláusulas estão no formato "CLÁUSULA PRIMEIRA - TÍTULO"
- Tente usar `--ocr` se o PDF for escaneado

**Erro ao importar bibliotecas?**
- Certifique-se de ter instalado: `pip3 install pdfplumber`
- Para OCR: `pip3 install pdf2image pytesseract`

**OCR não funciona?**
- Instale o Tesseract: `sudo apt-get install tesseract-ocr tesseract-ocr-por`
- Instale o poppler: `sudo apt-get install poppler-utils`

## Próximos Passos

1. ✅ Extrair cláusulas de todos os seus PDFs de CCT
2. ✅ Combinar todos os CSVs em um único arquivo
3. ✅ Criar aplicação Streamlit personalizada
4. ✅ Compartilhar com sua equipe

---

**Precisa de ajuda?** Consulte o `README_EXTRATOR_CCT.md` para documentação completa.

