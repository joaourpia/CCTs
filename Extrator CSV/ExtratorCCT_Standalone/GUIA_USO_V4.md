# 🚀 Guia Rápido - Versão 4.0

## ✨ Novidades Principais

1. **Barra de progresso visual** - Veja o que está acontecendo
2. **Janela de confirmação** - Revise antes de integrar
3. **Integração automática** - Sem copiar e colar manual

---

## 📋 Como Usar (Passo a Passo)

### 1️⃣ Executar o Aplicativo

**Duplo clique** em `ExtratorCCT.exe`

ou

```bash
python extrator_cct_v4.py
```

---

### 2️⃣ Configuração Inicial (Primeira Vez)

Se for a primeira execução, uma janela aparece:

```
┌─────────────────────────────────────┐
│ Configuração Inicial                │
├─────────────────────────────────────┤
│ API Key da OpenAI:                  │
│ [sk-proj-xxxxx...]                  │
│                                     │
│ [ ] Mostrar API key                 │
│                                     │
│ [Salvar] [Pular (usar sem IA)]      │
└─────────────────────────────────────┘
```

**Opções**:
- **Salvar**: Com resumos de IA (recomendado)
- **Pular**: Sem IA (resumos simples)

---

### 3️⃣ Selecionar PDF

Janela do Windows Explorer abre:

```
Selecione o arquivo PDF da CCT
```

**Navegue** até o PDF e **selecione**.

---

### 4️⃣ Barra de Progresso (NOVO! ⭐)

Uma janela aparece mostrando o progresso:

```
┌─────────────────────────────────────┐
│ Extrator de CCTs                    │
├─────────────────────────────────────┤
│ Extraindo texto do PDF...           │
│                                     │
│ ████████░░░░░░░░░░░░░░░░ 35%        │
│                                     │
│ 35%                                 │
└─────────────────────────────────────┘
```

**Etapas mostradas**:
- Extraindo texto do PDF... (0-30%)
- Identificando sindicato... (30-40%)
- Extraindo cláusulas... (40-70%)
- Gerando resumos... (70-95%)
- Salvando CSV... (95-100%)

**Aguarde** até 100%!

---

### 5️⃣ Confirmar Sindicato

Janela aparece com opções:

```
┌─────────────────────────────────────┐
│ Confirmar Sindicato                 │
├─────────────────────────────────────┤
│ Detectado:                          │
│ SINDICATO DOS FARMACÊUTICOS...      │
│                                     │
│ Outros encontrados:                 │
│ ○ SINDICATO DAS SANTAS CASAS        │
│ ● SINDICATO DOS FARMACÊUTICOS       │
│                                     │
│ Ou digite:                          │
│ [SINDICATO DOS FARMACÊUTICOS...]    │
│                                     │
│ [✅ Confirmar]                       │
└─────────────────────────────────────┘
```

**Escolha** o sindicato correto e clique **Confirmar**.

---

### 6️⃣ Aguardar Processamento

Barra de progresso continua:

```
Gerando resumos... 85%
```

**Aguarde** até concluir!

---

### 7️⃣ Janela de Confirmação (NOVO! ⭐)

Após concluir, janela aparece:

```
┌─────────────────────────────────────────────────┐
│ ✅ Extração Concluída!                          │
├─────────────────────────────────────────────────┤
│ Sindicato: SINDICATO DOS FARMACÊUTICOS...       │
│ Convenção: 2025-2027                            │
│ Cláusulas: 25                                   │
│ CSV: C:\Users\...\SINDIFARMA_2025.csv           │
├─────────────────────────────────────────────────┤
│ [📄 Abrir CSV] [🔗 Integrar] [❌ Fechar]         │
└─────────────────────────────────────────────────┘
```

**Opções**:

1. **📄 Abrir CSV**: Abre no Excel para revisar
2. **🔗 Integrar**: Integra com planilha mãe
3. **❌ Fechar**: Fecha sem integrar

---

### 8️⃣ Revisar CSV (Opcional)

Se clicar em **"Abrir CSV"**:

1. Excel/LibreOffice abre
2. **Revise** os dados
3. **Feche** o Excel
4. **Volte** para a janela de confirmação
5. Clique em **"Integrar"** ou **"Fechar"**

---

### 9️⃣ Integrar com Planilha Mãe (NOVO! ⭐)

Se clicar em **"Integrar"**:

#### Opção A: Planilha Mãe no Mesmo Diretório

Se `CCTs_Extraidas.csv` estiver na mesma pasta:

```
✅ Planilha mãe encontrada!
CCTs_Extraidas.csv

Deseja usar esta planilha?
[Sim] [Não, selecionar outra]
```

