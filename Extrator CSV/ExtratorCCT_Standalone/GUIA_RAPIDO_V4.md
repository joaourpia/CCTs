# 🚀 Guia Rápido - Extrator CCT v4.0 FINAL

## ⚡ Início Rápido

### 1️⃣ Executar o Programa

**Opção A: Executável Windows**
```
1. Duplo clique em ExtratorCCT.exe
2. Aguarde janela de seleção de PDF
```

**Opção B: Python**
```bash
python extrator_cct_standalone.py
```

---

### 2️⃣ Selecionar PDF da CCT

```
┌────────────────────────────────┐
│ Selecione o arquivo PDF       │
│                                │
│ 📁 Meus Documentos             │
│   └─ CCT_2025.pdf         [✓] │
│                                │
│        [Abrir] [Cancelar]      │
└────────────────────────────────┘
```

---

### 3️⃣ Escolher/Editar Sindicato

```
┌────────────────────────────────┐
│ Selecione o Sindicato          │
│                                │
│ Sindicatos Conhecidos:         │
│ ○ SINDIFIBA                    │
│ ○ SINDIMED                     │
│ ○ SINDICATO DOS COMERCIÁRIOS  │
│ ● Outro (digitar abaixo)       │
│                                │
│ Nome: [SINDIFARMACIA_______]   │
│                                │
│         [Confirmar]            │
└────────────────────────────────┘
```

**Dica**: Você pode editar qualquer nome antes de confirmar!

---

### 4️⃣ Aguardar Processamento

Uma barra de progresso aparecerá:

```
┌────────────────────────────────┐
│ Extraindo Dados da CCT         │
│                                │
│ ████████████░░░░░░░░  50%      │
│                                │
│ Extraindo cláusulas...         │
└────────────────────────────────┘
```

**Etapas**:
- 10% - Extraindo texto do PDF
- 30% - Identificando sindicato e convenção
- 50% - Extraindo cláusulas
- 90% - Salvando CSV
- 100% - Concluído!

---

### 5️⃣ Escolher Ação

Após extração, você verá:

```
┌─────────────────────────────────────────┐
│  ✅ CSV Gerado com Sucesso!             │
│                                         │
│  📄 Arquivo: clausulas_sindifiba.csv    │
│  📊 Cláusulas extraídas: 42             │
│  📑 Convenção: CCT 2025-2026            │
│                                         │
│  O que deseja fazer?                    │
│                                         │
│  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │Abrir CSV │  │ Integrar │  │ Fechar ││
│  └──────────┘  └──────────┘  └────────┘│
└─────────────────────────────────────────┘
```

**Opções**:

#### 🔹 Abrir CSV
- Abre o arquivo no Excel/editor padrão
- Permite revisar dados extraídos
- Útil para validação manual

#### 🔹 Integrar
- Adiciona dados à planilha mãe
- Cria backup automático
- Valida estrutura antes de integrar

#### 🔹 Fechar
- Encerra o programa
- Mantém CSV gerado no disco

---

### 6️⃣ Integrar com Planilha Mãe (Opcional)

Se escolher "Integrar":

**Passo 1**: Selecionar planilha mãe
```
┌────────────────────────────────┐
│ Selecione a Planilha Mãe      │
│                                │
│ 📁 Documentos                  │
│   └─ CCTs_Extraidas.csv   [✓] │
│                                │
│        [Abrir] [Cancelar]      │
└────────────────────────────────┘
```

**Passo 2**: Sistema processa automaticamente
- ✅ Cria backup: `CCTs_Extraidas_backup_20251204_161530.csv`
- ✅ Valida estrutura (5 colunas)
- ✅ Adiciona novos dados no final
- ✅ Preserva dados existentes

**Passo 3**: Confirmação
```
┌────────────────────────────────┐
│ ✅ Sucesso!                    │
│                                │
│ Integração concluída!          │
│                                │
│ • Backup criado                │
│ • 42 cláusulas adicionadas     │
│ • Planilha atualizada          │
│                                │
│            [OK]                │
└────────────────────────────────┘
```

---

## 📋 Estrutura do CSV Gerado

O arquivo CSV terá 5 colunas:

| Sindicato | Convenção | Título da Cláusula | Resumo | Cláusula Completa |
|-----------|-----------|-------------------|--------|-------------------|
| SINDIFIBA | CCT 2025-2026 | CLÁUSULA PRIMEIRA - ABRANGÊNCIA | Define abrangência... | CLÁUSULA PRIMEIRA... |

**Formato**:
- Encoding: UTF-8 com BOM
- Separador: vírgula (,)
- Compatível com Excel, Google Sheets, Pandas

---

## 🛡️ Backup Automático

Antes de modificar a planilha mãe, o sistema cria backup:

```
CCTs_Extraidas.csv
  ↓
CCTs_Extraidas_backup_20251204_161530.csv
```

**Formato do nome**: `{original}_backup_{AAAAMMDD}_{HHMMSS}.csv`

---

## ❓ Perguntas Frequentes

### O CSV não abre no Excel?
**Solução**: Abra Excel → Dados → Importar de Texto/CSV → Selecione UTF-8

### Barra de progresso não aparece?
**Solução**: Aguarde alguns segundos, pode estar carregando PDF grande

### Integração falhou?
**Solução**: Verifique se planilha mãe tem 5 colunas:
- Sindicato
- Convenção
- Título da Cláusula
- Resumo
- Cláusula Completa

### Backup não foi criado?
**Solução**: Verifique permissões de escrita na pasta da planilha mãe

---

## 🎯 Dicas de Uso

### ✅ Boas Práticas

1. **Sempre revise o CSV** antes de integrar
2. **Mantenha backups** em local seguro
3. **Use nomes descritivos** para sindicatos
4. **Valide dados** periodicamente

### ⚠️ Evite

1. ❌ Fechar janela de progresso durante processamento
2. ❌ Modificar CSV enquanto programa está aberto
3. ❌ Deletar backups imediatamente
4. ❌ Usar caracteres especiais em nomes de arquivo

---

## 📞 Suporte

**Documentação Completa**:
- `VERSAO_4.0_FINAL.md` - Detalhes técnicos
- `GUIA_USO_V4.md` - Guia completo
- `CHANGELOG.md` - Histórico de versões

**Problemas Técnicos**:
- Verifique `IMPLEMENTACAO_V4.md`
- Consulte `README_STANDALONE.md`

---

**Versão**: 4.0 FINAL  
**Atualizado**: 04/12/2025  
**Tempo médio de processamento**: 30-60 segundos por PDF
