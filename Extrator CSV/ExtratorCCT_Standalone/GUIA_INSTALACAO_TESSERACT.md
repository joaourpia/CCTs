# 📥 Guia de Instalação do Tesseract OCR

## 🎯 O Que é Tesseract OCR?

O **Tesseract OCR** é um software gratuito que converte imagens em texto. É **obrigatório** para o Extrator de CCTs funcionar.

---

## 🪟 Instalação no Windows (Passo a Passo)

### Passo 1: Baixar o Instalador

1. **Acesse o site oficial**:
   - https://github.com/UB-Mannheim/tesseract/wiki

2. **Encontre a seção "Windows"**

3. **Baixe o instalador mais recente**:
   - Procure por: `tesseract-ocr-w64-setup-5.x.x.exe`
   - Clique para baixar (~60 MB)

### Passo 2: Executar o Instalador

1. **Duplo clique** no arquivo baixado

2. **Aceite** o contrato de licença

3. **Escolha o local** de instalação:
   - Padrão: `C:\Program Files\Tesseract-OCR`
   - **Recomendação**: Mantenha o padrão

4. **Selecione componentes**:
   - ✅ Marque: **"Additional language data (download)"**
   - ✅ Marque: **"Portuguese"** (por)
   - ✅ Marque: **"English"** (eng) - já vem marcado

5. **Clique em "Install"**

6. **Aguarde** a instalação (~1-2 minutos)

7. **Clique em "Finish"**

### Passo 3: Verificar Instalação

1. **Abra o Prompt de Comando**:
   - Pressione `Win + R`
   - Digite: `cmd`
   - Pressione Enter

2. **Digite o comando**:
   ```
   tesseract --version
   ```

3. **Resultado esperado**:
   ```
   tesseract 5.x.x
   leptonica-1.x.x
   ...
   ```

✅ **Se aparecer a versão**: Instalação bem-sucedida!  
❌ **Se der erro**: Veja a seção "Solução de Problemas" abaixo

---

## 🆘 Solução de Problemas

### Problema: "tesseract is not recognized"

**Causa**: Tesseract não está no PATH do Windows

**Solução 1: Adicionar ao PATH Manualmente**

1. Pressione `Win + R`
2. Digite: `sysdm.cpl`
3. Vá para a aba "Avançado"
4. Clique em "Variáveis de Ambiente"
5. Em "Variáveis do sistema", encontre "Path"
6. Clique em "Editar"
7. Clique em "Novo"
8. Adicione: `C:\Program Files\Tesseract-OCR`
9. Clique em "OK" em todas as janelas
10. **Reinicie o Prompt de Comando**
11. Teste novamente: `tesseract --version`

**Solução 2: Reinstalar**

1. Desinstale o Tesseract:
   - Painel de Controle → Programas → Desinstalar
   - Encontre "Tesseract-OCR"
   - Clique em "Desinstalar"

2. Reinstale seguindo os passos acima
3. **Certifique-se de marcar "Add to PATH"** durante a instalação

### Problema: "Portuguese language not found"

**Causa**: Idioma português não foi instalado

**Solução**:

1. Reinstale o Tesseract
2. Durante a instalação, **marque**:
   - ✅ "Additional language data (download)"
   - ✅ "Portuguese" (por)

### Problema: "Instalação falhou"

**Causa**: Falta de permissões ou antivírus bloqueando

**Solução**:

1. **Execute como Administrador**:
   - Clique com botão direito no instalador
   - Escolha "Executar como administrador"

2. **Desative temporariamente o antivírus**:
   - Durante a instalação
   - Reative depois

---

## 🐧 Instalação no Linux

### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-por
```

### Fedora/CentOS

```bash
sudo dnf install tesseract tesseract-langpack-por
```

### Verificar

```bash
tesseract --version
```

---

## 🍎 Instalação no macOS

### Com Homebrew

```bash
brew install tesseract tesseract-lang
```

### Verificar

```bash
tesseract --version
```

---

## ✅ Checklist de Instalação

Após instalar, verifique:

- [ ] Tesseract instalado em `C:\Program Files\Tesseract-OCR`
- [ ] Comando `tesseract --version` funciona
- [ ] Idioma português (por) instalado
- [ ] PATH configurado corretamente

**Tudo OK?** ✅ Você está pronto para usar o Extrator de CCTs!

---

## 📞 Precisa de Ajuda?

### Links Úteis

- **Site oficial**: https://github.com/tesseract-ocr/tesseract
- **Download Windows**: https://github.com/UB-Mannheim/tesseract/wiki
- **Documentação**: https://tesseract-ocr.github.io/

### Problemas Persistentes?

1. Verifique se o Windows está atualizado
2. Tente reiniciar o computador
3. Verifique se há espaço em disco suficiente
4. Consulte a documentação oficial

---

## 🎉 Pronto!

Após instalar o Tesseract, você pode usar o **Extrator de CCTs** normalmente!

**Próximos passos**:
1. ✅ Tesseract instalado
2. ✅ Execute `ExtratorCCT.exe`
3. ✅ Configure a API key (opcional)
4. ✅ Comece a extrair CCTs!

**Boa sorte!** 🚀
