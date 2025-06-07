from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
import crud
from schemas import MarginChart, TurnoutChart, ConstituencyData, PartyDistribution

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

@app.get("/margin-comparison", response_model=List[MarginChart])
def margin_chart(year: int, election_type: str, session: Session = Depends(get_session)):
    try:
        return crud.get_margin_chart(session, year, election_type)
    except Exception as e:
        print(f"Error in /margin-comparison: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/voter-turnout", response_model=List[TurnoutChart])
def turnout_chart(year: int, election_type: str, state: str, session: Session = Depends(get_session)):
    try:
        return crud.get_turnout_chart(session, year, election_type, state)
    except Exception as e:
        print(f"Error in /voter-turnout: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/top-vs", response_model=List[ConstituencyData])
def top_vs(state: str, session: Session = Depends(get_session)):
    try:
        return crud.get_top_vs_constituencies(session, state)
    except Exception as e:
        print(f"Error in /top-vs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/party-distribution", response_model=List[PartyDistribution])
def party_distribution(state: str, year: int, session: Session = Depends(get_session)):
    try:
        data = crud.get_party_distribution(session, state, year)
        print(f"Returned data: {data}")  # Debug log
        return data
    except Exception as e:
        print(f"Error in /party-distribution: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)
