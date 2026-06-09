# Updated Functional Requirements Document (FRD)

**Project Title:** Real-Time Flight Delay Risk ETL

**Version:** 2.0 (Updated with JSON API, Miles Conversion, Enhanced Features)

---

## 1. Project Overview & Objectives

This project builds an automated, end-to-end **Data Product** that ingests real-time weather data from NOAA, calculates a **Flight Delay Risk Score** (0–100) for six major U.S. airports (including STL), stores historical data in DuckDB, and generates visual insights via Seaborn.

The pipeline runs entirely on **serverless, open-source infrastructure** inside GitHub Actions. No API keys or logins required. The final output includes a dynamic dashboard image (`latest_risk.png`) automatically committed and displayed in the project README.md for immediate portfolio impact.

**Key Goals:**
- Demonstrate senior-level ETL patterns: multi-source ingestion, transformation/feature engineering, idempotent warehousing, CI/CD visualization.
- Provide live, on-demand updates for recruiters and viewers.
- Maintain full local portability and zero-cost operation.

---

## 2. System Architecture & High-Level Data Flow

```
NOAA NWS JSON API (Public)     Airport Config (Static)
          |                               |
          +--------------+---------------+
                         |
                         v
               GitHub Actions (Python ETL)
                         |
                         v
                   DuckDB (flight_history.db)
                         |
                         v
                 Seaborn Visualization
                         |
                         v
               Git Commit + Push (README + PNG + DB)
```

---

## 3. Data Sources

### 3.1 Weather Data (Dynamic - NOAA NWS JSON API)
- **Provider:** National Oceanic and Atmospheric Administration (NOAA) National Weather Service.
- **Endpoint:** `https://api.weather.gov/stations/{ICAO}/observations/latest`
- **Format:** Clean JSON (no XML parsing needed).
- **Key Fields:** `observationTime`, `windSpeed` (km/h), `visibility` (meters), `textDescription`, `temperature`, `windGust`, etc.
- **Access:** Public HTTP GET via `requests`. No keys required.
- **Frequency:** Daily scheduled + manual trigger.

**Unit Conversions:**
- Wind Speed: km/h → mph (`value / 1.60934`)
- Visibility: meters → miles (`value / 1609.34`)

### 3.2 Airport Reference Data (Static)
Exactly six major U.S. hubs:

1. **STL** - St. Louis Lambert International (KSTL)
2. **ORD** - Chicago O'Hare (KORD)
3. **ATL** - Atlanta Hartsfield-Jackson (KATL)
4. **DFW** - Dallas/Fort Worth (KDFW)
5. **DEN** - Denver International (KDEN)
6. **LAX** - Los Angeles International (KLAX)

---

## 4. Functional Specifications

### 4.1 Workflow Orchestration
- **Platform:** GitHub Actions.
- **Triggers:**
  - Scheduled: Daily at 06:00 UTC (`0 6 * * *`).
  - Manual: `workflow_dispatch`.

### 4.2 Data Transformation & Cleansing
- Map NOAA station codes (KXXX) → 3-letter airport codes.
- Strict filtering to the 6 target airports.
- Type casting and unit conversions.
- Default values for missing data: wind=0, visibility=10 miles, precip=0.
- Timestamp standardization to UTC.

### 4.3 Feature Engineering: Flight Delay Risk Score
**Formula (0–100 scale):**

```python
base = (wind_mph * 1.5) + (gust_mph * 0.8 if gust else 0)
visibility_penalty = 30 if vis_miles < 3 else 50 if vis_miles < 1 else 0
precip_penalty = 40 if any(kw in text.lower() for kw in ["snow", "thunderstorm", "ice", "freezing", "rain", "fog"]) else 0
temp_penalty = 15 if temp_c and (temp_c < -5 or temp_c > 35) else 0

risk_score = min(100, int(base + visibility_penalty + precip_penalty + temp_penalty))
```

- **Output:** Integer score per airport + raw component breakdown (for transparency).

### 4.4 Data Storage (DuckDB)
- Database: `flight_history.db` (file-based).
- Table: `flight_risk_history` with strict schema.
- **Idempotent Upsert:** `INSERT OR REPLACE` on composite key `(airport_code, observation_time)`.
- Retains full history for 24h+ trend analysis.

---

## 5. Visualization & Presentation Layer

### 5.1 Output
- High-resolution PNG: `latest_risk.png` (DPI 300).
- Theme: `sns.set_theme(style="whitegrid")`.

### 5.2 Dashboard Components
1. **Multi-Airport 24-Hour Sparklines** (FacetGrid or subplots):
   - One subplot per airport.
   - X: Time (last 24 hours).
   - Y: Risk Score (fixed 0–100 scale).
   - Color: Gradient (palette="flare").

2. **Summary Bar Chart** (Current risk levels across all airports).

3. **README Integration:**
   ```markdown
   ### Real-Time Flight Delay Risk Tracker
   ![Latest 24-Hour Risk Scores](./latest_risk.png)
   ```

---

## 6. Non-Functional Requirements

- **Self-Contained:** All code, config, and data in the repo.
- **Resilience:** Graceful error handling for network issues (log + no corrupt output).
- **Portability:** Runnable locally with `python etl.py`.
- **Maintainability:** Config-driven airports, modular scripts (`config.py`, `etl.py`, `visualize.py`).
- **Dependencies:** Minimal (`requests`, `pandas`, `duckdb`, `seaborn`, `matplotlib`).

---

**Project Folder Structure (Recommended):**
```
projects/flight-delay-risk-etl/
├── config.py
├── etl.py
├── visualize.py
├── requirements.txt
├── .env.example
├── flight_history.db          # (committed)
├── latest_risk.png            # (auto-updated)
├── .github/workflows/
│   └── update-risk.yml
├── README.md
└── UPDATED_FRD.md             # This document
```

This FRD serves as the single source of truth for development. All implementation must align with these specs.

---

**Approval Status:** ✅ Accepted (JSON + Miles + All Suggestions)  
**Next:** Proceed to project scaffolding and code.
