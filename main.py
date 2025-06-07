from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import SessionLocal
import crud
from schemas import MarginChart, TurnoutChart, ConstituencyData, PartyDistribution

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://votermitra.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency for database session
async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

@app.get("/")
def read_root():
    return {"message": "VoterMitra API is running."}

@app.get("/margin-comparison", response_model=List[MarginChart])
async def margin_chart(year: int, election_type: str, session: AsyncSession = Depends(get_session)):
    return await crud.get_margin_chart(session, year, election_type)

@app.get("/voter-turnout", response_model=List[TurnoutChart])
async def turnout_chart(year: int, election_type: str, state: str, session: AsyncSession = Depends(get_session)):
    return await crud.get_turnout_chart(session, year, election_type, state)

@app.get("/top-vs", response_model=List[ConstituencyData])
async def top_vs(state: str, session: AsyncSession = Depends(get_session)):
    return await crud.get_top_vs_constituencies(session, state)

@app.get("/party-distribution", response_model=List[PartyDistribution])
async def party_distribution(state: str, year: int, session: AsyncSession = Depends(get_session)):
    return await crud.get_party_distribution(session, state, year)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)
