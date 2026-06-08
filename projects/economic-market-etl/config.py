import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration - loaded from .env
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "database": os.getenv("DB_NAME", "portfolio_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "")
}

# FRED API
FRED_API_KEY = os.getenv("FRED_API_KEY", "")

# Economic series to track
ECONOMIC_SERIES = {
    "GDP": "GDP",
    "Unemployment_Rate": "UNRATE",
    "Inflation_CPI": "CPIAUCSL",
    "Fed_Funds_Rate": "FEDFUNDS",
    "Industrial_Production": "INDPRO"
}

# Stock symbols to track
STOCK_SYMBOLS = ["SPY", "QQQ", "DIA", "^VIX"]