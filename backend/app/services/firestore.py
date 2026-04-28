from google.cloud import firestore
import os

# To use this, you need GOOGLE_APPLICATION_CREDENTIALS
db = None

def get_db():
    global db
    if not db:
        try:
            # Requires valid GCP credentials
            db = firestore.Client()
        except Exception as e:
            print("Warning: Could not initialize Firestore Client. Make sure credentials are set.")
    return db
