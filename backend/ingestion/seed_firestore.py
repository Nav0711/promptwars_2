"""
seed_firestore.py
Run this script ONCE to seed Firestore with:
  1. Live election schedule data (elections collection)
  2. FAQ Q&A pairs (faqs collection)
  3. RAG knowledge chunks with embeddings (rag_chunks collection)

Usage:
  export GCP_PROJECT_ID=promptwars2-494413
  export GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa.json
  python seed_firestore.py
"""
import os
import sys
import datetime

# Add backend root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from google.cloud import firestore
from ingestion.embedder import generate_embedding

GCP_PROJECT = os.getenv("GCP_PROJECT_ID", "promptwars2-494413")

# ── Data ──────────────────────────────────────────────────────────────────────

ELECTIONS = [
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
            {"phase": 3, "date": "2026-06-29", "constituencies": 80, "status": "UPCOMING"},
        ],
        "total_seats": 243,
        "eligible_voters_millions": 74.3,
    },
    {
        "state": "Uttar Pradesh",
        "type": "By-Election",
        "phases": [
            {"phase": 1, "date": "2026-07-10", "constituencies": 10, "status": "UPCOMING"}
        ],
        "total_seats": 10,
        "eligible_voters_millions": 10.1,
    },
]

FAQS = [
    {
        "category": "Voter Registration",
        "question": "How do I register as a voter in India?",
        "question_hi": "मैं भारत में मतदाता के रूप में कैसे पंजीकरण करूँ?",
        "answer": "You can register online at voterportal.eci.gov.in or the Voter Helpline App. Fill Form 6 with your Aadhaar and address proof. You must be a citizen aged 18 or above.",
        "source_url": "https://voterportal.eci.gov.in",
    },
    {
        "category": "Voter Registration",
        "question": "How do I check my voter registration status?",
        "answer": "Visit electoralsearch.eci.gov.in and enter your EPIC number or personal details (Name, DOB, State) to check if you are enrolled on the electoral roll.",
        "source_url": "https://electoralsearch.eci.gov.in",
    },
    {
        "category": "Voting Process",
        "question": "What documents do I need to carry on election day?",
        "answer": "You must carry your EPIC (Voter ID) card. Alternatively, the ECI accepts 12 other photo ID documents: Aadhaar card, Passport, Driving License, PAN card, etc.",
        "source_url": "https://eci.gov.in/voter/",
    },
    {
        "category": "EVM & Technology",
        "question": "How does the Electronic Voting Machine (EVM) work?",
        "answer": "An EVM consists of a Control Unit and Balloting Unit. The presiding officer activates the ballot. You press the button next to your chosen candidate. The vote is recorded securely. A VVPAT slip shows your choice for 7 seconds to confirm.",
        "source_url": "https://eci.gov.in/evm/",
    },
    {
        "category": "NOTA",
        "question": "What is NOTA and how do I use it?",
        "answer": "NOTA (None of the Above) is an option on the EVM that allows voters to reject all candidates without abstaining. It appears as the last option on the ballot. If NOTA gets the highest votes, a re-election is held.",
        "source_url": "https://eci.gov.in/faqs/",
    },
    {
        "category": "Model Code of Conduct",
        "question": "What is the Model Code of Conduct (MCC)?",
        "answer": "The MCC is a set of guidelines issued by the ECI for political parties and candidates during elections. It comes into effect from the date of announcement of the election schedule and remains in force till the completion of the election process.",
        "source_url": "https://eci.gov.in/mcc/",
    },
    {
        "category": "Polling Booth",
        "question": "How do I find my polling booth?",
        "answer": "You can find your polling booth at voterportal.eci.gov.in or by searching on the Voter Helpline App. Enter your EPIC number or personal details. You can also call the 1950 Voter Helpline.",
        "source_url": "https://voterportal.eci.gov.in/booth-location",
    },
    {
        "category": "Complaints",
        "question": "How do I report an election violation?",
        "answer": "You can report violations using the cVIGIL app (available on Android and iOS). You can also call the 1950 National Voter Helpline. Photos and videos can be submitted as evidence.",
        "source_url": "https://cvigil.eci.gov.in",
    },
    {
        "category": "Special Provisions",
        "question": "Can senior citizens and disabled voters vote from home?",
        "answer": "Yes. The ECI provides Postal Ballot facility for voters aged 85 and above and Persons with Disabilities (PwD). They can vote from home with the help of a polling officer who visits them.",
        "source_url": "https://eci.gov.in/voters/postal-ballot/",
    },
    {
        "category": "Candidates",
        "question": "How can I find information about candidates contesting in my constituency?",
        "answer": "Candidate information including criminal records, assets, and liabilities are available on the ECI affidavit portal at affidavit.eci.gov.in. You can also check myneta.info for a user-friendly view.",
        "source_url": "https://affidavit.eci.gov.in",
    },
]

