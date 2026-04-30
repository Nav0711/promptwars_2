"""
firestore.py — Lazy singleton Firestore client.
Uses GCP_PROJECT_ID env var so the same code runs locally and on Cloud Run.
"""
from google.cloud import firestore
import os

GCP_PROJECT = os.getenv("GCP_PROJECT_ID", "promptwars2-494413")

db = None

def get_db():
    global db
    if not db:
        try:
            db = firestore.Client(project=GCP_PROJECT)
        except Exception as e:
            print(f"[firestore] Warning: Could not initialize Firestore Client: {e}")
            print("[firestore] Make sure GOOGLE_APPLICATION_CREDENTIALS or ADC is configured.")
    return db
