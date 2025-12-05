import pandas as pd
import streamlit as st
import re
import os
import base64 # Importa o módulo base64 para codificar a imagem

# -------------------------------------------------
# 1️⃣ Configurações da página
st.set_page_config(page_title="CCTs Liga Alvaro Bahia", layout="wide")
# -------------------------------------------------
# 2️⃣ Caminho da imagem do logo
# Certifique-se de que este caminho está correto no seu sistema
# ALTERAÇÃO AQUI: Usando caminho relativo com os.path.join
logo_path = os.path.join("images", "Logo_Liga_Alvaro.png")
# -------------------------------------------------
# 3️⃣ Exibir o logo no topo da página, rolando com o conteúdo
# Removendo 'position: fixed' para que a imagem role com o texto.
# Inserimos ela no fluxo normal do Streamlit.
if os.path.exists(logo_path):
    try:
        # Converte a imagem para base64 (necessário para embed no HTML)
        with open(logo_path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        # Usamos st.markdown para inserir a imagem, mas sem o 'position: fixed'.
        # Adicionei um 'margin-bottom' para dar um pequeno espaçamento antes do título.
        logo_html = f"""
        <div style="text-align: left; margin-bottom: 20px;">
            <img src="data:image/png;base64,{b64}" style="width:150px;">
        </div>
        """
        st.markdown(logo_html, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar ou exibir o logo: {e}")
else:
    st.warning(f"⚠️ Logo não encontrado no caminho especificado: {logo_path}")
# -------------------------------------------------
# 4️⃣ Título principal da aplicação (centralizado)
# Removendo o 'margin-top' que havíamos adicionado, pois o logo não é mais fixo.
st.markdown(
    '<h1 style="font-size:3rem; font-weight:900; text-align:center;">CCTs Liga Alvaro Bahia</h1>',
    unsafe_allow_html=True,
)
# -------------------------------------------------
# (O restante do seu código permanece inalterado)
# Carregue a base
df = pd.read_csv("CCTs_Extraidas.csv", encoding="utf-8")
# CONFIRA essas variáveis com os nomes certos do seu csv!
col_sindicato = "Sindicato"
col_cct = "Convenção"         # ajuste conforme seu arquivo ("Convenção", "Acordo", etc)
col_nome = "Título da Cláusula"
col_resumo = "Resumo"
col_completa = "Cláusula Completa"
# 1º SELEÇÃO: SINDICATO
sindicatos = sorted(df[col_sindicato].dropna().unique())
sindicato_escolhido = st.selectbox(
    "Selecione o sindicato:",
    ["Selecione"] + sindicatos,
    index=0
)
if sindicato_escolhido and sindicato_escolhido != "Selecione":
    # 2º SELEÇÃO: CCT/acordo, filtrado pelo sindicato
    filtra_cct = df[df[col_sindicato]==sindicato_escolhido]
    cct_unicos = sorted(filtra_cct[col_cct].dropna().unique())
    cct_escolhida = st.selectbox(
        "Selecione a convenção/acordo coletivo:",
        ["Selecione"] + cct_unicos,
        index=0
    )
    if cct_escolhida and cct_escolhida != "Selecione":
        # 3º SELEÇÃO: Cláusula, filtrada pelo sindicato+acordo escolhido
        filtra_clausulas = filtra_cct[filtra_cct[col_cct] == cct_escolhida]
        clausulas_lista = filtra_clausulas[col_nome].dropna().tolist()
        clausula_escolhida = st.selectbox(
            "Escolha a cláusula:",
            ["Selecione"] + clausulas_lista,
            index=0,
            help="Selecione o nome da cláusula desejada"
        )
        if clausula_escolhida and clausula_escolhida != "Selecione":
            linha = filtra_clausulas[filtra_clausulas[col_nome]==clausula_escolhida].iloc[0]
            st.markdown(f"<h3 style='margin-bottom: 0'>{linha[col_nome]}</h3>", unsafe_allow_html=True)
            if col_resumo in df.columns:
                st.markdown(f"<div style='color:#666; font-size:1.1rem; margin-bottom:0.5rem;'><b>Resumo:</b> {linha[col_resumo]}</div>", unsafe_allow_html=True)
            # Lógica para negrito nos parágrafos (mantida da nossa conversa anterior)
            conteudo_completo_formatado = str(linha[col_completa]) # Garante que é string
            conteudo_completo_formatado = re.sub(
                r'(PARÁGRAFO\s+(?:[A-ZÀ-Ú\s]+))',
                r'<b>\1</b>',
                conteudo_completo_formatado
            )
            st.markdown(f"<div style='background-color: #F8F9FA; border-radius:7px; padding: 1rem;'><b>Conteúdo Completo:</b><br>{conteudo_completo_formatado}</div>", unsafe_allow_html=True)
        else:
            st.write("Selecione uma cláusula para ver detalhes.")
    else:
        st.write("Selecione uma convenção/acordo coletivo.")
else:
    st.write("Selecione o sindicato acima para começar.")
