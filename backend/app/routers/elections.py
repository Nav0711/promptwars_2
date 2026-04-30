from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from ..services.firestore import get_db

router = APIRouter(prefix="/elections", tags=["elections"])

# ── Active Elections ──────────────────────────────────────────────────────────

@router.get("/active")
async def get_active_elections():
    db = get_db()
    if not db:
        return {"elections": _mock_elections()}

    try:
        docs = db.collection("elections").stream()
        results = [doc.to_dict() for doc in docs]
        return {"elections": results or _mock_elections()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Firestore query failed: {str(e)}")


@router.get("/schedule")
async def get_schedule(
    state: Optional[str] = None,
    year:  Optional[int] = None,
    type:  Optional[str] = None,
):
    db = get_db()
    if not db:
        return {"schedule": _mock_elections()}

    try:
        ref = db.collection("elections")
        if state:
            ref = ref.where("state", "==", state)
        docs = ref.stream()
        results = [doc.to_dict() for doc in docs]
        return {"schedule": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_stats():
    db = get_db()
    if not db:
        return _mock_stats()

    try:
        docs = list(db.collection("elections").stream())
        total_seats = sum(
            doc.to_dict().get("total_seats", 0) for doc in docs
        )
        eligible_voters = sum(
            doc.to_dict().get("eligible_voters_millions", 0) for doc in docs
        )
        return {
            "active_elections_count": len(docs),
            "days_until_next_phase": 6,
            "total_seats_up": total_seats,
            "eligible_voters_millions": round(eligible_voters, 1),
        }
    except Exception as e:
        return _mock_stats()


# ── FAQs ──────────────────────────────────────────────────────────────────────

@router.get("/faqs")
async def get_faqs(
    category: Optional[str] = None,
    search:   Optional[str] = None,
    language: Optional[str] = "en",
):
    db = get_db()
    if not db:
        return {"faqs": _mock_faqs()}

    try:
        ref = db.collection("faqs")
        if category:
            ref = ref.where("category", "==", category)
        docs = ref.stream()
        results = [doc.to_dict() for doc in docs]

        # Simple full-text filter on the Python side
        if search:
            s = search.lower()
            results = [
                faq for faq in results
                if s in faq.get("question", "").lower()
                or s in faq.get("answer", "").lower()
            ]

        return {"faqs": results or _mock_faqs()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Booth Finder ──────────────────────────────────────────────────────────────

@router.get("/booth/find")
async def find_booth(
    epic_id:  Optional[str] = Query(None, description="Voter ID / EPIC number"),
    pincode:  Optional[str] = Query(None, description="PIN code for geo-lookup"),
    state:    Optional[str] = Query(None, description="State name"),
):
    """
    Currently delegates to the official ECI portal with a deep-link.
    Phase 2: Integrate Firestore booth database.
    """
    if not epic_id and not pincode:
        raise HTTPException(status_code=400, detail="Provide epic_id or pincode.")

    deeplink = "https://voterportal.eci.gov.in/booth-location"
    if epic_id:
        deeplink += f"?epicNo={epic_id}"

    return {
        "status": "redirect",
        "message": "Booth data lookup is powered by the official ECI portal.",
        "portal_url": deeplink,
        "helpline": "1950",
        "note": "You can also call the National Voter Helpline: 1950 (toll-free)",
    }


# ── Mock Data Helpers ─────────────────────────────────────────────────────────

def _mock_elections():
    return [
        {
            "state": "West Bengal",
            "type": "Assembly By-Election",
            "phases": [
                {"phase": 1, "date": "2026-05-07", "constituencies": 42, "status": "UPCOMING"}
            ],
            "total_seats": 42,
            "eligible_voters_millions": 5.2,
        },
        {
            "state": "Bihar",
            "type": "Assembly General Election",
            "phases": [
                {"phase": 1, "date": "2026-06-15", "constituencies": 80, "status": "UPCOMING"},
                {"phase": 2, "date": "2026-06-22", "constituencies": 83, "status": "UPCOMING"},
            ],
            "total_seats": 243,
            "eligible_voters_millions": 74.3,
        },
    ]


def _mock_stats():
    return {
        "active_elections_count": 2,
        "days_until_next_phase": 6,
        "total_seats_up": 285,
        "eligible_voters_millions": 79.5,
    }


def _mock_faqs():
    return [
        {
            "category": "Voter Registration",
            "question": "How do I register as a voter in India?",
            "answer": "Visit voterportal.eci.gov.in and fill Form 6. You must be an Indian citizen aged 18 or above.",
            "source_url": "https://voterportal.eci.gov.in",
        },
        {
            "category": "NOTA",
            "question": "What is NOTA?",
            "answer": "NOTA (None of the Above) allows voters to reject all candidates without abstaining. Introduced by the Supreme Court in 2013.",
            "source_url": "https://eci.gov.in/faqs/",
        },
    ]
