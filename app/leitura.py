import pandas as pd
import os
import openpyxl
import yfinance as yf
import datetime
import numpy as np

def leitura_arquivos(local):
    dfs = []

    #Itera sobre a pasta para leitura dos arquivos
    for arquivo in os.listdir(local):
        #Verifica se o arquivo é do formato excel
        if arquivo.endswith("xlsx"):
            local_file = os.path.join(local, arquivo)
            df = pd.read_excel(local_file)
            dfs.append(df)

    dfs = pd.concat(dfs)

    dfs['Data do Negócio'] = pd.to_datetime(dfs['Data do Negócio'], format='%d/%m/%Y').dt.date

    # Classifique o DataFrame com base na coluna 'Data do Negócio'
    dfs = dfs.sort_values('Data do Negócio', ascending=True)

    return dfs

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

def desdobramento_acao(df, ticker: str, data_de_corte):
    # Realize a comparação com cada valor da coluna 'Data do Negócio'
    df['Preço'] = df.apply(lambda x: x['Preço'] / 2 
                           if (x['Data do Negócio'] < data_de_corte)
                            and (x["Código de Negociação"] == ticker) 
                            else x['Preço'], axis=1)
    
    df['Quantidade'] = df.apply(lambda x: x['Quantidade'] * 2 
                                if (x['Data do Negócio'] < data_de_corte) 
                                and (x["Código de Negociação"] == ticker) 
                                else x['Quantidade'], axis=1)
    
    return df

def historico_cotacao(ticker: list):
    data_ontem = (datetime.datetime.now().date() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    dfs_hist = []
    for label in ticker:
        print(label)
        try:
            df_hist = yf.download(label ,start="2022-10-01", end=data_ontem, progress=False)
            df_hist['Ticker'] = label  # Adiciona uma coluna 'Ticker' ao DataFrame para identificar de qual ação são os dados
            dfs_hist.append(df_hist)
        except Exception as e:
            print(f"Erro ao baixar dados para o ticker {label}: {e}")

    if dfs_hist:
        dfs_hist = pd.concat(dfs_hist)
        dfs_hist.reset_index(inplace=True)  # Resetar o índice após a concatenação

        # Renomear colunas
        dfs_hist.columns = ["Data do Negócio", "Preço abertura", "Máxima", "Mínima", "Preço fechamento", "Fechamento ajustado", "Volume", "Ticker"]

    return dfs_hist



if __name__ == "__main__":
    ### BLOCO DE TESTES

    #Realiza leitura dos arquivos
    df = leitura_arquivos("./data")

    #Removedor de ativos não desejados
    df = remove_ticker(df, list(["RBVA11", "ARCT11", "NUBR33"]))

    data_de_corte = datetime.date(2023, 12, 1)
    df = desdobramento_acao(df, "SLCE3F", data_de_corte)
    print("AQUI")

    df = padroniza_ticker(df)

    df_hist = historico_cotacao(df["Código de Negociação"].unique())

    df_agrupa = agrupa_valor(df)

    merged_df = pd.merge_asof(df_hist, df_agrupa[0], on='Data do Negócio', direction='backward')