RAG_CHUNKS = [
    {
        "text": "The Voter ID card, officially called the EPIC (Electors Photo Identity Card), is issued by the Election Commission of India. It is mandatory to present it at the polling booth to vote. If you don't have an EPIC, you may use 12 alternative photo ID documents approved by ECI, including Aadhaar, Passport, Driving License, or PAN Card.",
        "source_url": "https://eci.gov.in/voter/",
        "category": "voter_id",
    },
    {
        "text": "The Model Code of Conduct (MCC) comes into effect from the date of announcement of the General Election / State Election schedule by the Election Commission of India. It remains in force until the completion of the election process. The MCC prohibits use of government resources for campaigning, bribery, and inflammatory speeches.",
        "source_url": "https://eci.gov.in/mcc/",
        "category": "mcc",
    },
    {
        "text": "NOTA (None of the Above) was introduced by the Supreme Court of India in 2013. It allows voters to cast a negative vote without abstaining. The NOTA button appears as the last option on the EVM. Even if NOTA receives the highest votes, the candidate with the next highest votes wins (as per current rules in most states).",
        "source_url": "https://eci.gov.in/faqs/nota",
        "category": "nota",
    },
    {
        "text": "Voter registration in India is done through Form 6 for new registrations, Form 7 for deletion of name, Form 8 for corrections and updates. You must be an Indian citizen, aged 18 or above, and ordinarily resident in the constituency. Registration can be done online at voterportal.eci.gov.in or offline at your local Electoral Registration Officer (ERO).",
        "source_url": "https://voterportal.eci.gov.in",
        "category": "registration",
    },
    {
        "text": "The Conduct of Elections Rules, 1961, govern the entire election process in India. Key provisions include secrecy of ballot (Section 128), prohibition on canvassing within 100 meters of a polling station (Section 130), and prohibition on carrying arms near polling stations (Section 134B).",
        "source_url": "https://eci.gov.in/acts-rules/conduct-of-elections-rules-1961/",
        "category": "rules",
    },
    {
        "text": "Electronic Voting Machines (EVMs) were first used on an experimental basis in 1982 (Kerala by-poll) and were used in all Indian general elections from 2004 onwards. EVMs are manufactured by BEL (Bharat Electronics Limited) and ECIL (Electronics Corporation of India Limited). They are tamper-proof, standalone devices that do not connect to any network.",
        "source_url": "https://eci.gov.in/evm/",
        "category": "evm",
    },
    {
        "text": "The Voter Verifiable Paper Audit Trail (VVPAT) is a printer attached to the EVM that prints a paper slip showing the party symbol and candidate name for whom the vote was cast. This slip is visible for 7 seconds through a transparent window. The VVPAT slip then falls into a sealed box. VVPAT was introduced in 2013 and is now used in all constituencies.",
        "source_url": "https://eci.gov.in/evm/vvpat/",
        "category": "vvpat",
    },
    {
        "text": "The cVIGIL app allows citizens to report Model Code of Conduct (MCC) violations and distribution of cash or gifts to influence voters. Users can capture photo or video evidence and submit it directly to the ECI. The complaint must be filed within 100 minutes of the violation. Vigilance teams are dispatched within 100 minutes of receiving a complaint.",
        "source_url": "https://cvigil.eci.gov.in",
        "category": "complaints",
    },
]

# ── Seed Functions ────────────────────────────────────────────────────────────

def seed_elections(db):
    print("\n📊 Seeding elections collection...")
    for election in ELECTIONS:
        doc_id = election["state"].lower().replace(" ", "_")
        db.collection("elections").document(doc_id).set(election)
        print(f"  ✅ {election['state']}")

def seed_faqs(db):
    print("\n❓ Seeding faqs collection...")
    for i, faq in enumerate(FAQS):
        db.collection("faqs").document(f"faq_{i+1:03d}").set(faq)
        print(f"  ✅ FAQ {i+1}: {faq['question'][:50]}...")

def seed_rag_chunks(db):
    print("\n🔮 Seeding rag_chunks collection with Vertex AI embeddings...")
    for i, chunk in enumerate(RAG_CHUNKS):
        print(f"  Embedding chunk {i+1}/{len(RAG_CHUNKS)}: {chunk['category']}...")
        embedding = generate_embedding(chunk["text"])
        chunk_data = {
            **chunk,
            "embedding": embedding,
            "created_at": datetime.datetime.utcnow().isoformat(),
        }
        db.collection("rag_chunks").document(f"chunk_{i+1:03d}").set(chunk_data)
        print(f"  ✅ chunk_{i+1:03d} ({len(embedding)}d vector)")

def main():
    print(f"🚀 Connecting to Firestore in project: {GCP_PROJECT}")
    db = firestore.Client(project=GCP_PROJECT)
    print("✅ Firestore connected.")

    seed_elections(db)
    seed_faqs(db)
    seed_rag_chunks(db)

    print("\n🎉 Firestore seeding complete!")
    print("📋 Collections created: elections, faqs, rag_chunks")

if __name__ == "__main__":
    main()
