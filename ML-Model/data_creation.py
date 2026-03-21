import yfinance as yf
import pandas as pd

# 5 stocks from each of the 11 sectors on stockanalysis.com
tickers_list = {
    "SAP": "Tech", 
    "MSFT": "Tech",
    "IBM": "Tech",
    "NVDA": "Tech",
    "AAPL": "Tech",

    "VRTX": "Health",
    "ABT": "Health",
    "TAK": "Health",
    "ISRG": "Health",
    "HCA": "Health",

    "HDB": "Finance",
    "XXI": "Finance",
    "BLK": "Finance",
    "MS": "Finance",
    "V": "Finance",

    "GE": "Industry",
    "GEV": "Industry",
    "PWR": "Industry",
    "VRT": "Industry",
    "CTAS": "Industry",

    "COP": "Energy",
    "ENB": "Energy",
    "SLB": "Energy",
    "VLO": "Energy",
    "XOM": "Energy",

    "GOOGL": "Communication",
    "AMX": "Communication",
    "NFLX": "Communication",
    "APP": "Communication",
    "NTES": "Communication",

    "KHC": "Consumables",
    "EDU": "Consumables",
    "PG": "Consumables",
    "ADM": "Consumables",
    "KO": "Consumables",

    "LIN": "Materials",
    "NEM": "Materials",
    "BHP": "Materials",
    "MT": "Materials",
    "DOW": "Materials",

    "ORLY": "Services",
    "MCD": "Services",
    "CASY": "Services",
    "AMZN": "Services",
    "SGI": "Services",

    "CBRE": "Real_Estate",
    "NLY": "Real_Estate",
    "SPG": "Real_Estate",
    "AVB": "Real_Estate",
    "ARE": "Real_Estate",

    "NEE": "Utilities",
    "AXIA": "Utilities",
    "ATO": "Utilities",
    "AWK": "Utilities",
    "SRE": "Utilities"
    }

dfs = []

for ticker_name, ticker_type in tickers_list.items():
    cur_ticker = yf.Ticker(ticker_name)
    df = cur_ticker.history(period="5y")
    
    df["Type"] = ticker_type

    df = df.reset_index()
    dfs.append(df)

final_df = pd.concat(dfs, ignore_index=True)

print(final_df)

final_df.to_csv("data.csv", index=False)