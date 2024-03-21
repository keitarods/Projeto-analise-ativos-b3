import pandas as pd
import os
import openpyxl
import yfinance as yf

def leitura_arquivos(local):
    dfs = []

    #Itera sobre a pasta para leitura dos arquivos
    for arquivo in os.listdir(local):
        #Verifica se o arquivo é do formato excel
        if arquivo.endswith("xlsx"):
            local_file = os.path.join(local, arquivo)
            df = pd.read_excel(local_file)
            dfs.append(df)
    # Converta a coluna 'Data do Negócio' para o tipo datetime.date
    df['Data do Negócio'] = pd.to_datetime(df['Data do Negócio'], format='%d/%m/%Y').dt.date

    # Classifique o DataFrame com base na coluna 'Data do Negócio'
    df = df.sort_values('Data do Negócio', ascending=True)


    return df

def padroniza_ticker(df, ticker = "Código de Negociação"):
    df[ticker] = df[ticker].apply(lambda x : str(x)+".SA")
    
    return df

def obtem_tickers(df):
    tickers = df["Código de Negociação"].unique()
    return tickers

def agrupa_valor(df):
    data = df.groupby(["Código de Negociação"]).agg(Preço_Médio=("Preço", "mean"), Qti=("Quantidade", "sum")).reset_index()
    data["Valor atual"] = data["Código de Negociação"].apply(lambda x : yf.Ticker(x).info["previousClose"])
    data["Acumulado Investido"] = data["Preço_Médio"] * data["Qti"]
    data["Acumulado Atual"] = data["Valor atual"] * data["Qti"]
    data["Diferença investido"] = data["Acumulado Atual"] - data["Acumulado Investido"]

    data_2 = df.set_index(["Código de Negociação", "Data do Negócio"])["Valor"].groupby(level=0).cumsum().reset_index()

    return pd.DataFrame(data), pd.DataFrame(data_2)

def remove_ticker(df, ticker: list):
    data = df[~df["Código de Negociação"].isin(ticker)]
    
    return data

