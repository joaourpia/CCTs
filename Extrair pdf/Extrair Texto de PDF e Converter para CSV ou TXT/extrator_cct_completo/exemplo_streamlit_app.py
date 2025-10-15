#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de Aplicação Streamlit para Consulta de Convenções Coletivas

Este é um exemplo de como usar os dados extraídos pelo script extrator_clausulas_cct.py
em uma aplicação Streamlit.

Para executar:
    pip3 install streamlit pandas
    streamlit run exemplo_streamlit_app.py
"""

import streamlit as st
import pandas as pd
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="Convenções Coletivas de Trabalho",
    page_icon="📋",
    layout="wide"
)

# Título principal
st.title("📋 Consulta de Convenções Coletivas de Trabalho")
st.markdown("---")

# Sidebar para upload e filtros
with st.sidebar:
    st.header("⚙️ Configurações")
    
    # Upload de arquivo CSV
    uploaded_file = st.file_uploader(
        "Carregar arquivo CSV com cláusulas",
        type=['csv'],
        help="Faça upload do arquivo CSV gerado pelo extrator_clausulas_cct.py"
    )
    
    st.markdown("---")
    st.markdown("""
    ### Como usar:
    1. Faça upload do arquivo CSV com as cláusulas extraídas
    2. Use os filtros para encontrar cláusulas específicas
    3. Clique em "Ver texto completo" para expandir cada cláusula
    
    ### Gerar CSV:
    Use o script `extrator_clausulas_cct.py` para extrair cláusulas de PDFs:
    ```bash
    python3 extrator_clausulas_cct.py \\
        -i convencao.pdf \\
        -o clausulas.csv \\
        -s "SINDICATO" \\
        -c "ANO"
    ```
    """)

# Função para carregar dados
@st.cache_data
def carregar_dados(file):
    """Carrega e processa o arquivo CSV"""
    df = pd.read_csv(file)
    return df

# Verifica se há arquivo carregado
if uploaded_file is not None:
    try:
        # Carrega os dados
        df = carregar_dados(uploaded_file)
        
        # Verifica se o DataFrame tem as colunas esperadas
        colunas_esperadas = ['Sindicato', 'Convenção', 'Título da Cláusula', 'Resumo', 'Cláusula Completa']
        if not all(col in df.columns for col in colunas_esperadas):
            st.error("❌ O arquivo CSV não possui as colunas esperadas. Verifique se foi gerado corretamente pelo extrator.")
            st.stop()
        
        # Estatísticas gerais
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Cláusulas", len(df))
        with col2:
            st.metric("Sindicatos", df['Sindicato'].nunique())
        with col3:
            st.metric("Convenções", df['Convenção'].nunique())
        
        st.markdown("---")
        
        # Filtros
        col_filtro1, col_filtro2 = st.columns(2)
        
        with col_filtro1:
            # Filtro por sindicato
            sindicatos = ['Todos'] + sorted(df['Sindicato'].unique().tolist())
            sindicato_selecionado = st.selectbox(
                "🏢 Filtrar por Sindicato",
                sindicatos
            )
        
        with col_filtro2:
            # Filtro por convenção
            if sindicato_selecionado != 'Todos':
                convencoes = ['Todas'] + sorted(df[df['Sindicato'] == sindicato_selecionado]['Convenção'].unique().tolist())
            else:
                convencoes = ['Todas'] + sorted(df['Convenção'].unique().tolist())
            
            convencao_selecionada = st.selectbox(
                "📅 Filtrar por Convenção",
                convencoes
            )
        
        # Busca por palavra-chave
        busca = st.text_input(
            "🔍 Buscar por palavra-chave (título ou conteúdo)",
            placeholder="Digite uma palavra-chave para buscar..."
        )
        
        # Aplica filtros
        df_filtrado = df.copy()
        
        if sindicato_selecionado != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['Sindicato'] == sindicato_selecionado]
        
        if convencao_selecionada != 'Todas':
            df_filtrado = df_filtrado[df_filtrado['Convenção'] == convencao_selecionada]
        
        if busca:
            # Busca em título e texto completo
            mascara = (
                df_filtrado['Título da Cláusula'].str.contains(busca, case=False, na=False) |
                df_filtrado['Cláusula Completa'].str.contains(busca, case=False, na=False)
            )
            df_filtrado = df_filtrado[mascara]
        
        st.markdown("---")
        
        # Exibe resultados
        if len(df_filtrado) == 0:
            st.warning("⚠️ Nenhuma cláusula encontrada com os filtros aplicados.")
        else:
            st.success(f"✅ {len(df_filtrado)} cláusula(s) encontrada(s)")
            
            # Opção de visualização
            modo_visualizacao = st.radio(
                "Modo de visualização:",
                ["Expandir uma por vez", "Listar todas"],
                horizontal=True
            )
            
            st.markdown("---")
            
            # Exibe as cláusulas
            for idx, row in df_filtrado.iterrows():
                # Container para cada cláusula
                with st.container():
                    # Cabeçalho da cláusula
                    st.subheader(f"📄 {row['Título da Cláusula']}")
                    
                    # Informações adicionais
                    col_info1, col_info2 = st.columns(2)
                    with col_info1:
                        st.caption(f"**Sindicato:** {row['Sindicato']}")
                    with col_info2:
                        st.caption(f"**Convenção:** {row['Convenção']}")
                    
                    # Resumo
                    st.markdown(f"**Resumo:** {row['Resumo']}")
                    
                    # Texto completo
                    if modo_visualizacao == "Expandir uma por vez":
                        with st.expander("📖 Ver texto completo"):
                            st.markdown(row['Cláusula Completa'])
                    else:
                        st.markdown("**Texto completo:**")
                        st.info(row['Cláusula Completa'])
                    
                    st.markdown("---")
            
            # Opção de download dos resultados filtrados
            st.markdown("### 💾 Exportar Resultados")
            
            csv_filtrado = df_filtrado.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="⬇️ Baixar resultados filtrados (CSV)",
                data=csv_filtrado,
                file_name="clausulas_filtradas.csv",
                mime="text/csv"
            )
    
    except Exception as e:
        st.error(f"❌ Erro ao processar o arquivo: {e}")
        st.exception(e)

else:
    # Tela inicial quando não há arquivo carregado
    st.info("👈 Faça upload de um arquivo CSV na barra lateral para começar")
    
    st.markdown("""
    ## Bem-vindo ao Sistema de Consulta de CCT
    
    Este sistema permite consultar cláusulas de Convenções Coletivas de Trabalho de forma organizada e eficiente.
    
    ### Como funcionar:
    
    1. **Extrair cláusulas de PDFs**: Use o script `extrator_clausulas_cct.py` para converter PDFs de convenções em arquivos CSV
    2. **Carregar dados**: Faça upload do arquivo CSV gerado na barra lateral
    3. **Consultar**: Use os filtros e busca para encontrar cláusulas específicas
    4. **Exportar**: Baixe os resultados filtrados quando necessário
    
    ### Recursos:
    
    - ✅ Filtros por sindicato e convenção
    - ✅ Busca por palavra-chave
    - ✅ Visualização de resumos e textos completos
    - ✅ Exportação de resultados filtrados
    - ✅ Interface intuitiva e responsiva
    
    ### Exemplo de uso do extrator:
    
    ```bash
    # Extrair cláusulas de um PDF
    python3 extrator_clausulas_cct.py \\
        -i CCTFISIOTERAPIA2025-2026HCM.pdf \\
        -o clausulas_fisio.csv \\
        -s "FISIOTERAPEUTAS/T.O." \\
        -c "MARINGÁ 2025/2026"
    
    # Extrair apenas as primeiras 18 cláusulas
    python3 extrator_clausulas_cct.py \\
        -i convencao.pdf \\
        -o clausulas.csv \\
        --limite 18
    
    # Para PDFs escaneados (usar OCR)
    python3 extrator_clausulas_cct.py \\
        -i convencao_escaneada.pdf \\
        -o clausulas.csv \\
        --ocr
    ```
    
    ---
    
    **Desenvolvido para facilitar o acesso e consulta de Convenções Coletivas de Trabalho**
    """)

# Rodapé
st.markdown("---")
st.caption("Sistema de Consulta de Convenções Coletivas de Trabalho | Desenvolvido com Streamlit")

