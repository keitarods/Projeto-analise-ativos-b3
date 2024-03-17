import pandas as pd
import os
import openpyxl


def leitura_arquivos(local):
    dfs = []

    #Itera sobre a pasta para leitura dos arquivos
    for arquivo in os.listdir(local):
        #Verifica se o arquivo é do formato excel
        if arquivo.endswith("xlsx"):
            local_file = os.path.join(local, arquivo)
            df = pd.read_excel(local_file)
            dfs.append(df)

    df = pd.concat(dfs).sort_values("Data do Negócio", ascending = True) #Ordena ativos por data

    return df

def obtem_tickers(df):
    tickers = df["Código de Negociação"].unique()
    return tickers

def agrupa_valor(df):
    data = df.groupby(["Código de Negociação"])["Preço"].agg(Média_Preço=("mean"))
    data_1 = df.groupby(["Código de Negociação"])["Quantidade"].agg(Qti=("sum"))
    data_2 = df.set_index(["Código de Negociação", "Data do Negócio"])["Valor"].groupby(level=0).cumsum().reset_index()

    return pd.DataFrame(data), pd.DataFrame(data_1), pd.DataFrame(data_2)

def remove_ticker(df, ticker: list):
    data = df[~df["Código de Negociação"].isin(ticker)]
    
    return data