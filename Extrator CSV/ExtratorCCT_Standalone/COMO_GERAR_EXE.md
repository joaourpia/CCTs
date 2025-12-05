# 🔨 Como Gerar o Executável (.exe)

## 📋 Pré-requisitos

1. **Python 3.8+** instalado
2. **Tesseract OCR** instalado
3. **Windows** (para gerar .exe do Windows)

---

## 🚀 Passo a Passo

### 1. Instalar Dependências

Abra o Prompt de Comando (CMD) ou PowerShell na pasta do projeto e execute:

```bash
pip install -r requirements.txt
```

Isso instalará:
- pymupdf
- pytesseract
- pillow
- openai
- pyinstaller

### 2. Gerar o Executável

#### Opção A: Usar o Script Automático (Recomendado)

```bash
python build_exe.py
```

Este script:
- Verifica se PyInstaller está instalado
- Gera o executável com todas as configurações corretas
- Cria o arquivo `ExtratorCCT.exe` na pasta `dist/`

#### Opção B: Comando Manual

```bash
pyinstaller --name=ExtratorCCT --onefile --windowed --add-data="README_STANDALONE.md;." --hidden-import=PIL._tkinter_finder --hidden-import=pytesseract --hidden-import=openai --collect-all=pytesseract --collect-all=PIL extrator_cct_standalone.py
```

### 3. Encontrar o Executável

Após a geração, o executável estará em:

```
dist/ExtratorCCT.exe
```

### 4. Testar

1. Duplo clique em `dist/ExtratorCCT.exe`
2. Configure a API key (ou pule)
3. Teste com um PDF de CCT

---

## 📦 Distribuir para Outros Computadores

### O Que Distribuir

Crie uma pasta com:

```
ExtratorCCT/
├── ExtratorCCT.exe                    ← O aplicativo
├── README_STANDALONE.md               ← Documentação
└── GUIA_INSTALACAO_TESSERACT.md      ← Guia do Tesseract
```

### Compactar

1. Selecione a pasta `ExtratorCCT`
2. Clique com botão direito → "Enviar para" → "Pasta compactada (zipada)"
3. Distribua o arquivo ZIP

### Instruções para Usuários

1. Extrair o ZIP
2. Instalar Tesseract OCR (seguir `GUIA_INSTALACAO_TESSERACT.md`)
3. Executar `ExtratorCCT.exe`
4. Configurar API key (opcional)
5. Usar normalmente!

---

## ⚙️ Opções Avançadas do PyInstaller

### Incluir Ícone

```bash
pyinstaller --icon=icone.ico ...
```

### Gerar com Console (para Debug)

Remova `--windowed` do comando:

```bash
pyinstaller --name=ExtratorCCT --onefile ...
```

### Incluir Arquivos Adicionais

```bash
--add-data="arquivo.txt;."
--add-data="pasta;pasta"
```

### Reduzir Tamanho

```bash
--exclude-module=matplotlib
--exclude-module=numpy
```

---

## 🆘 Solução de Problemas

### Problema: "PyInstaller não encontrado"

**Solução**:
```bash
pip install pyinstaller
```

### Problema: "Erro ao gerar executável"

**Solução**:
1. Verifique se todas as dependências estão instaladas
2. Tente executar como administrador
3. Verifique se o antivírus não está bloqueando

### Problema: "Executável muito grande"

**Solução**:
- Use `--onefile` para um único arquivo
- Exclua módulos desnecessários com `--exclude-module`
- Tamanho típico: 50-100 MB (normal para apps com OCR)

### Problema: "Executável não funciona em outro PC"

**Solução**:
- Certifique-se de que o Tesseract está instalado no outro PC
- Verifique se é Windows 64-bit
- Teste em uma máquina virtual primeiro

---

## 📊 Tamanhos Esperados

| Componente | Tamanho |
|------------|---------|
| **ExtratorCCT.exe** | ~50-100 MB |
| **Tesseract OCR** | ~60 MB (instalado separadamente) |
| **Total distribuído** | ~50-100 MB (só o .exe) |

---

## 🎯 Checklist de Distribuição

Antes de distribuir, verifique:

- [ ] Executável gerado com sucesso
- [ ] Testado em máquina local
- [ ] Testado em máquina limpa (sem Python)
- [ ] Documentação incluída
- [ ] Guia de instalação do Tesseract incluído
- [ ] Compactado em ZIP
- [ ] Instruções claras para usuários

---

## 💡 Dicas

### Para Desenvolvimento

- Use `--windowed` para esconder o console
- Remova `--windowed` para ver erros durante testes

### Para Distribuição

- Sempre teste em máquina limpa
- Inclua documentação completa
- Forneça guia de instalação do Tesseract
- Considere criar um instalador (Inno Setup, NSIS)

### Para Manutenção

- Mantenha o código fonte organizado
- Versione os executáveis
- Documente mudanças em CHANGELOG

---

## 🎉 Pronto!

Agora você pode:
1. ✅ Gerar o executável
2. ✅ Distribuir para outros computadores
3. ✅ Usar sem Python instalado

**Boa sorte!** 🚀

---

**Nota**: O executável gerado é específico para Windows. Para Mac/Linux, use a versão Python diretamente.
