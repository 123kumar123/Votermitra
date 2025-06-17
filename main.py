from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import schemas


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

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import crud
import models
from schemas import SeatDistribution, VoteShare, PartyCount, PartyCard

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API: Party-wise seat distribution (with year & optional state filter)
@app.get("/Home/party-seat-distribution", response_model=list[schemas.PartyShare])
def seat_distribution(elect_type: str, year: int, state: str = None, db: Session = Depends(get_db)):
    try:
        return crud.get_party_seat_distribution(db, elect_type, year, state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# API: Party-wise vote share (with year & optional state filter)
@app.get("/Home/party-vote-share", response_model=list[schemas.PartyShare])
def vote_share(elect_type: str, year: int, state: str = None, db: Session = Depends(get_db)):
    try:
        return crud.get_party_vote_share(db, elect_type, year, state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/Home/party-type-count", response_model=PartyCount)
def get_party_counts(elect_type: str, year: int, state: str = None, db: Session = Depends(get_db)):
    try:
        return crud.get_national_regional_party_count(db, elect_type, year, state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/Home/party-cards", response_model=list[PartyCard])
def get_party_cards(db: Session = Depends(get_db)):
    try:
        return crud.get_party_cards_with_seats(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)
