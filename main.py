from fastapi import FastAPI, Depends, HTTPException,Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import schemas
from sqlalchemy.exc import SQLAlchemyError 


from database import SessionLocal
import crud
from schemas import MarginChart, TurnoutChart, ConstituencyData, PartyDistribution
from schemas import SummaryData, SeatDistribution, VoteShare, PartyInfo
from schemas import (
    SummaryStats,
    PartySeatShare,
    PartyVoteShare,
    YearlyData,
    PartyPerformancePoint,
    AgeDistributionPoint,
    NewPartiesIndependentsPoint
)

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

@app.get("/Constituency/margin-comparison")
def get_margin_comparison(year: int, election_type: str, db: Session = Depends(get_db)):
    try:
        return crud.get_top_margin_constituencies(db, year, election_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/constituency/party-seat-distribution", response_model=list[schemas.PartyShare])
def seat_distribution(elect_type: str, year: int, state: str = None, db: Session = Depends(get_db)):
    try:
        return crud.get_party_seat_distribution(db, elect_type, year, state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/constituency/voter-turnout-comparison")
def voter_turnout(state: str, year: int, election_type: str, db: Session = Depends(get_db)):
    try:
        return crud.get_top_voter_turnout_constituencies(db, state, year, election_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/constituency/party-vote-share", response_model=list[schemas.PartyShare])
def vote_share(elect_type: str, year: int, state: str = None, db: Session = Depends(get_db)):
    try:
        return crud.get_party_vote_share(db, elect_type, year, state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/candidates/top-candidates", response_model=List[schemas.CandidateOut])
def top_candidates(
    year: int = Query(..., description="Election Year"),
    house_type: str = Query(..., description="Lok Sabha or Vidhan Sabha"),
    db: Session = Depends(get_db)
):
    try:
        candidates = crud.get_top_candidates(db=db, year=year, house_type=house_type)
        if not candidates:
            raise HTTPException(status_code=404, detail="No data found for given filters")
        return candidates
    except SQLAlchemyError as e:
        # Log e or print(e) if needed
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
@app.get("/candidates/top-candidates", response_model=List[schemas.CandidateOut])
def get_top_candidates(
    state: str = Query(..., description="State name, e.g., Bihar"),
    year: int = Query(..., description="Election Year, e.g., 2024"),
    house_type: str = Query(..., description="House type: Lok Sabha or Vidhan Sabha"),
    db: Session = Depends(get_db)
):
    try:
        candidates = crud.get_top_candidates(db=db, state=state, year=year, house_type=house_type)
        if not candidates:
            raise HTTPException(status_code=404, detail="No top candidates found for given filters")
        return candidates
    except SQLAlchemyError as e:
        print(f"DB error: {e}")  # Optional for logging
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    
@app.get("/elections/lok-sabha-2024/summary", response_model=schemas.LokSabhaSummaryOut)
def get_lok_sabha_2024_summary(
    year: int = Query(2024, description="Election Year"),
    house_type: str = Query("Lok Sabha", description="House type"),
    db: Session = Depends(get_db)
):
    try:
        summary = (
            db.query(models.LokSabhaSummary)
            .filter_by(year=year, house_type=house_type)
            .first()
        )

        if not summary:
            raise HTTPException(status_code=404, detail="Summary data not found for the given parameters")

        return summary

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
@app.get("/elections/summary", response_model=SummaryStats)
def get_summary(election_type: str, year: int, db: Session = Depends(get_db)):
    try:
        # Example query logic: Replace with your own DB query

        constituencies = db.execute(
            "SELECT COUNT(DISTINCT constituency) FROM master WHERE election_type = :etype AND year = :yr",
            {'etype': election_type, 'yr': year}).scalar()

        voter_turnout = db.execute(
            "SELECT AVG(percentage) FROM master WHERE election_type = :etype AND year = :yr",
            {'etype': election_type, 'yr': year}).scalar()

        leading_party = db.execute(
            "SELECT party FROM party_analytics WHERE elect_type = :etype AND elect_year = :yr ORDER BY seats_won DESC LIMIT 1",
            {'etype': election_type, 'yr': year}).scalar()

        government = "Coalition"  # or calculate based on your data logic

        return SummaryStats(
            constituencies=constituencies or 0,
            voter_turnout=round(voter_turnout or 0, 2),
            leading_party=leading_party or "N/A",
            government=government
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching summary: {str(e)}")


@app.get("/elections/party-seat-distribution", response_model=List[PartySeatShare])
def get_party_seat_distribution(election_type: str, year: int, db: Session = Depends(get_db)):
    try:
        # Example query: sum seats won per party
        result = db.execute(
            "SELECT party_name, SUM(seats_won) as seats FROM party_analytics "
            "WHERE elect_type = :etype AND elect_year = :yr GROUP BY party_name ORDER BY seats DESC",
            {'etype': election_type, 'yr': year}).fetchall()

        total_seats = sum(row['seats'] for row in result) or 1

        return [
            PartySeatShare(
                party=row['party_name'],
                seats=row['seats'],
                percentage=round(row['seats'] / total_seats * 100, 2)
            )
            for row in result
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching seat distribution: {str(e)}")


@app.get("/elections/party-vote-share", response_model=List[PartyVoteShare])
def get_party_vote_share(election_type: str, year: int, db: Session = Depends(get_db)):
    try:
        # Example query: vote share per party
        result = db.execute(
            "SELECT party_name, SUM(vote_share) as vote_share FROM party_vote_share_table "
            "WHERE election_type = :etype AND year = :yr GROUP BY party_name ORDER BY vote_share DESC",
            {'etype': election_type, 'yr': year}).fetchall()

        total_vote = sum(row['vote_share'] for row in result) or 1

        return [
            PartyVoteShare(
                party=row['party_name'],
                vote_share=round(row['vote_share'] / total_vote * 100, 2)
            )
            for row in result
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching vote share: {str(e)}")


@app.get("/elections/seat-share-across-years", response_model=List[YearlyData])
def seat_share_across_years(election_type: str, start_year: int = 1952, end_year: int = 2024, db: Session = Depends(get_db)):
    try:
        # Example: For each year, get seats won by BJP, Congress, Others
        data = []
        for year in range(start_year, end_year + 1):
            seats_data = db.execute(
                "SELECT party_name, SUM(seats_won) as seats FROM party_analytics "
                "WHERE elect_type = :etype AND elect_year = :yr GROUP BY party_name",
                {'etype': election_type, 'yr': year}).fetchall()
            bjp_seats = sum(row['seats'] for row in seats_data if row['party_name'].lower() == 'bjp')
            congress_seats = sum(row['seats'] for row in seats_data if row['party_name'].lower() == 'congress')
            others_seats = sum(row['seats'] for row in seats_data if row['party_name'].lower() not in ('bjp', 'congress'))
            data.append(YearlyData(year=year, bjp=bjp_seats, congress=congress_seats, others=others_seats))
        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching seat share across years: {str(e)}")


@app.get("/elections/vote-share-trends", response_model=List[YearlyData])
def vote_share_trends(election_type: str, start_year: int = 1984, end_year: int = 2024, db: Session = Depends(get_db)):
    try:
        data = []
        for year in range(start_year, end_year + 1):
            vote_data = db.execute(
                "SELECT party_name, SUM(vote_share) as vote_share FROM party_vote_share_table "
                "WHERE election_type = :etype AND year = :yr GROUP BY party_name",
                {'etype': election_type, 'yr': year}).fetchall()
            bjp_vote = sum(row['vote_share'] for row in vote_data if row['party_name'].lower() == 'bjp')
            congress_vote = sum(row['vote_share'] for row in vote_data if row['party_name'].lower() == 'congress')
            others_vote = sum(row['vote_share'] for row in vote_data if row['party_name'].lower() not in ('bjp', 'congress'))
            data.append(YearlyData(year=year, bjp=bjp_vote, congress=congress_vote, others=others_vote))
        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching vote share trends: {str(e)}")


@app.get("/elections/party-performance", response_model=List[PartyPerformancePoint])
def party_performance_over_years(election_type: str, start_year: int = 1952, end_year: int = 2024, metric: str = Query("seats_won", regex="^(seats_won|vote_share)$"), db: Session = Depends(get_db)):
    try:
        data = []
        for year in range(start_year, end_year + 1):
            if metric == "seats_won":
                q = "SELECT party_name, SUM(seats_won) as metric FROM party_analytics WHERE elect_type = :etype AND elect_year = :yr GROUP BY party_name"
            else:
                q = "SELECT party_name, SUM(vote_share) as metric FROM party_vote_share_table WHERE election_type = :etype AND year = :yr GROUP BY party_name"

            results = db.execute(q, {'etype': election_type, 'yr': year}).fetchall()
            bjp_metric = sum(r['metric'] for r in results if r['party_name'].lower() == 'bjp')
            congress_metric = sum(r['metric'] for r in results if r['party_name'].lower() == 'congress')
            others_metric = sum(r['metric'] for r in results if r['party_name'].lower() not in ('bjp', 'congress'))

            data.append(PartyPerformancePoint(year=year, bjp=bjp_metric, congress=congress_metric, others=others_metric))

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching party performance: {str(e)}")


@app.get("/elctions/age-distribution", response_model=List[AgeDistributionPoint])
def age_distribution(year: int, db: Session = Depends(get_db)):
    try:
        # Example age groups: 25-35, 36-45, 46-55, 56-65, 66+
        query = """
        SELECT
            CASE 
                WHEN age BETWEEN 25 AND 35 THEN '25-35'
                WHEN age BETWEEN 36 AND 45 THEN '36-45'
                WHEN age BETWEEN 46 AND 55 THEN '46-55'
                WHEN age BETWEEN 56 AND 65 THEN '56-65'
                ELSE '66+'
            END as age_group,
            COUNT(*) as count
        FROM master
        WHERE year = :yr
        GROUP BY age_group
        ORDER BY age_group
        """
        rows = db.execute(query, {'yr': year}).fetchall()
        return [AgeDistributionPoint(age_group=row['age_group'], count=row['count']) for row in rows]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching age distribution: {str(e)}")


@app.get("/elctions/rise-new-parties", response_model=List[NewPartiesIndependentsPoint])
def rise_of_new_parties(start_year: int = 2003, end_year: int = 2024, db: Session = Depends(get_db)):
    try:
        data = []
        for year in range(start_year, end_year + 1):
            # Query new parties count for year
            new_parties = db.execute(
                "SELECT COUNT(DISTINCT party_name) FROM party_analytics WHERE elect_year = :yr AND is_new_party = 1",
                {'yr': year}).scalar() or 0

            # Query independents count
            independents = db.execute(
                "SELECT COUNT(DISTINCT candidate) FROM master WHERE year = :yr AND party = 'Independent'",
                {'yr': year}).scalar() or 0

            data.append(NewPartiesIndependentsPoint(year=year, new_parties=new_parties, independents=independents))
        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching new parties rise data: {str(e)}")
    
@app.get("/elections/vs-ruling-parties", response_model=list[schemas.VSRulingPartyOut])
def read_vs_ruling_parties(db: Session = Depends(get_db)):
    try:
        return crud.get_all_vs_ruling_parties(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)
