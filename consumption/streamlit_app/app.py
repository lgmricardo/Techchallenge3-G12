# -*- coding: utf-8 -*-
"""Dataviz interativo — Tech Challenge Fase 3 · State of Data Brasil.

Replica os 15 gráficos do material executivo (consumption/charts/*.png), navegáveis por
pergunta de negócio, cada um com a tabela Gold correspondente disponível para conferência.
Fonte dos dados: datalake/gold/csv/ (camada Gold do pipeline, sem reprocessamento aqui).

Rodar localmente:
    streamlit run consumption/streamlit_app/app.py
"""
import pandas as pd
import streamlit as st
from data import PERGUNTAS, GOLD, CHARTS

st.set_page_config(page_title="State of Data Brasil — Dataviz", layout="wide")


@st.cache_data
def ler(nome, filtro_col=None, filtro_val=None):
    df = pd.read_csv(GOLD / f"{nome}.csv")
    if filtro_col:
        df = df[df[filtro_col] == filtro_val]
    return df

st.sidebar.title("State of Data Brasil")
st.sidebar.caption("Tech Challenge Fase 3 · Dataviz sobre a camada Gold")
secao = st.sidebar.radio("Pergunta de negócio", list(PERGUNTAS.keys()))
st.sidebar.markdown("---")
st.sidebar.caption(
    "22.686 respostas · 6 edições (2019–2025/26) · 21 tabelas Gold · "
    "gráficos idênticos ao material executivo (`consumption/charts/`)."
)

st.title("O Mercado Brasileiro de Dados")
st.caption("State of Data Brasil (Data Hackers/Bain) · pipeline AWS Medallion · " + secao)

for titulo, png, figura, tabela, filtro_col, filtro_val in PERGUNTAS[secao]:
    st.subheader(titulo)
    col_img, col_meta = st.columns([3, 1])
    with col_img:
        st.image(str(CHARTS / png), use_container_width=True)
    with col_meta:
        st.markdown(f"**{figura}** do relatório técnico")
        st.markdown(f"Fonte: `{tabela}.csv`")
        if filtro_col:
            st.markdown(f"Filtro: `{filtro_col} == {filtro_val!r}`")
    df = ler(tabela, filtro_col, filtro_val)
    with st.expander(f"Ver dados — {tabela}.csv ({len(df)} linhas)"):
        st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown("---")
