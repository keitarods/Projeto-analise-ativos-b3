import yfinance as yf
import pandas as pd


df = pd.DataFrame({"Ação": ["KLBN4F.SA", "WEGE3.SA", "BBAS3.SA"]})

klabin = yf.Ticker("KLBN4F.SA").info["previousClose"]
df["Preço"] = df["Ação"].apply(lambda x : yf.Ticker(x).info["previousClose"])
print(df)