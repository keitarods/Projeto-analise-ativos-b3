import streamlit as st
import os
from leitura import leitura_arquivos, obtem_tickers, agrupa_valor, remove_ticker, padroniza_ticker
from st_aggrid import AgGrid
from streamlit_pandas_profiling import st_profile_report
import plotly.express as px
import altair as alt
import pandas as pd

st.write("""
# Projeto de análise B3
Essa é uma página voltada para verificar as suas movimentações na Bolsa B3
""")

#Realiza leitura dos arquivos
df = leitura_arquivos("./data")

#Removedor de ativos não desejados
df = remove_ticker(df, list(["RBVA11", "ARCT11", "NUBR33"]))

df = padroniza_ticker(df)

#Header
st.subheader("Extato de compra e venda de ativos")

#Cria botão para selecionar filtro de ativos
selecao= st.multiselect("Selecione", options = obtem_tickers(df))

if len(selecao) > 0:
    df_select = df[df["Código de Negociação"].isin(selecao)]
   
    st.dataframe(df_select)

else:
    st.dataframe(df)

#Cria os agrupamentos por preço médio, quantidade de ativos, e acumulo dos ativos pelo tempo
df_agrupa = agrupa_valor(df)
#df_agrupa0 = pd.DataFrame(df_agrupa[0])
#df_agrupa0 = acumulado(df_agrupa0)

st.subheader("Preço Médio por ativo")
st.dataframe(df_agrupa[0])

st.subheader("Soma acumulativa")
st.dataframe(df_agrupa[1])

# Cria o gráfico com a progressão dos ativos em função do tempo
fig = px.line(df_agrupa[1], x='Data do Negócio', y='Valor', color='Código de Negociação',
            title='Progressão dos Ativos em Função do Tempo',
            labels={'Data do Negócio': 'Data', 'Valor': 'Valor'},
            hover_data={'Data do Negócio': '|%B %d, %Y', 'Código de Negociação': True, 'Valor': ':.2f'})

# Ajusta a aparência do gráfico
fig.update_layout(width=1000, height=600)

# Exibe o gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)