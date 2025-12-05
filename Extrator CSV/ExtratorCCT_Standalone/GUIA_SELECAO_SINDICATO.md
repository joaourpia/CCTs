# 📋 Guia: Seleção de Sindicato

## 🎯 Nova Funcionalidade (v3.0)

A partir da versão 3.0, o extrator permite que você **confirme ou escolha** o sindicato dos empregados antes de processar o PDF.

---

## 🖼️ Como Funciona

### 1️⃣ Detecção Automática

O script tenta detectar automaticamente o sindicato dos empregados no PDF.

**Se detectar**:
- Mostra o sindicato encontrado em destaque (verde)
- Você pode confirmar ou escolher outro

**Se NÃO detectar**:
- Mostra "SINDICATO NÃO IDENTIFICADO"
- Você DEVE escolher da lista ou digitar manualmente

---

### 2️⃣ Janela de Confirmação

Após a detecção, uma janela aparece com:

#### 📌 Seção 1: Sindicato Detectado Automaticamente

```
┌─────────────────────────────────────────────────┐
│ Sindicato Detectado Automaticamente             │
├─────────────────────────────────────────────────┤
│ SINDICATO DOS ENFERMEIROS DO ESTADO DA BAHIA    │
└─────────────────────────────────────────────────┘
```

**Verde** = Detectado com sucesso  
**Vermelho** = Não detectado

#### 📌 Seção 2: Outros Sindicatos Encontrados no PDF

```
┌─────────────────────────────────────────────────┐
│ Outros Sindicatos Encontrados no PDF            │
├─────────────────────────────────────────────────┤
│ ○ SINDICATO DAS SANTAS CASAS E ENTIDADES...     │
│ ● SINDICATO DOS ENFERMEIROS DO ESTADO DA BAHIA  │
│ ○ SINDICATO DOS FARMACÊUTICOS DO ESTADO...      │
└─────────────────────────────────────────────────┘
```

**Lista completa** de todos os sindicatos mencionados no PDF.

#### 📌 Seção 3: Ou Digite Manualmente

```
┌─────────────────────────────────────────────────┐
│ Ou Digite Manualmente                            │
├─────────────────────────────────────────────────┤
│ [SINDICATO DOS ENFERMEIROS DO ESTADO DA BAHIA] │
└─────────────────────────────────────────────────┘
```

Campo de texto editável para digitar ou ajustar o nome.

#### 📌 Botão de Confirmação

```
                                    [ ✅ Confirmar ]
```

Clique para continuar com o sindicato selecionado.

---

## 🎓 Exemplos de Uso

### Exemplo 1: Sindicato Detectado Corretamente

**Situação**: Script detectou "SINDICATO DOS ENFERMEIROS DO ESTADO DA BAHIA"

**Ação**:
1. Veja que está correto
2. Clique em "✅ Confirmar"
3. Pronto!

---

### Exemplo 2: Sindicato Detectado Incorretamente

**Situação**: Script detectou "SINDICATO DAS SANTAS CASAS" (empregador), mas você quer o dos empregados

**Ação**:
1. Veja a lista de "Outros Sindicatos Encontrados"
2. Clique no radio button do sindicato correto
3. Clique em "✅ Confirmar"

---

### Exemplo 3: Sindicato Não Detectado

**Situação**: Script mostra "SINDICATO NÃO IDENTIFICADO"

**Ação**:
1. Veja a lista de "Outros Sindicatos Encontrados"
2. Clique no radio button do sindicato correto
3. **OU** digite manualmente no campo de texto
4. Clique em "✅ Confirmar"

---

### Exemplo 4: Ajuste Manual

**Situação**: Sindicato detectado, mas com pequeno erro (ex: falta de acento)

**Ação**:
1. Clique no campo "Ou Digite Manualmente"
2. Edite o texto (adicione acento, corrija palavra, etc.)
3. Clique em "✅ Confirmar"

---

## 💡 Dicas

