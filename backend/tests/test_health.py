"""
test_health.py — Smoke tests for health and root endpoints.
Validates the API is reachable and returns correct metadata.
"""


def test_root_returns_welcome(client):
    """Root endpoint must return a welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Chunav Saathi" in data["message"]


def test_health_check(client):
    """Health check must return ok status and correct version info."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert data["project"] == "promptwars2-494413"
    assert "vertex_ai" in data["ai_backend"]


def test_health_contains_all_fields(client):
    """Health check must include all expected metadata keys."""
    response = client.get("/health")
    data = response.json()
    expected_keys = {"status", "version", "ai_backend", "project"}
    assert expected_keys.issubset(data.keys())
