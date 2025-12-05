# 📦 Extrator de CCTs - Versão Standalone (Aplicativo)

## 🎯 Sobre Este Aplicativo

Este é um **aplicativo standalone** para extrair dados de Convenções Coletivas de Trabalho (CCTs) em PDF e gerar arquivos CSV prontos para uso.

**Características**:
- ✅ **Não precisa de Python** instalado
- ✅ **Interface gráfica** (Windows Explorer)
- ✅ **Configuração de API key** via interface
- ✅ **Qualidade profissional** com Tesseract OCR
- ✅ **Portátil** - funciona em qualquer Windows

---

## 📋 Requisitos

### Obrigatório

**Tesseract OCR** - Para extração de texto de alta qualidade

### Opcional

**API Key da OpenAI** - Para resumos profissionais com IA

---

## 🚀 Instalação

### 1. Instalar Tesseract OCR

#### Windows

1. **Baixe o instalador**:
   - Acesse: https://github.com/UB-Mannheim/tesseract/wiki
   - Baixe: `tesseract-ocr-w64-setup-5.x.x.exe`

2. **Execute o instalador**:
   - Durante a instalação, marque:
     - ✅ "Additional language data (download)"
     - ✅ Selecione **Portuguese** (por)
   - Complete a instalação

3. **Verifique a instalação**:
   - Abra o Prompt de Comando
   - Digite: `tesseract --version`
   - Deve mostrar a versão instalada

### 2. Executar o Aplicativo

1. **Duplo clique** em `ExtratorCCT.exe`

2. **Primeira execução**:
   - Uma janela de configuração aparecerá
   - Você pode:
     - **Inserir API key da OpenAI** (opcional)
     - **Pular** e usar sem IA

3. **Pronto!** O aplicativo está configurado

---

## 💻 Como Usar

### Passo 1: Executar

Duplo clique em `ExtratorCCT.exe`

### Passo 2: Selecionar PDF

- Janela do Windows Explorer abre
- Navegue até o PDF da CCT
- Clique em "Abrir"

### Passo 3: Escolher Destino

- Janela "Salvar Como" abre
- Nome é sugerido automaticamente
- Escolha a pasta
- Clique em "Salvar"

### Passo 4: Aguardar

⏳ O OCR leva tempo (3-5 minutos para 17 páginas)

**Progresso mostrado no console** (se habilitado)

### Passo 5: Pronto!

Pop-up de sucesso aparece com:
- Nome do arquivo gerado
- Número de cláusulas extraídas
- Período da convenção

---

## ⚙️ Configuração da API Key da OpenAI

### Primeira Execução

Na primeira vez que executar, uma janela de configuração aparece:

1. **Inserir API key** (opcional):
   - Cole sua API key da OpenAI
   - Clique em "Salvar"

2. **Pular** (usar sem IA):
   - Clique em "Pular (usar sem IA)"
   - Resumos serão simples (primeiras frases)

### Alterar Configuração Depois

As configurações são salvas em:
- **Windows**: `C:\Users\[SeuUsuário]\AppData\Roaming\ExtratorCCT\config.json`

Você pode:
1. Deletar o arquivo `config.json` para reconfigurar
2. Editar manualmente o arquivo JSON

### Obter API Key

1. Acesse: https://platform.openai.com/api-keys
2. Faça login ou crie uma conta
3. Clique em "Create new secret key"
4. Copie a chave (começa com `sk-proj-...`)
5. Cole na janela de configuração

**Com API key**: Resumos profissionais com IA ⭐  
**Sem API key**: Resumos simples (funciona normalmente)

---

## 📊 Distribuição para Outros Computadores

### O Que Distribuir

1. **ExtratorCCT.exe** - O aplicativo
2. **README_STANDALONE.md** - Este arquivo (documentação)
3. **INSTALACAO_TESSERACT.pdf** (opcional) - Guia de instalação do Tesseract

### Instruções para Usuários Finais

1. **Instale o Tesseract OCR** (obrigatório)
   - Siga as instruções acima
   - Link: https://github.com/UB-Mannheim/tesseract/wiki

2. **Execute o aplicativo**:
   - Duplo clique em `ExtratorCCT.exe`

3. **Configure na primeira execução**:
   - Insira API key da OpenAI (opcional)
   - Ou pule para usar sem IA

4. **Use normalmente**:
   - Selecione PDF
   - Escolha onde salvar CSV
   - Aguarde processamento
   - Pronto!

---

## 🆘 Solução de Problemas

### Problema: "Tesseract OCR não encontrado"

**Solução**:
1. Certifique-se de que o Tesseract está instalado
2. Reinstale o Tesseract se necessário
3. Verifique se está no PATH do Windows

**Como verificar**:
- Abra o Prompt de Comando
- Digite: `tesseract --version`
- Deve mostrar a versão

### Problema: "Aplicativo não abre"

**Solução**:
1. Verifique se o Windows Defender não bloqueou
2. Clique com botão direito → "Executar como administrador"
3. Verifique se há antivírus bloqueando

### Problema: "Muito lento"

**Solução**:
- OCR é lento mesmo! É normal.
- 17 páginas = ~3-5 minutos
- A qualidade vale a pena!

