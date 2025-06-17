from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session
from models import ConstituencyAnalytics
from typing import Optional
from sqlalchemy import text

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
