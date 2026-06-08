# Economic & Market Data ETL Pipeline

This is a repeatable, production-style ETL pipeline that pulls current economic indicators from FRED (Federal Reserve) and stock market data from Yahoo Finance, transforms it, and loads it into PostgreSQL.

Demonstrates: Multi-source data ingestion, transformation logic, orchestration, repeatability, and modern data engineering practices.

## Features
- Live data extraction (can be run anytime for latest values)
- Clean separation of concerns (Extract → Transform → Load)
- Configurable via .env
- Ready for scheduling with GitHub Actions
- Extensible for Tableau, PySpark, Snowflake, etc.

## How to Run Locally

1. Install dependencies:
   pip install -r requirements.txt

2. Configure database and API:
   cp .env.example .env
   # Edit .env with your PostgreSQL credentials and FRED API key

3. Run the pipeline:
   python run_pipeline.py

## Project Structure
- extract.py — Data ingestion from FRED + Yahoo Finance
- transform.py — Data cleaning and structuring
- load.py — PostgreSQL loading
- orchestrator.py — Main ETL coordination
- config.py — Configuration

## Database Tables Created
- economic_indicators
- market_data

## Future Enhancements
- Scheduled runs via GitHub Actions
- Tableau Public visualizations
- Migration to Snowflake
- PySpark processing for larger scale
- Data quality checks and monitoring

---

## Sample Run

See [`pipeline_sample_run.txt`](pipeline_sample_run.txt) for a complete example execution output, including:
- Live data pulled from FRED and Yahoo Finance
- Database load confirmation
- Resulting table contents

---


Last updated: June 2026
Part of Josef Schulze Portfolio