### ✅ Boas Práticas

1. **Sempre revise**: Mesmo que detectado automaticamente, confira se está correto
2. **Use a lista**: Mais rápido que digitar manualmente
3. **Copie do PDF**: Se precisar digitar, abra o PDF e copie o nome exato
4. **Seja consistente**: Use sempre o mesmo formato para o mesmo sindicato

### ⚠️ Atenções

1. **Sindicato dos EMPREGADOS**: Escolha o sindicato dos trabalhadores, NÃO o dos empregadores
2. **Nome completo**: Inclua o nome completo (ex: "DO ESTADO DA BAHIA")
3. **Sigla opcional**: Pode incluir ou não a sigla (ex: "- SINDIMED")
4. **Maiúsculas**: O script normaliza automaticamente

---

## 🔍 Como Identificar o Sindicato Correto

### Padrão de CCT

Convenções Coletivas geralmente têm este formato:

```
de um lado, o SINDICATO DOS EMPREGADORES (SINDIFIBA, etc.)
e, do outro lado, o SINDICATO DOS EMPREGADOS (SINDIMED, SEEB, etc.)
```

**Regra**: Escolha o sindicato que vem **DEPOIS** de "do outro lado" ou "representados pelo".

### Exemplos

| PDF | Empregador | Empregado (ESCOLHA ESTE) |
|-----|------------|--------------------------|
| **SINDIMED** | SINDIFIBA | SINDICATO DOS MÉDICOS DO ESTADO DA BAHIA |
| **SEEB** | SINDIFIBA | SINDICATO DOS ENFERMEIROS DO ESTADO DA BAHIA |
| **SINDIFARMA** | SINDIFIBA | SINDICATO DOS FARMACÊUTICOS DO ESTADO DA BAHIA |

---

## 🆘 Problemas Comuns

### Problema 1: Lista Vazia

**Sintoma**: Seção "Outros Sindicatos Encontrados" está vazia

**Causa**: PDF não tem sindicatos claramente identificados

**Solução**: Digite manualmente no campo de texto

---

### Problema 2: Muitas Opções

**Sintoma**: Lista tem 10+ opções

**Causa**: PDF menciona muitos sindicatos

**Solução**: 
1. Use a barra de rolagem para ver todas
2. Escolha o que vem após "do outro lado" ou "representados pelo"

---

### Problema 3: Nome Muito Longo

**Sintoma**: Nome do sindicato tem 100+ caracteres

**Causa**: Sindicato tem nome muito descritivo

**Solução**: 
1. Pode usar o nome completo (recomendado)
2. **OU** encurtar para a parte principal (ex: "SINDICATO DOS TRABALHADORES EM SANTAS CASAS")

---

## 📊 Comparação: Antes vs Depois

| Aspecto | Antes (v2.1) | Depois (v3.0) |
|---------|--------------|---------------|
| **Detecção automática** | ✅ Sim | ✅ Sim |
| **Confirmação manual** | ❌ Não | ✅ Sim |
| **Lista de opções** | ❌ Não | ✅ Sim |
| **Edição manual** | ❌ Não | ✅ Sim |
| **Taxa de acerto** | ~70% | **100%** ✅ |

---

## 🎉 Benefícios

1. ✅ **100% de precisão**: Você confirma o sindicato correto
2. ✅ **Flexibilidade**: Funciona com QUALQUER tipo de sindicato
3. ✅ **Transparência**: Vê todas as opções disponíveis
4. ✅ **Controle total**: Pode editar se necessário
5. ✅ **Rápido**: Apenas um clique para confirmar

---

## 📝 Resumo

1. **Script detecta** automaticamente (se possível)
2. **Janela aparece** com opções
3. **Você escolhe** ou edita
4. **Clica em Confirmar**
5. **Processamento continua** com sindicato correto

**Simples, rápido e preciso!** 🚀

---

**Versão**: 3.0  
**Data**: Dezembro 2024  
**Status**: ✅ Ativo
