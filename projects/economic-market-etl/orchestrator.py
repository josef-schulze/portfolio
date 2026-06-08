from extract import extract_economic_data, extract_stock_data
from transform import transform_economic_data, transform_stock_data
from load import load_data
import pandas as pd

def run_full_pipeline():
    print("=== Starting Economic & Market Data ETL Pipeline ===\n")
    
    # Extract
    econ_raw = extract_economic_data()
    stock_raw = extract_stock_data()
    
    # Transform
    econ_df = transform_economic_data(econ_raw)
    stock_df = transform_stock_data(stock_raw)
    
    # Load
    if not econ_df.empty:
        load_data(econ_df, "economic_indicators")
    if not stock_df.empty:
        load_data(stock_df, "market_data")
    
    print("\n=== Pipeline completed successfully! ===")

if __name__ == "__main__":
    run_full_pipeline()
