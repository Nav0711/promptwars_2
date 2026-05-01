"""
test_ai_tools.py — Tests for AI tool endpoints (quiz, explainer, summarizer).
Uses mocked Vertex AI responses to avoid real API calls in CI.
"""
from unittest.mock import patch, AsyncMock
import json


# ── Quiz Endpoint Tests ──────────────────────────────────────────────────────

class TestQuizEndpoint:
    """Tests for GET /v1/ai/quiz."""

    def test_quiz_returns_200(self, client):
        """Quiz endpoint should always return 200 (static fallback on AI failure)."""
        response = client.get("/v1/ai/quiz?language=en")
        assert response.status_code == 200

    def test_quiz_has_correct_structure(self, client):
        """Quiz response must have title, questions array, and total_questions."""
        response = client.get("/v1/ai/quiz?language=en")
        data = response.json()
        assert "title" in data
        assert "questions" in data
        assert "total_questions" in data
        assert data["total_questions"] == 5
        assert len(data["questions"]) == 5

    def test_quiz_question_structure(self, client):
        """Each question must have id, question text, 4 options, correct_answer, explanation, difficulty."""
        response = client.get("/v1/ai/quiz?language=en")
        data = response.json()
        for q in data["questions"]:
            assert "id" in q
            assert "question" in q
            assert "options" in q
            assert len(q["options"]) == 4
            assert "correct_answer" in q
            assert 0 <= q["correct_answer"] <= 3
            assert "explanation" in q
            assert "difficulty" in q
            assert q["difficulty"] in ("easy", "medium", "hard")

    def test_quiz_hindi_language(self, client):
        """Quiz in Hindi should return a valid quiz with Hindi title."""
        response = client.get("/v1/ai/quiz?language=hi")
        data = response.json()
        assert "title_hi" in data
        assert len(data["title_hi"]) > 0

    @patch("app.routers.ai_tools.generate_vertex_response")
    @patch("app.routers.ai_tools.retrieve_context")
    def test_quiz_with_mocked_ai(self, mock_rag, mock_vertex, client):
        """Quiz should parse a well-formed AI response correctly."""
        mock_rag.return_value = (["Test context"], [])
        mock_quiz = {
            "title": "Test Quiz",
            "title_hi": "टेस्ट क्विज़",
            "total_questions": 5,
            "questions": [
                {"id": i, "question": f"Q{i}?", "options": ["A", "B", "C", "D"],
                 "correct_answer": 0, "explanation": f"Exp{i}", "difficulty": "easy"}
                for i in range(1, 6)
            ],
        }
        mock_vertex.return_value = (json.dumps(mock_quiz), False)
        response = client.get("/v1/ai/quiz?language=en")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Quiz"

    @patch("app.routers.ai_tools.generate_vertex_response")
    @patch("app.routers.ai_tools.retrieve_context")
    def test_quiz_falls_back_on_invalid_json(self, mock_rag, mock_vertex, client):
        """Quiz should fall back to static quiz when AI returns invalid JSON."""
        mock_rag.return_value = ([], [])
        mock_vertex.return_value = ("This is not valid JSON at all", False)
        response = client.get("/v1/ai/quiz?language=en")
        assert response.status_code == 200
        data = response.json()
        assert data["total_questions"] == 5  # Static fallback has 5 questions

    @patch("app.routers.ai_tools.generate_vertex_response")
    @patch("app.routers.ai_tools.retrieve_context")
    def test_quiz_falls_back_on_ai_error(self, mock_rag, mock_vertex, client):
        """Quiz should fall back to static quiz when AI returns an error."""
        mock_rag.return_value = ([], [])
        mock_vertex.return_value = ("Error text", True)  # is_error=True
        response = client.get("/v1/ai/quiz?language=en")
        assert response.status_code == 200
        data = response.json()
        assert data["total_questions"] == 5


# ── Explainer Endpoint Tests ────────────────────────────────────────────────

class TestExplainerEndpoint:
    """Tests for POST /v1/ai/explain."""

    @patch("app.routers.ai_tools.generate_vertex_response")
    @patch("app.routers.ai_tools.retrieve_context")
    def test_explain_valid_term(self, mock_rag, mock_vertex, client):
        """Explainer should return a valid response for a known term."""
        mock_rag.return_value = (["NOTA allows voters to reject all candidates."], [])
        explanation = {
            "term": "NOTA",
            "simple_explanation": "NOTA lets voters reject all candidates.",
            "example": "Press the NOTA button on the EVM.",
            "source_url": "https://eci.gov.in",
        }
        mock_vertex.return_value = (json.dumps(explanation), False)
        response = client.post("/v1/ai/explain", json={"term": "NOTA", "language": "en"})
        assert response.status_code == 200
        data = response.json()
        assert data["term"] == "NOTA"
        assert len(data["simple_explanation"]) > 0

    @patch("app.routers.ai_tools.generate_vertex_response")
    @patch("app.routers.ai_tools.retrieve_context")
    def test_explain_graceful_fallback(self, mock_rag, mock_vertex, client):
        """Explainer should provide a fallback if AI returns invalid JSON."""
        mock_rag.return_value = ([], [])
        mock_vertex.return_value = ("invalid json!!!", False)
        response = client.post("/v1/ai/explain", json={"term": "EVM", "language": "en"})
        assert response.status_code == 200
        data = response.json()
        assert data["term"] == "EVM"
        assert "eci.gov.in" in data["source_url"]


# ── Summarizer Endpoint Tests ───────────────────────────────────────────────

class TestSummarizerEndpoint:
    """Tests for POST /v1/ai/summarize."""

    @patch("app.routers.ai_tools.generate_vertex_response")
    def test_summarize_valid_content(self, mock_vertex, client):
        """Summarizer should return structured summary for valid content."""
        summary = {
            "summary": "The ECI announced new polling dates for Bihar.",
            "key_points": ["Bihar Phase 1 on June 15", "Phase 2 on June 22"],
            "category": "Schedule",
        }
        mock_vertex.return_value = (json.dumps(summary), False)
        response = client.post("/v1/ai/summarize", json={
            "content": "ECI press release about Bihar elections...",
            "language": "en",
        })
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "key_points" in data
        assert isinstance(data["key_points"], list)
        assert data["category"] in ("Schedule", "MCC", "Candidate", "Results", "Notices", "General")

    @patch("app.routers.ai_tools.generate_vertex_response")
    def test_summarize_ai_error_returns_500(self, mock_vertex, client):
        """Summarizer should return 500 when AI fails."""
        mock_vertex.return_value = ("Error", True)
        response = client.post("/v1/ai/summarize", json={
            "content": "Some content",
            "language": "en",
        })
        assert response.status_code == 500
