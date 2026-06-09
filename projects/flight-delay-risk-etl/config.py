# Configuration for Flight Delay Risk ETL
from zoneinfo import ZoneInfo

AIRPORTS = {
    "STL": "KSTL",
    "ORD": "KORD",
    "ATL": "KATL",
    "DFW": "KDFW",
    "DEN": "KDEN",
    "LAX": "KLAX"
}

DB_FILE = "flight_history.db"
TABLE_NAME = "flight_risk_history"

# For future extensibility (e.g., different risk thresholds per airport)
AIRPORT_INFO = {
    "STL": {"name": "St. Louis Lambert International", "region": "Midwest"},
    "ORD": {"name": "Chicago O'Hare", "region": "Midwest"},
    "ATL": {"name": "Hartsfield-Jackson Atlanta", "region": "Southeast"},
    "DFW": {"name": "Dallas/Fort Worth", "region": "South"},
    "DEN": {"name": "Denver International", "region": "Mountain"},
    "LAX": {"name": "Los Angeles International", "region": "West Coast"}
}

# Visualization settings
IMAGE_OUTPUT = "latest_risk.png"

# Timezone
TZ = ZoneInfo("America/Chicago")