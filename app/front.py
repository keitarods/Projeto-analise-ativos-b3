import streamlit as st
import os
from leitura import leitura_arquivos, obtem_tickers
from st_aggrid import AgGrid
from streamlit_pandas_profiling import st_profile_report

st.write("""
# Projeto de análise B3
Essa é uma página voltada para verificar as suas movimentações na Bolsa B3
""")

df = leitura_arquivos("./data")

st.subheader("Extato de compra e venda de ativos")
selecao= st.multiselect("Selecione", options = obtem_tickers(df))

if len(selecao) > 0:
    df_select = df[df["Código de Negociação"].isin(selecao)]
    st.dataframe(df_select)

else:
    st.dataframe(df)

