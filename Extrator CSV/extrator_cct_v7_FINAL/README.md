# 📚 Extrator de CCTs - Versão 7 Final

## 🎯 Novidades da Versão 7

### ✨ Interface Gráfica com Windows Explorer

✅ **Seleção de arquivo PDF** - Janela do Windows Explorer  
✅ **Seleção de local para salvar CSV** - Janela "Salvar Como"  
✅ **OpenAI por padrão** - Não pergunta mais, usa automaticamente se configurado  
✅ **Detecção melhorada de convenção** - Busca em todo o PDF e no nome do arquivo  
✅ **Mensagens de sucesso/erro** - Pop-ups informativos  

---

## 🚀 Como Usar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

**Dependências**:
- `pymupdf` - Extração de texto de PDFs
- `openai` - Geração de resumos com IA
- `tkinter` - Interface gráfica (já vem com Python)

### 2. Executar o Script

**Duplo clique** no arquivo `extrator_cct_v7_final.py`

**Ou via terminal**:
```bash
python extrator_cct_v7_final.py
```

### 3. Usar a Interface

1. **Janela 1**: Selecione o PDF da CCT
   - Navegue pelas pastas
   - Selecione o arquivo PDF
   - Clique em "Abrir"

2. **Janela 2**: Escolha onde salvar o CSV
   - O nome é sugerido automaticamente
   - Escolha a pasta de destino
   - Clique em "Salvar"

3. **Processamento**: Aguarde
   - O script mostra o progresso no terminal
   - Extração de texto
   - Identificação de sindicato e convenção
   - Extração de cláusulas
   - Geração de resumos com IA

4. **Conclusão**: Pop-up de sucesso
   - Mostra quantas cláusulas foram extraídas
   - CSV está pronto para uso!

---

## 🔧 Configuração da OpenAI (Opcional mas Recomendado)

### Por que configurar?

Com OpenAI configurada, os resumos das cláusulas são:
- ✅ Mais elaborados e contextualizados
- ✅ Profissionais e concisos
- ✅ Melhor qualidade geral

Sem OpenAI, o script funciona normalmente mas usa resumos simples (primeiras frases).

### Como configurar

#### Windows

1. Pressione `Win + R`
2. Digite `sysdm.cpl` e pressione Enter
3. Vá para "Avançado" → "Variáveis de Ambiente"
4. Em "Variáveis do usuário", clique em "Novo"
5. Nome: `OPENAI_API_KEY`
6. Valor: `sua-chave-api-aqui`
7. Clique em OK em todas as janelas
8. **Reinicie o terminal/prompt**

#### Linux/macOS

Adicione ao `~/.bashrc` ou `~/.zshrc`:

```bash
export OPENAI_API_KEY="sua-chave-api-aqui"
```

Depois:
```bash
source ~/.bashrc
```

### Obter API Key

1. Acesse: https://platform.openai.com/api-keys
2. Faça login ou crie uma conta
3. Clique em "Create new secret key"
4. Copie a chave (começa com `sk-proj-...`)
5. Configure conforme acima

---

## 📊 Detecção de Convenção

A versão 7 detecta o período da convenção de 3 formas:

### 1. Busca no Texto do PDF (Prioridade 1)

Procura padrões como:
- `2025-2026`
- `2025/2026`
- `CONVENÇÃO COLETIVA 2025-2026`

### 2. Busca de Anos Sequenciais (Prioridade 2)

Encontra dois anos próximos no texto e assume que são o período.

### 3. Nome do Arquivo (Prioridade 3 - Fallback)

Se não encontrar no texto, extrai do nome do arquivo:
- `SINDISAUDE_2025_2026.pdf` → `2025-2026`
- `cct_2025.pdf` → `2025-2026` (assume ano seguinte)
- `CCT_2025_2027.pdf` → `2025-2027`

### ⚠️ Importante

Se a convenção detectada estiver errada:

1. **Renomeie o PDF** com o período correto:
   - Exemplo: `SINDISAUDE_2025_2027.pdf`
   
2. **Ou** verifique se o PDF contém o período correto no texto

O script sempre **garante ordem crescente** dos anos.

---

## ✨ Funcionalidades

### 1. Interface Gráfica

- ✅ Janela de seleção de arquivo (Windows Explorer)
- ✅ Janela "Salvar Como" para CSV
- ✅ Pop-ups de sucesso/erro
- ✅ Não precisa digitar caminhos

