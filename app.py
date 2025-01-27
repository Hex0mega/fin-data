import os
import yfinance as yf
import pyodbc, struct
import json
from fastapi import FastAPI
from azure import identity
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_methods=["GET", "PUT"],  # Allow specific methods

)

@app.get("/price/{ticker}")
def get_investments(ticker: str):
        dat = yf.Ticker(ticker)
        price = dat.analyst_price_targets['current']
        return {"price":price}
    
#connect to Azure SQL db
connection_string = os.getenv("AZURE_SQL_CONNECTIONSTRING")
print(connection_string)

def get_conn():
    credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
    token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
    conn = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
    return conn

@app.put("/investment/{ticker}")
def get_investments(ticker: str):
    with get_conn() as conn:
        cursor = conn.cursor()
        dat = yf.Ticker(ticker)
        price = dat.analyst_price_targets['current']
        query = f"UPDATE Investments SET LastPrice=? WHERE Ticker=?"
        params = (price, ticker)
        print(query)
        cursor.execute(query, params)
        conn.commit()
        return price