-- =============================================
-- Database Setup for Economic & Market Data ETL Pipeline
-- Run this as the postgres superuser
-- =============================================

-- Create dedicated user (if not exists)
CREATE USER portfolio_user WITH PASSWORD '(REDACTED)';

-- Create database
CREATE DATABASE portfolio_db OWNER portfolio_user;

-- Connect to the new database and create tables
\c portfolio_db

-- Create custom schema
CREATE SCHEMA IF NOT EXISTS etl_data AUTHORIZATION portfolio_user;

-- Economic Indicators Table
CREATE TABLE IF NOT EXISTS etl_data.economic_indicators (
    id SERIAL PRIMARY KEY,
    indicator VARCHAR(100) NOT NULL,
    value NUMERIC(18,6),
    date DATE NOT NULL,
    data_type VARCHAR(50),
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Market Data Table
CREATE TABLE IF NOT EXISTS etl_data.market_data (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    close_price NUMERIC(12,2),
    volume BIGINT,
    date DATE NOT NULL,
    data_type VARCHAR(50),
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Grant permissions
GRANT USAGE ON SCHEMA etl_data TO portfolio_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA etl_data TO portfolio_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA etl_data TO portfolio_user;

-- Indexes
CREATE INDEX IF NOT EXISTS idx_econ_indicator_date ON etl_data.economic_indicators(indicator, date);
CREATE INDEX IF NOT EXISTS idx_market_symbol_date ON etl_data.market_data(symbol, date);
