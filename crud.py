from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session
from models import ConstituencyAnalytics
from typing import Optional

def get_margin_chart(session: Session, year: int, election_type: str):
    result = session.execute(
        select(
            ConstituencyAnalytics.constituency,
            ConstituencyAnalytics.winning_margin
        ).where(
            ConstituencyAnalytics.election_year == year,
            ConstituencyAnalytics.election_type == election_type
        ).order_by(desc(ConstituencyAnalytics.winning_margin)).limit(5)
    )
    rows = result.all()
    return [
        {"constituency": row[0], "winning_margin": row[1]}
        for row in rows
    ]

def get_turnout_chart(session: Session, year: int, election_type: str, state: str):
    result = session.execute(
        select(
            ConstituencyAnalytics.constituency,
            ConstituencyAnalytics.percentage
        ).where(
            ConstituencyAnalytics.election_year == year,
            ConstituencyAnalytics.election_type == election_type,
            ConstituencyAnalytics.state == state
        ).order_by(desc(ConstituencyAnalytics.percentage)).limit(5)
    )
    rows = result.all()
    return [
        {"constituency": row[0], "percentage": row[1]}
        for row in rows
    ]

def get_top_vs_constituencies(session: Session, state: str):
    result = session.execute(
        select(
            ConstituencyAnalytics.constituency,
            ConstituencyAnalytics.winners,
            ConstituencyAnalytics.partywin,
            ConstituencyAnalytics.winning_margin
        ).where(
            ConstituencyAnalytics.state == state,
            ConstituencyAnalytics.election_type.ilike("Vidhan Sabha")
        ).order_by(desc(ConstituencyAnalytics.winning_margin)).limit(3)
    )
    rows = result.all()
    return [
        {
            "constituency": row[0],
            "winners": row[1],
            "partywin": row[2],
            "winning_margin": row[3]
        }
        for row in rows
    ]

def get_party_distribution(session: Session, state: str, year: int):
    stmt = (
        select(
            ConstituencyAnalytics.party,
            func.sum(ConstituencyAnalytics.votes).label("votes")
        ).where(
            ConstituencyAnalytics.state == state,
            ConstituencyAnalytics.election_year == year
        ).group_by(ConstituencyAnalytics.party)
    )
    results = session.execute(stmt).all()

    cleaned = []
    for row in results:
        party = row[0] if row[0] is not None else "Unknown"
        cleaned.append({
            "party": party,
            "votes": row[1]
        })

    return cleaned
