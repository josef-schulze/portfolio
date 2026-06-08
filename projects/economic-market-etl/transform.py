import pandas as pd
from datetime import datetime

def transform_economic_data(econ_data):
    """Transform economic data into structured format"""
    records = []
    for name, info in econ_data.items():
        records.append({
            'indicator': name,
            'value': info['value'],
            'date': info['date'],
            'data_type': 'economic',
            'loaded_at': datetime.now().isoformat()
        })
    return pd.DataFrame(records)

def transform_stock_data(stock_data):
    """Transform stock data"""
    records = []
    for symbol, info in stock_data.items():
        records.append({
            'symbol': symbol,
            'close_price': info['close'],
            'volume': info['volume'],
            'date': info['date'],
            'data_type': 'market',
            'loaded_at': datetime.now().isoformat()
        })
    return pd.DataFrame(records)

if __name__ == "__main__":
    print("Transform module ready.")
