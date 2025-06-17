from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
import crud
from schemas import MarginChart, TurnoutChart, ConstituencyData, PartyDistribution
from schemas import SummaryData, SeatDistribution, VoteShare, PartyInfo

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://votermitra.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "VoterMitra API is running."}

@app.get("/constituency/margin-comparison", response_model=List[MarginChart])
def margin_chart(year: int, election_type: str, session: Session = Depends(get_session)):
    try:
        return crud.get_margin_chart(session, year, election_type)
    except Exception as e:
        print(f"Error in /margin-comparison: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/constituency/voter-turnout", response_model=List[TurnoutChart])
def turnout_chart(year: int, election_type: str, state: str, session: Session = Depends(get_session)):
    try:
        return crud.get_turnout_chart(session, year, election_type, state)
    except Exception as e:
        print(f"Error in /voter-turnout: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/constituency/top-vs", response_model=List[ConstituencyData])
def top_vs(state: str, session: Session = Depends(get_session)):
    try:
        return crud.get_top_vs_constituencies(session, state)
    except Exception as e:
        print(f"Error in /top-vs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/constituency/party-distribution", response_model=List[PartyDistribution])
def party_distribution(state: str, year: int, session: Session = Depends(get_session)):
    try:
        data = crud.get_party_distribution(session, state, year)
        print(f"Returned data: {data}")  # Debug log
        return data
    except Exception as e:
        print(f"Error in /party-distribution: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/Home/lok-sabha/summary", response_model=SummaryData)
def lok_sabha_summary(session: Session = Depends(get_session)):
    try:
        return crud.get_lok_sabha_summary(session)
    except Exception as e:
        print(f"Error in /lok-sabha/summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/Home/lok-sabha/seat-distribution", response_model=List[SeatDistribution])
def seat_distribution(session: Session = Depends(get_session)):
    try:
        return crud.get_seat_distribution(session)
    except Exception as e:
        print(f"Error in /lok-sabha/seat-distribution: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/Home/lok-sabha/vote-share", response_model=List[VoteShare])
def vote_share(session: Session = Depends(get_session)):
    try:
        return crud.get_vote_share(session)
    except Exception as e:
        print(f"Error in /lok-sabha/vote-share: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/Home/lok-sabha/party-info", response_model=List[PartyInfo])
def party_info(session: Session = Depends(get_session)):
    try:
        return crud.get_national_regional_parties(session)
    except Exception as e:
        print(f"Error in /lok-sabha/party-info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

from schemas import ComparativeAnalysis

@app.get("/Home/results/{state}")
def get_state_election_data(state: str, session: Session = Depends(get_session)):
    try:
        year = 2024
        election_type = "Vidhan Sabha"

        # Top 5 turnout chart
        summary = crud.get_turnout_chart(session, year=year, election_type=election_type, state=state)
        if not summary:
            raise HTTPException(status_code=404, detail="No turnout data found")

        # Party-wise seat distribution
        raw_seat_data = crud.get_party_distribution(session, state=state, year=year)
        total_votes = sum(p['votes'] for p in raw_seat_data)
        seat_distribution = [
            {
                "party": p["party"],
                "percentage": round((p["votes"] / total_votes) * 100, 1) if total_votes else 0.0
            }
            for p in raw_seat_data
        ]

        # Party-wise vote share (for India-level 2024 LS)
        vote_share_data = crud.get_vote_share(session)
        vote_share = [
            {"party": p["party"], "vote_share": p["vote_share"]}
            for p in vote_share_data
        ]

        return {
            "state": state.title(),
            "summary": summary,
            "seat_distribution": seat_distribution,
            "vote_share": vote_share
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/Home/lok-sabha/comparative-analysis", response_model=ComparativeAnalysis)
def comparative_analysis(session: Session = Depends(get_session)):
    try:
        return crud.get_comparative_analysis(session)
    except Exception as e:
        print(f"Error in /comparative-analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)
