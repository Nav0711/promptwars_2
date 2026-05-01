"""
conftest.py — Shared test fixtures for Chunav Saathi backend tests.
Provides an HTTPX-backed async test client without requiring live GCP credentials.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Synchronous test client for FastAPI app."""
    return TestClient(app)
