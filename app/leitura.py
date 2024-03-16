import pandas as pd
import os
import openpyxl


def leitura_arquivos(local):
    dfs = []

    for arquivo in os.listdir(local):
        if arquivo.endswith("xlsx"):
            local_file = os.path.join(local, arquivo)
            df = pd.read_excel(local_file)

            dfs.append(df)

    df = pd.concat(dfs)
    df = df.sort_values("Data do Negócio", ascending = True)

    return df

def obtem_tickers(df):
    return df["Código de Negociação"].unique()
