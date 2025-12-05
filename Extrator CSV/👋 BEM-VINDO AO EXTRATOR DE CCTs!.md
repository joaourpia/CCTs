# 👋 BEM-VINDO AO EXTRATOR DE CCTs!

## 🎯 O Que É Este Pacote?

Este é o **código-fonte** para gerar um **aplicativo standalone** (executável .exe) do Extrator de Convenções Coletivas de Trabalho.

---

## 📦 O Que Está Incluído?

| Arquivo | Descrição |
|---------|-----------|
| **extrator_cct_standalone.py** | Código-fonte principal |
| **build_exe.py** | Script para gerar o executável |
| **requirements.txt** | Dependências Python |
| **README_STANDALONE.md** | Documentação completa |
| **GUIA_INSTALACAO_TESSERACT.md** | Guia de instalação do Tesseract |
| **COMO_GERAR_EXE.md** | Como gerar o executável |

---

## 🚀 Início Rápido

### Opção 1: Usar Como Aplicativo Python (Mais Fácil)

1. **Instale o Tesseract OCR**:
   - Siga: `GUIA_INSTALACAO_TESSERACT.md`

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute**:
   ```bash
   python extrator_cct_standalone.py
   ```

4. **Configure** na primeira execução:
   - Insira API key da OpenAI (opcional)
   - Ou pule para usar sem IA

5. **Use normalmente**!

### Opção 2: Gerar Executável (.exe) para Distribuir

1. **Siga o guia**:
   - Abra: `COMO_GERAR_EXE.md`
   - Siga os passos

2. **Execute o script**:
   ```bash
   python build_exe.py
   ```

3. **Encontre o executável**:
   - `dist/ExtratorCCT.exe`

4. **Distribua**:
   - Copie o .exe para outros computadores
   - Inclua a documentação

---

## 📋 Requisitos

### Para Executar o Script Python

- ✅ Python 3.8+
- ✅ Tesseract OCR instalado
- ✅ Dependências instaladas (`pip install -r requirements.txt`)
- ✅ (Opcional) API key da OpenAI

### Para Gerar o Executável

- ✅ Tudo acima +
- ✅ PyInstaller instalado
- ✅ Windows (para gerar .exe do Windows)

### Para Usar o Executável em Outros PCs

- ✅ Windows 10/11
- ✅ Tesseract OCR instalado
- ✅ (Opcional) API key da OpenAI

---

## 🎯 Qual Opção Escolher?

### Use o Script Python Se:

- ✅ Você tem Python instalado
- ✅ Vai usar apenas no seu computador
- ✅ Quer fazer modificações no código
- ✅ Quer testar rapidamente

### Gere o Executável Se:

- ✅ Quer distribuir para outros computadores
- ✅ Outros usuários não têm Python
- ✅ Quer um aplicativo "profissional"
- ✅ Quer facilitar o uso para não-técnicos

---

## 📚 Documentação

| Documento | Quando Ler |
|-----------|------------|
| **LEIA-ME_PRIMEIRO.md** | ← Você está aqui! |
| **README_STANDALONE.md** | Documentação completa do aplicativo |
| **GUIA_INSTALACAO_TESSERACT.md** | Como instalar o Tesseract OCR |
| **COMO_GERAR_EXE.md** | Como gerar o executável |

---

## 🆘 Precisa de Ajuda?

### Problemas Comuns

1. **"Tesseract não encontrado"**:
   - Siga: `GUIA_INSTALACAO_TESSERACT.md`

2. **"Erro ao instalar dependências"**:
   - Verifique se Python está instalado
   - Execute: `pip install --upgrade pip`
   - Tente novamente: `pip install -r requirements.txt`

3. **"Erro ao gerar executável"**:
   - Siga: `COMO_GERAR_EXE.md`
   - Verifique se PyInstaller está instalado

### Mais Ajuda

Consulte a documentação completa em `README_STANDALONE.md`

---

## 🎓 Fluxo de Trabalho Recomendado

### Para Desenvolvedores

1. ✅ Instale Tesseract
2. ✅ Instale dependências Python
3. ✅ Teste o script Python
4. ✅ Faça modificações (se necessário)
5. ✅ Gere o executável
6. ✅ Teste o executável
7. ✅ Distribua

### Para Usuários Finais

1. ✅ Instale Tesseract
2. ✅ Execute `ExtratorCCT.exe`
3. ✅ Configure API key (opcional)
4. ✅ Use normalmente

---

## ✨ Recursos

### Configuração de API Key

- ✅ **Interface gráfica** para configurar
- ✅ **Salva localmente** (não precisa reconfigurar)
- ✅ **Opcional** (funciona sem IA)

### Tesseract OCR

- ✅ **Qualidade profissional** de extração
- ✅ **Detecta automaticamente** se instalado
- ✅ **Guia de instalação** incluído

### Interface Gráfica

- ✅ **Windows Explorer** para selecionar arquivos
- ✅ **Pop-ups informativos** de sucesso/erro
- ✅ **Fácil de usar** para não-técnicos

---

## 🎉 Pronto para Começar!

Escolha sua opção:

### 👨‍💻 Desenvolvedor / Técnico

→ Leia: `COMO_GERAR_EXE.md`

### 👤 Usuário Final

→ Leia: `README_STANDALONE.md`

### 🔧 Instalação do Tesseract

→ Leia: `GUIA_INSTALACAO_TESSERACT.md`

---

**Boa sorte!** 🚀

---

**Versão**: Standalone 1.0  
**Data**: Dezembro 2024  
**Autor**: Manus AI
