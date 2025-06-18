from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session
from models import ConstituencyAnalytics
from typing import Optional
from sqlalchemy import text
from models import MasterTable
from sqlalchemy import distinct
from models import CandidateAnalytics
from models import VSRulingParty
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import PartyAnalyticsAggregate, PartyDetails


def get_party_seat_distribution(db: Session, elect_type: str, year: int, state: str = None):
    try:
        query = db.query(
            PartyAnalyticsAggregate.party_name,
            func.sum(PartyAnalyticsAggregate.seats_won).label("seats")
        ).filter(
            PartyAnalyticsAggregate.elct_type == elect_type,
            PartyAnalyticsAggregate.elect_year == year
        )

        if state:
            query = query.filter(PartyAnalyticsAggregate.elect_state == state)

        query = query.group_by(PartyAnalyticsAggregate.party_name)
        return [{"party_name": r.party_name, "seats": r.seats} for r in query.all()]
    except Exception as e:
        raise e


def get_party_vote_share(db: Session, elect_type: str, year: int, state: str = None):
    try:
        query = db.query(
            PartyAnalyticsAggregate.party_name,
            func.sum(PartyAnalyticsAggregate.votes).label("total_votes")
        ).filter(
            PartyAnalyticsAggregate.elct_type == elect_type,
            PartyAnalyticsAggregate.elect_year == year
        )

        if state:
            query = query.filter(PartyAnalyticsAggregate.elect_state == state)

        results = query.group_by(PartyAnalyticsAggregate.party_name).all()
        total_votes = sum(r.total_votes for r in results)

        vote_share_data = []
        for r in results:
            percentage = (r.total_votes / total_votes) * 100 if total_votes else 0
            vote_share_data.append({
                "party_name": r.party_name,
                "vote_share_percentage": round(percentage, 2)
            })
        return vote_share_data
    except Exception as e:
        raise e


def get_national_regional_party_count(db: Session, elect_type: str, year: int, state: str = None):
    try:
        query = db.query(
            PartyAnalyticsAggregate.party_status,
            func.count(func.distinct(PartyAnalyticsAggregate.party_name)).label("count")
        ).filter(
            PartyAnalyticsAggregate.elct_type == elect_type,
            PartyAnalyticsAggregate.elect_year == year
        )

        if state:
            query = query.filter(PartyAnalyticsAggregate.elect_state == state)

        query = query.group_by(PartyAnalyticsAggregate.party_status)
        results = query.all()

        counts = {"national": 0, "regional": 0}
        for r in results:
            status = (r.party_status or "").lower()
            if "national" in status:
                counts["national"] += r.count
            elif "regional" in status:
                counts["regional"] += r.count
        return counts
    except Exception as e:
        raise e


def get_party_cards_with_seats(db: Session):
    try:
        latest_year = db.query(func.max(PartyAnalyticsAggregate.elect_year)).filter(
            PartyAnalyticsAggregate.elct_type == "Lok Sabha"
        ).scalar()

        seats_subquery = db.query(
            PartyAnalyticsAggregate.party_name,
            func.sum(PartyAnalyticsAggregate.seats_won).label("seats_lok_sabha")
        ).filter(
            PartyAnalyticsAggregate.elct_type == "Lok Sabha",
            PartyAnalyticsAggregate.elect_year == latest_year
        ).group_by(PartyAnalyticsAggregate.party_name).subquery()

        result = db.query(
            PartyDetails.party_name,
            PartyDetails.year_found,
            PartyDetails.party_symbol,
            func.coalesce(seats_subquery.c.seats_lok_sabha, 0).label("seats_lok_sabha")
        ).outerjoin(
            seats_subquery, PartyDetails.party_name == seats_subquery.c.party_name
        ).all()

        return [
            {
                "party_name": r.party_name,
                "year_found": r.year_found,
                "party_symbol": r.party_symbol,
                "seats_lok_sabha": r.seats_lok_sabha
            }
            for r in result
        ]
    except Exception as e:
        raise e

def get_all_states(db: Session):
    try:
        return db.query(distinct(MasterTable.state)).all()
    except Exception as e:
        raise Exception(f"Error fetching states: {str(e)}")

def get_all_years(db: Session):
    try:
        return db.query(distinct(MasterTable.year)).order_by(MasterTable.year.desc()).all()
    except Exception as e:
        raise Exception(f"Error fetching years: {str(e)}")

def get_all_election_types(db: Session):
    try:
        return db.query(distinct(MasterTable.election_type)).all()
    except Exception as e:
        raise Exception(f"Error fetching election types: {str(e)}")
    


def get_top_candidates(db: Session, year: int, house_type: str, limit: int = 5):
    return (
        db.query(CandidateAnalytics)
        .filter(CandidateAnalytics.year == year, CandidateAnalytics.house_type == house_type)
        .order_by(CandidateAnalytics.win_loss_ratio.desc())
        .limit(limit)
        .all()
    )
def get_top_candidates(db: Session, state: str, year: int, house_type: str):
    return db.execute(
        """
        SELECT 
            candidate_name,
            party_name,
            constituency,
            state,
            total_votes,
            victory_margin,
            vote_percentage
        FROM candidate_analytics
        WHERE state = :state
          AND election_year = :year
          AND house_type = :house_type
        ORDER BY vote_percentage DESC
        LIMIT 5;
        """,
        {"state": state, "year": year, "house_type": house_type}
    ).fetchall()

def get_all_vs_ruling_parties(db: Session):
    return db.query(VSRulingParty).all()

