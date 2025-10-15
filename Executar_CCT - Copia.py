import pandas as pd
import streamlit as st

st.set_page_config(page_title="CCTs Liga Alvaro Bahia", layout="wide")

# Carregue a base
df = pd.read_csv("clausulas_farmaceuticos.csv", encoding="utf-8")

# CONFIRA essas variáveis com os nomes certos do seu csv!
col_sindicato = "Sindicato"
col_cct = "Convenção"         # ajuste conforme seu arquivo ("Convenção", "Acordo", etc)
col_nome = "Título da Cláusula"
col_resumo = "Resumo"
col_completa = "Cláusula Completa"

st.markdown(
    '<h1 style="font-size:3rem; font-weight:900; text-align:center;">CCTs Liga Alvaro Bahia</h1>',
    unsafe_allow_html=True,
)

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
            st.markdown(f"<div style='background-color: #F8F9FA; border-radius:7px; padding: 1rem;'><b>Conteúdo Completo:</b><br>{linha[col_completa]}</div>", unsafe_allow_html=True)
        else:
            st.write("Selecione uma cláusula para ver detalhes.")
    else:
        st.write("Selecione uma convenção/acordo coletivo.")
else:
    st.write("Selecione o sindicato acima para começar.")