**Clique "Sim"** para usar automaticamente.

#### Opção B: Selecionar Manualmente

Se não encontrar ou clicar "Não":

```
Selecione a Planilha Mãe (CCTs_Extraidas.csv)
```

Windows Explorer abre → **Navegue** e **selecione**.

---

### 🔟 Confirmação de Sucesso

Após integrar:

```
┌─────────────────────────────────────┐
│ ✅ Sucesso!                          │
├─────────────────────────────────────┤
│ 25 cláusulas adicionadas à          │
│ planilha mãe!                       │
│                                     │
│ Backup criado:                      │
│ CCTs_Extraidas_backup_20241204.csv  │
│                                     │
│ [OK]                                │
└─────────────────────────────────────┘
```

**Pronto!** Dados integrados com sucesso! 🎉

---

## 💡 Dicas Importantes

### ✅ Boas Práticas

1. **Sempre revise** o CSV antes de integrar
2. **Mantenha** a planilha mãe na mesma pasta do executável
3. **Não interrompa** durante o processamento
4. **Aguarde** a barra de progresso chegar a 100%

### ⚠️ Atenções

1. **Não feche** a barra de progresso manualmente
2. **Não mova** arquivos durante o processamento
3. **Revise** antes de integrar (evita retrabalho)
4. **Backup** é criado automaticamente (segurança)

---

## 🔧 Localização da Planilha Mãe

### Estratégia Automática

O aplicativo procura nesta ordem:

1. **Mesma pasta** do executável → `CCTs_Extraidas.csv`
2. **Caminho salvo** no config (última vez usada)
3. **Pergunta** ao usuário (Windows Explorer)

### Recomendação

**Coloque a planilha mãe na mesma pasta do executável!**

```
📁 Pasta do Aplicativo/
├── ExtratorCCT.exe
├── CCTs_Extraidas.csv  ← AQUI!
└── tesseract/ (se portátil)
```

**Vantagem**: Integração automática sem perguntar!

---

## 📊 Fluxo Completo Resumido

```
1. Execute → 2. Configure (1ª vez) → 3. Selecione PDF
   ↓
4. [NOVO] Barra de progresso (30s-3min)
   ↓
5. Confirme sindicato
   ↓
6. [NOVO] Barra de progresso continua
   ↓
7. [NOVO] Janela de confirmação
   ↓
8. [OPCIONAL] Revise CSV
   ↓
9. [NOVO] Integre automaticamente
   ↓
10. [NOVO] Sucesso! Backup criado
```

**Tempo total**: 2-5 minutos (depende do tamanho do PDF)

---

## 🆘 Problemas Comuns

### Problema 1: Barra de progresso trava

**Sintoma**: Barra para em 50% e não avança

**Causa**: PDF muito grande ou OCR demorado

**Solução**: Aguarde! Pode levar até 5 minutos

---

### Problema 2: Planilha mãe não encontrada

**Sintoma**: Sempre pede para selecionar manualmente

**Causa**: Planilha não está na mesma pasta

**Solução**: 
1. Mova `CCTs_Extraidas.csv` para a pasta do executável
2. **OU** selecione manualmente (será lembrado)

---

### Problema 3: Erro ao integrar

**Sintoma**: "Estrutura do CSV não corresponde"

**Causa**: Planilha mãe tem colunas diferentes

**Solução**:
1. Verifique se tem 5 colunas
2. Use a planilha mãe fornecida
3. Não modifique os nomes das colunas

---

### Problema 4: Backup não criado

**Sintoma**: Mensagem de erro ao criar backup

**Causa**: Sem permissão de escrita

**Solução**:
1. Execute como administrador
2. Verifique permissões da pasta

---

## 📋 Checklist Antes de Usar

- [ ] Tesseract OCR instalado
- [ ] API Key configurada (opcional)
- [ ] Planilha mãe na pasta correta
- [ ] PDF válido selecionado
- [ ] Espaço em disco suficiente

---

## 🎉 Resumo

**Versão 4.0** é profissional e fácil de usar:

1. ✅ **Barra de progresso** - Sabe o que está acontecendo
2. ✅ **Janela de confirmação** - Revisa antes de integrar
3. ✅ **Integração automática** - Sem erros manuais
4. ✅ **Backup automático** - Segurança garantida
5. ✅ **Inteligente** - Encontra a planilha mãe sozinho

**Pronto para uso profissional!** 🚀

---

**Versão**: 4.0  
**Data**: Dezembro 2024  
**Status**: ✅ Pronto para produção