### 2. Detecção Inteligente

- ✅ Sindicatos longos (até 300 caracteres)
- ✅ Convenção do texto ou nome do arquivo
- ✅ Normalização automática de erros de OCR

### 3. Correções de OCR

- ✅ **Sindicatos**: `slNDlcATo` → `SINDICATO`
- ✅ **Datas**: `abrill2025` → `abril/2025`
- ✅ **Estados**: `BAHTA` → `BAHIA`
- ✅ **Palavras**: `TRABAI-HADORES` → `TRABALHADORES`
- ✅ **35+ padrões** de correção

### 4. Resumos com IA

- ✅ Usa GPT-4.1-mini por padrão
- ✅ Resumos concisos (máx 200 caracteres)
- ✅ Fallback para resumos simples se IA não disponível

### 5. CSV Compatível

- ✅ Formato compatível com pandas
- ✅ Escape correto de caracteres especiais
- ✅ Sem erros de parsing
- ✅ Pronto para integrar com planilha mãe

---

## 📋 Formato do CSV

O CSV gerado contém 5 colunas:

| Coluna | Descrição |
|--------|-----------|
| **Sindicato** | Nome do sindicato dos empregados (normalizado) |
| **Convenção** | Período da convenção (AAAA-AAAA) |
| **Título da Cláusula** | Título normalizado da cláusula |
| **Resumo** | Resumo gerado (IA ou simples) |
| **Cláusula Completa** | Texto completo da cláusula |

---

## 🆘 Solução de Problemas

### Problema: "Nenhum arquivo selecionado"

**Solução**: Certifique-se de clicar em "Abrir" na janela de seleção.

### Problema: "Convenção errada"

**Solução**: Renomeie o PDF com o período correto (ex: `CCT_2025_2027.pdf`).

### Problema: "OpenAI não disponível"

**Solução**: Configure a variável de ambiente `OPENAI_API_KEY` ou use sem IA (funciona normalmente).

### Problema: "Erro ao abrir janela"

**Solução**: Certifique-se de que `tkinter` está instalado:

```bash
# Windows/macOS: já vem com Python
# Linux (Ubuntu/Debian):
sudo apt-get install python3-tk
```

### Problema: "Sindicato não identificado"

**Solução**: O PDF pode ter formatação muito diferente. Verifique se o sindicato está no início do documento.

---

## 📊 Comparação de Versões

| Recurso | v6 | v7 ⭐ |
|---------|----|----|
| **Interface gráfica** | ❌ | ✅ Windows Explorer |
| **Seleção de arquivo** | Linha de comando | ✅ Janela gráfica |
| **Salvar CSV** | Linha de comando | ✅ Janela "Salvar Como" |
| **Pergunta sobre IA** | ❌ | ✅ Automático |
| **Pop-ups informativos** | ❌ | ✅ |
| **Detecção de convenção** | Básica | ✅ Melhorada (3 estratégias) |
| **Ordem dos anos** | ❌ | ✅ Garantida |

---

## 🎯 Fluxo de Uso

```
1. Executar script
   ↓
2. Selecionar PDF (janela gráfica)
   ↓
3. Escolher onde salvar CSV (janela gráfica)
   ↓
4. Aguardar processamento (terminal mostra progresso)
   ↓
5. Pop-up de sucesso
   ↓
6. CSV pronto!
```

**Simples e rápido!** ⚡

---

## 💡 Dicas

### ✅ Faça

- Nomeie os PDFs com o período correto (ex: `CCT_2025_2027.pdf`)
- Configure OpenAI para resumos melhores
- Valide o CSV gerado antes de integrar
- Mantenha backups da planilha mãe

### ❌ Evite

- PDFs com senha ou corrompidos
- Caminhos com caracteres especiais
- Executar múltiplas instâncias ao mesmo tempo

---

## 📞 Suporte

### Problemas Comuns

Consulte a seção **Solução de Problemas** acima.

### Melhorias

Sugestões são bem-vindas!

---

## 🎉 Conclusão

A **Versão 7** traz a melhor experiência de uso:

✅ **Interface gráfica** - Fácil e intuitiva  
✅ **OpenAI por padrão** - Resumos profissionais  
✅ **Detecção melhorada** - Convenção correta  
✅ **Pop-ups informativos** - Feedback claro  

**Pronto para uso profissional!** 🚀

---

**Versão**: 7.0 Final  
**Data**: Dezembro 2024  
**Autor**: Manus AI