### Problema: "API key inválida"

**Solução**:
1. Verifique se copiou a chave completa
2. Gere uma nova chave no site da OpenAI
3. Delete `config.json` e reconfigure

**Localização do config.json**:
- `C:\Users\[SeuUsuário]\AppData\Roaming\ExtratorCCT\config.json`

### Problema: "Erro ao processar PDF"

**Solução**:
1. Verifique se o PDF não está corrompido
2. Tente abrir o PDF em outro leitor
3. Verifique se o PDF não está protegido por senha

---

## 📋 Formato do CSV Gerado

O CSV contém 5 colunas:

| Coluna | Descrição |
|--------|-----------|
| **Sindicato** | Nome do sindicato dos empregados |
| **Convenção** | Período da convenção (AAAA/AAAA) |
| **Título da Cláusula** | Título normalizado da cláusula |
| **Resumo** | Resumo (IA ou simples) |
| **Cláusula Completa** | Texto completo da cláusula |

**Compatível com**:
- ✅ Microsoft Excel
- ✅ Google Sheets
- ✅ LibreOffice Calc
- ✅ pandas (Python)
- ✅ Qualquer leitor CSV

---

## 💡 Dicas de Uso

### ✅ Faça

- Instale o Tesseract antes de usar
- Configure a API key para resumos melhores
- Aguarde pacientemente o OCR (vale a pena!)
- Valide o CSV gerado antes de integrar
- Mantenha backups dos PDFs originais

### ❌ Evite

- Não cancele o OCR no meio (perderá o progresso)
- Não processe PDFs gigantes (100+ páginas)
- Não use PDFs protegidos por senha
- Não use PDFs corrompidos ou ilegíveis

---

## 🔒 Privacidade e Segurança

### Dados Locais

- **Configurações**: Salvas localmente em `AppData\Roaming\ExtratorCCT`
- **API Key**: Armazenada localmente (nunca enviada para terceiros)
- **PDFs**: Processados localmente (nunca enviados para servidores)

### Uso da OpenAI

Se você configurar a API key:
- **Resumos**: Apenas o texto das cláusulas é enviado para a OpenAI
- **Não enviamos**: PDFs completos, dados pessoais, ou informações sensíveis
- **Você controla**: Pode usar sem IA (sem enviar nada)

---

## 📊 Comparação: Com IA vs Sem IA

| Aspecto | Com OpenAI ⭐ | Sem OpenAI |
|---------|--------------|------------|
| **Resumos** | Profissionais, contextualizados | Simples (primeiras frases) |
| **Qualidade** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Custo** | Requer API key (pago) | Gratuito |
| **Privacidade** | Envia texto para OpenAI | 100% local |
| **Velocidade** | Mais lento (~5-10s por cláusula) | Rápido (instantâneo) |

**Recomendação**: Use com OpenAI para qualidade profissional! 🎯

---

## 🎓 Perguntas Frequentes (FAQ)

### 1. Preciso de Python instalado?

**Não!** O executável já contém tudo que precisa.

### 2. Preciso de internet?

**Sim**, se usar OpenAI para resumos.  
**Não**, se usar sem IA (resumos simples).

### 3. Funciona no Mac ou Linux?

**Não**, este executável é apenas para Windows.  
Use a versão Python para Mac/Linux.

### 4. Quanto custa a API da OpenAI?

Varia conforme uso. Consulte: https://openai.com/pricing  
Para CCTs típicas: ~$0.01-0.05 por documento.

### 5. Posso processar múltiplos PDFs de uma vez?

Não nesta versão. Processe um por vez.

### 6. O aplicativo é seguro?

Sim! Todo o código está disponível para revisão.  
Nenhum dado é enviado para terceiros (exceto OpenAI se configurado).

### 7. Posso usar comercialmente?

Sim! O aplicativo é gratuito para uso pessoal e comercial.

---

## 🏆 Vantagens da Versão Standalone

1. ✅ **Não precisa de Python** - Executável standalone
2. ✅ **Fácil distribuição** - Um único arquivo .exe
3. ✅ **Interface gráfica** - Windows Explorer integrado
4. ✅ **Configuração simples** - API key via interface
5. ✅ **Qualidade profissional** - Tesseract OCR
6. ✅ **Portátil** - Funciona em qualquer Windows

---

## 📞 Suporte

### Problemas Técnicos

Consulte a seção **Solução de Problemas** acima.

### Melhorias e Sugestões

Sugestões são bem-vindas!

---

## 🎉 Conclusão

O **Extrator de CCTs Standalone** é a solução completa para extrair dados de CCTs com qualidade profissional.

**Requisitos**:
- ✅ Windows 10/11
- ✅ Tesseract OCR instalado
- ✅ (Opcional) API key da OpenAI

**Tempo**: ~3-5 minutos por documento  
**Qualidade**: ⭐⭐⭐⭐⭐ PROFISSIONAL

**Pronto para uso em qualquer computador!** 🚀

---

**Versão**: Standalone 1.0  
**Data**: Dezembro 2024  
**Autor**: Manus AI  
**Status**: ✅ Produção
