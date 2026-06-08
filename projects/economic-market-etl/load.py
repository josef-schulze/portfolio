import pandas as pd
from sqlalchemy import create_engine
from config import DB_CONFIG

def get_engine():
    conn_str = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    return create_engine(conn_str)

def load_data(df, table_name):
    """Load DataFrame to PostgreSQL"""
    engine = get_engine()
    df.to_sql(table_name, engine, schema='etl_data', if_exists='append', index=False)
    print(f"Loaded {len(df)} records to table 'etl_data.{table_name}'")
