"""
test_tracker.py — Comprehensive tests for the election tracker endpoint.
Covers date edge cases, sorting logic, and response structure.
"""
from unittest.mock import patch
import datetime


def test_tracker_returns_phases(client):
    """Tracker must return a list of phases and a last_updated timestamp."""
    response = client.get("/v1/elections/tracker")
    assert response.status_code == 200
    data = response.json()
    assert "phases" in data
    assert "last_updated" in data
    assert isinstance(data["phases"], list)
    assert len(data["phases"]) > 0


def test_tracker_phase_has_required_fields(client):
    """Each phase object must contain all required fields."""
    response = client.get("/v1/elections/tracker")
    data = response.json()
    required = {"id", "state", "type", "phase", "date", "constituencies", "total_seats", "status", "days_away"}
    for phase in data["phases"]:
        assert required.issubset(phase.keys()), f"Missing keys in phase: {required - phase.keys()}"


def test_tracker_status_values_are_valid(client):
    """Status must be one of the three valid states."""
    response = client.get("/v1/elections/tracker")
    data = response.json()
    valid_statuses = {"UPCOMING", "VOTING_TODAY", "COMPLETED"}
    for phase in data["phases"]:
        assert phase["status"] in valid_statuses, f"Invalid status: {phase['status']}"


def test_tracker_sorting_order(client):
    """Phases should be sorted: VOTING_TODAY first, then UPCOMING (by days_away), then COMPLETED."""
    response = client.get("/v1/elections/tracker")
    data = response.json()
    order = {"VOTING_TODAY": 0, "UPCOMING": 1, "COMPLETED": 2}
    phases = data["phases"]
    for i in range(len(phases) - 1):
        curr_order = order[phases[i]["status"]]
        next_order = order[phases[i + 1]["status"]]
        if curr_order == next_order:
            assert phases[i]["days_away"] <= phases[i + 1]["days_away"]
        else:
            assert curr_order <= next_order


def test_tracker_next_phase_is_present(client):
    """next_phase should point to the first upcoming or voting-today phase."""
    response = client.get("/v1/elections/tracker")
    data = response.json()
    assert "next_phase" in data
    if data["next_phase"]:
        assert data["next_phase"]["status"] in ("UPCOMING", "VOTING_TODAY")


@patch("app.routers.elections.datetime")
def test_tracker_past_date_marks_completed(mock_dt, client):
    """A phase whose date has passed should be marked COMPLETED."""
    # Set 'today' to a date after all phase dates
    mock_dt.date.today.return_value = datetime.date(2027, 1, 1)
    mock_dt.date.fromisoformat = datetime.date.fromisoformat
    mock_dt.datetime.utcnow.return_value = datetime.datetime(2027, 1, 1)
    response = client.get("/v1/elections/tracker")
    data = response.json()
    for phase in data["phases"]:
        assert phase["status"] == "COMPLETED"


@patch("app.routers.elections.datetime")
def test_tracker_same_day_marks_voting_today(mock_dt, client):
    """A phase whose date matches today should be VOTING_TODAY."""
    mock_dt.date.today.return_value = datetime.date(2026, 5, 7)  # West Bengal phase
    mock_dt.date.fromisoformat = datetime.date.fromisoformat
    mock_dt.datetime.utcnow.return_value = datetime.datetime(2026, 5, 7)
    response = client.get("/v1/elections/tracker")
    data = response.json()
    wb_phase = next(p for p in data["phases"] if p["id"] == "phase-wb-1")
    assert wb_phase["status"] == "VOTING_TODAY"
    assert wb_phase["days_away"] == 0


@patch("app.routers.elections.datetime")
def test_tracker_future_date_marks_upcoming(mock_dt, client):
    """A phase whose date is in the future should be UPCOMING."""
    mock_dt.date.today.return_value = datetime.date(2026, 1, 1)  # Well before all phases
    mock_dt.date.fromisoformat = datetime.date.fromisoformat
    mock_dt.datetime.utcnow.return_value = datetime.datetime(2026, 1, 1)
    response = client.get("/v1/elections/tracker")
    data = response.json()
    for phase in data["phases"]:
        assert phase["status"] == "UPCOMING"
        assert phase["days_away"] > 0
