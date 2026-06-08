import pandas as pd
import yfinance as yf
from fredapi import Fred
import os
from datetime import datetime
from config import ECONOMIC_SERIES, STOCK_SYMBOLS, FRED_API_KEY

def extract_economic_data():
    """Extract latest economic indicators from FRED"""
    if not FRED_API_KEY:
        print("⚠️  No FRED API key provided. Skipping economic data.")
        return {}
    
    fred = Fred(api_key=FRED_API_KEY)
    data = {}
    print("Fetching economic data from FRED...")
    for name, series_id in ECONOMIC_SERIES.items():
        try:
            series = fred.get_series(series_id)
            latest = series.tail(1)
            data[name] = {
                'value': latest.iloc[0],
                'date': latest.index[0].strftime('%Y-%m-%d')
            }
            print(f"  ✓ {name}: {data[name]['value']} ({data[name]['date']})")
        except Exception as e:
            print(f"  ✗ Error fetching {name}: {e}")
    return data

def extract_stock_data():
    """Extract recent stock/ETF data"""
    print("Fetching stock market data...")
    data = {}
    for symbol in STOCK_SYMBOLS:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="5d")
            if not hist.empty:
                latest = hist.iloc[-1]
                data[symbol] = {
                    'close': round(latest['Close'], 2),
                    'volume': int(latest['Volume']),
                    'date': latest.name.strftime('%Y-%m-%d')
                }
                print(f"  ✓ {symbol}: ${data[symbol]['close']} on {data[symbol]['date']}")
        except Exception as e:
            print(f"  ✗ Error fetching {symbol}: {e}")
    return data

if __name__ == "__main__":
    econ = extract_economic_data()
    stocks = extract_stock_data()