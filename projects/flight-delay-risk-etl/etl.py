import requests
import logging
import time
from datetime import datetime, timedelta
import duckdb
import pandas as pd
from config import AIRPORTS, DB_FILE, TABLE_NAME

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_numeric(value):
    """Safely extract numeric value from NOAA's nested JSON format"""
    if value is None:
        return 0.0
    if isinstance(value, dict) and 'value' in value:
        val = value['value']
        return float(val) if val is not None else 0.0
    if isinstance(value, (int, float)):
        return float(value)
    return 0.0

def calculate_risk_score(props):
    """Calculate Flight Delay Risk Score"""
    if not props:
        return 0, {}

    wind_kmh = extract_numeric(props.get('windSpeed'))
    wind_mph = wind_kmh / 1.60934

    gust_kmh = extract_numeric(props.get('windGust'))
    gust_mph = gust_kmh / 1.60934

    vis_meters = extract_numeric(props.get('visibility'))
    vis_miles = vis_meters / 1609.34

    temp_c = extract_numeric(props.get('temperature'))
    text_desc = str(props.get('textDescription', '') or '')

    base = (wind_mph * 1.5) + (gust_mph * 0.8)
    visibility_penalty = 50 if vis_miles < 1 else 30 if vis_miles < 3 else 0
    precip_keywords = ["snow", "thunderstorm", "ice", "freezing", "rain", "fog", "hail"]
    precip_penalty = 40 if any(kw in text_desc.lower() for kw in precip_keywords) else 0
    temp_penalty = 15 if (temp_c < -5 or temp_c > 35) else 0

    raw_score = base + visibility_penalty + precip_penalty + temp_penalty
    risk_score = max(0, min(100, int(raw_score)))

    components = {
        'base': round(base, 1),
        'vis': visibility_penalty,
        'precip': precip_penalty,
        'temp': temp_penalty
    }

    return risk_score, components

def init_db():
    """Create table if it doesn't exist"""
    conn = duckdb.connect(DB_FILE)
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            airport_code VARCHAR,
            observation_time TIMESTAMP,
            risk_score INTEGER,
            wind_mph DOUBLE,
            visibility_miles DOUBLE,
            temperature_c DOUBLE,
            text_description VARCHAR,
            components VARCHAR,
            inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.close()
    logging.info("Database table ready")

def prune_old_data():
    """Keep only the last 24 hours of data"""
    conn = duckdb.connect(DB_FILE)
    cutoff = (datetime.utcnow() - timedelta(hours=24)).isoformat()
    
    # Count rows before deletion
    before = conn.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()[0]
    
    # Delete old records
    conn.execute(f"DELETE FROM {TABLE_NAME} WHERE observation_time < '{cutoff}'")
    
    after = conn.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()[0]
    deleted = before - after
    
    if deleted > 0:
        logging.info(f"Pruned {deleted} old records (older than 24 hours)")
    conn.close()

def save_to_duckdb(records):
    """Save new records"""
    if not records:
        return
    conn = duckdb.connect(DB_FILE)
    df = pd.DataFrame(records)
    if 'components' in df.columns:
        df['components'] = df['components'].astype(str)
    
    conn.execute(f"""
        INSERT INTO {TABLE_NAME} 
        (airport_code, observation_time, risk_score, wind_mph, 
         visibility_miles, temperature_c, text_description, components)
        SELECT * FROM df
    """)
    conn.close()
    logging.info(f"Saved {len(records)} new records")

def main():
    logging.info("Starting Flight Delay Risk ETL")
    
    init_db()
    prune_old_data()
    
    all_records = []
    
    for airport_code, icao in AIRPORTS.items():
        logging.info(f"Processing {airport_code} ({icao})")
        url = f"https://api.weather.gov/stations/{icao}/observations/latest"
        
        try:
            response = requests.get(url, timeout=15, 
                                  headers={'User-Agent': 'FlightDelayRiskPortfolio/1.0'})
            response.raise_for_status()
            data = response.json()
            
            props = data.get('properties', {})
            if not props or not props.get('timestamp'):
                logging.warning(f"No valid data for {airport_code}")
                continue
                
            risk_score, components = calculate_risk_score(props)
            
            record = {
                'airport_code': airport_code,
                'observation_time': props.get('timestamp'),
                'risk_score': risk_score,
                'wind_mph': extract_numeric(props.get('windSpeed')) / 1.60934,
                'visibility_miles': extract_numeric(props.get('visibility')) / 1609.34,
                'temperature_c': extract_numeric(props.get('temperature')),
                'text_description': props.get('textDescription', ''),
                'components': components
            }
            
            all_records.append(record)
            time.sleep(0.7)
            
        except Exception as e:
            logging.error(f"Error processing {airport_code}: {e}")
    
    save_to_duckdb(all_records)
    logging.info("ETL completed successfully")

if __name__ == "__main__":
    main()