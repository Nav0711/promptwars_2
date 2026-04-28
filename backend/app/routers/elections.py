from fastapi import APIRouter, HTTPException
from typing import Optional
from ..services.firestore import get_db

router = APIRouter(prefix="/elections", tags=["elections"])

@router.get("/active")
async def get_active_elections():
    db = get_db()
    if not db:
        # Fallback to mock data if Firestore is not connected
        return {
            "elections": [
                {
                    "state": "West Bengal",
                    "type": "Assembly By-Election",
                    "phases": [
                        { "phase": 1, "date": "2026-05-07", "constituencies": 42, "status": "UPCOMING" }
                    ]
                }
            ]
        }
        
    try:
        elections_ref = db.collection("elections")
        docs = elections_ref.stream()
        
        results = []
        for doc in docs:
            data = doc.to_dict()
            # Optionally add doc ID
            # data["id"] = doc.id
            results.append(data)
            
        return {"elections": results if results else [
            {
                "state": "Fallback State",
                "type": "Assembly By-Election",
                "phases": [{"phase": 1, "date": "2026-05-07", "constituencies": 42, "status": "UPCOMING"}]
            }
        ]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Firestore query failed: {str(e)}")

@router.get("/schedule")
async def get_schedule(state: Optional[str] = None, year: Optional[int] = None, type: Optional[str] = None):
    return {"schedule": []}

@router.get("/stats")
async def get_stats():
    return {
        "active_elections_count": 1,
        "days_until_next_phase": 10,
        "total_seats_up": 42,
        "eligible_voters_millions": 5.2
    }
