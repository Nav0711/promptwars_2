"""
analytics_service.py — BigQuery integration for historical election data.
Uses Application Default Credentials (ADC) on Cloud Run.
"""
import os
from typing import Optional

GCP_PROJECT    = os.getenv("GCP_PROJECT_ID", "promptwars2-494413")
BQ_DATASET     = os.getenv("BQ_DATASET",     "chunav_analytics")

# Historical turnout mock data for hackathon (BigQuery is seeded separately)
_MOCK_TURNOUT = [
    {"state": "Uttar Pradesh", "year": 2022, "turnout_pct": 60.5, "registered_voters": 152_000_000},
    {"state": "Uttar Pradesh", "year": 2017, "turnout_pct": 61.1, "registered_voters": 138_000_000},
    {"state": "Uttar Pradesh", "year": 2012, "turnout_pct": 59.4, "registered_voters": 124_000_000},
    {"state": "West Bengal",   "year": 2021, "turnout_pct": 78.3, "registered_voters":  73_000_000},
    {"state": "West Bengal",   "year": 2016, "turnout_pct": 77.1, "registered_voters":  68_000_000},
    {"state": "Bihar",         "year": 2020, "turnout_pct": 57.1, "registered_voters":  72_000_000},
    {"state": "Bihar",         "year": 2015, "turnout_pct": 56.8, "registered_voters":  68_000_000},
    {"state": "Maharashtra",   "year": 2024, "turnout_pct": 65.2, "registered_voters":  97_000_000},
    {"state": "Maharashtra",   "year": 2019, "turnout_pct": 61.4, "registered_voters":  89_000_000},
    {"state": "Tamil Nadu",    "year": 2021, "turnout_pct": 74.3, "registered_voters":  62_000_000},
    {"state": "Tamil Nadu",    "year": 2016, "turnout_pct": 73.2, "registered_voters":  58_000_000},
]

def get_turnout_trends(state: Optional[str] = None):
    """
    Returns historical voter turnout trends.
    Phase 2: Will query BigQuery directly.
    """
    try:
        from google.cloud import bigquery
        client = bigquery.Client(project=GCP_PROJECT)

        query = f"""
            SELECT state, year, turnout_pct, registered_voters
            FROM `{GCP_PROJECT}.{BQ_DATASET}.turnout_history`
            {f"WHERE state = '{state}'" if state else ""}
            ORDER BY state, year DESC
            LIMIT 30
        """
        result = client.query(query).result()
        return [dict(row) for row in result]

    except Exception as e:
        print(f"[analytics] BigQuery unavailable, using mock data: {e}")
        if state:
            return [r for r in _MOCK_TURNOUT if r["state"] == state]
        return _MOCK_TURNOUT

def get_national_summary():
    """Returns national-level election statistics."""
    try:
        from google.cloud import bigquery
        client = bigquery.Client(project=GCP_PROJECT)
        query = f"""
            SELECT
                COUNT(DISTINCT state) as total_states,
                AVG(turnout_pct) as avg_turnout,
                SUM(registered_voters) as total_registered
            FROM `{GCP_PROJECT}.{BQ_DATASET}.turnout_history`
            WHERE year = (SELECT MAX(year) FROM `{GCP_PROJECT}.{BQ_DATASET}.turnout_history`)
        """
        row = list(client.query(query).result())[0]
        return dict(row)
    except Exception:
        return {
            "total_states": 28,
            "avg_turnout": 67.4,
            "total_registered": 970_000_000,
        }
