import yfinance as yf
import pandas as pd
import datetime


df = pd.DataFrame({"Ação": ["KLBN4F.SA", "WEGE3.SA", "BBAS3.SA"]})

# Obtendo a data de ontem
data_ontem = (datetime.datetime.now().date() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

# Baixando os dados para o símbolo KLBN4.SA desde 2022-10-01 até ontem
data_klbn4 = yf.download("KLBN4F.SA", start="2022-10-01", end=data_ontem, progress=False)

print(data_klbn4)