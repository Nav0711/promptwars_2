# Chunav Saathi — Submission Guidelines Compliance

This document outlines how the **Chunav Saathi** platform specifically addresses the evaluation criteria and submission guidelines, focusing on the latest quality engineering iterations.

---

## 1. Testing Coverage
> *"Testing coverage appears limited to core paths, with gaps around edge cases and integration flows."*

**How we solved it:**
- **Edge Cases:** Implemented a robust `pytest` suite for the backend (`test_tracker.py`). We use Python's `unittest.mock` to simulate time travel (past dates, exact polling day, future dates) to guarantee the phase-tracker logic handles all edge cases without relying on live databases.
- **Integration Flows & Fallbacks:** In `test_ai_tools.py`, we test the integration between our API and Vertex AI. We explicitly test failure modes (e.g., when the AI returns invalid JSON or fails to connect). The tests verify that our platform gracefully falls back to static content rather than crashing.
- **Safety Testing:** `test_guardrails.py` contains 15+ automated tests verifying that political biases, predictions, and prompt injection attempts (in both English and Hindi) are safely blocked.

## 2. Accessibility (A11y)
> *"Early-stage accessibility patterns are visible, with opportunities around structure, navigation flow, and assistive support maturity."*

**How we solved it:**
- **Navigation Flow:** Added an invisible, focusable "Skip to main content" link at the very top of `layout.tsx` to allow keyboard users to bypass the navigation bar.
- **Assistive Support Maturity:** 
    - The `ChatWidget` now uses `aria-live="polite"` so screen readers dynamically announce when the AI finishes typing a response.
    - We added a **Focus Trap** to the chat input when it opens.
    - The `VoterQuiz` options are now structured with `role="radiogroup"` and `role="radio"`, utilizing `aria-checked` and `aria-labelledby` so visually impaired users hear exactly what option they are selecting.
- **Structure:** Updated `layout.tsx` to include proper ARIA landmarks (`role="main"`).

## 3. Security Implementation
> *"Security implementation demonstrates strong defensive practices and awareness of common risk vectors."*

**How we elevated it further:**
- **Rate Limiting:** We implemented an in-memory Sliding Window Rate Limiter (`rate_limiter.py`) injected as a FastAPI dependency (`Depends(ai_rate_limiter)`) into all AI routes (`/v1/chat`, `/quiz`, `/explain`, `/summarize`). This defends against DDoS attempts and prevents malicious users from exhausting our Google Cloud Vertex AI quota.

## 4. Codebase Quality & Maintainability
> *"Codebase quality appears strong, showing clear structure, maintainability, and alignment across components."*

**How we elevated it further:**
- **Global Error Boundary:** We wrapped the entire React tree in `ErrorBoundary.tsx`. If a catastrophic render failure occurs, the user sees a polished "Something went wrong" screen with a recovery button, rather than an unhandled white screen.
- **Structured JSON Logging:** Added `logger.py` to the backend. All AI requests now emit structured JSON logs containing latency, language, and guardrail triggers. This makes production debugging in Google Cloud Logging vastly easier.

## 5. Performance Behavior
> *"Performance behavior is consistently efficient, showing stable load times and optimized resource usage."*

**How we elevated it further:**
- **Dynamic Imports (Lazy Loading):** The `IndiaElectionMap` component uses heavy TopoJSON datasets and SVG parsing. We updated `page.tsx` to use Next.js `dynamic()` imports with `ssr: false`. This removes the heavy map logic from the initial JavaScript bundle, significantly speeding up the Time to Interactive (TTI). While the map chunks load, a sleek `Skeleton` component is displayed.
