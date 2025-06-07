from sqlalchemy.future import select
from sqlalchemy import func, desc
from models import ConstituencyAnalytics

async def get_margin_chart(session, year: int, election_type: str):
    result = await session.execute(
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

async def get_turnout_chart(session, year: int, election_type: str, state: str):
    result = await session.execute(
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


async def get_top_vs_constituencies(session, state: str):
    result = await session.execute(
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


async def get_party_distribution(session, state: str, year: int):
    result = await session.execute(
        select(
            ConstituencyAnalytics.partywin,
            func.count().label("seats")
        ).where(
            ConstituencyAnalytics.state == state,
            ConstituencyAnalytics.election_year == year
        ).group_by(ConstituencyAnalytics.partywin)
    )
    rows = result.all()
    return [
        {"party": row[0], "seats": row[1]}
        for row in rows
    ]

