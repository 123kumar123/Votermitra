from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session
from models import ConstituencyAnalytics
from typing import Optional
from sqlalchemy import text

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
def get_lok_sabha_summary(db):
    query = """
        SELECT
            COUNT(DISTINCT constituency) AS total_constituencies,
            ROUND(AVG(percentage), 1) AS voter_turnout,
            COUNT(DISTINCT CASE WHEN party_status = 'National' THEN party_name END) AS national_parties,
            COUNT(DISTINCT CASE WHEN party_status = 'Regional' THEN party_name END) AS regional_parties
        FROM master m
        JOIN party_details p ON m.party = p.party_name
        WHERE m.year = 2024 AND m.electtype = 'Lok Sabha';
    """
    result = db.execute(text(query)).fetchone()
    return {
        "constituencies": result[0],
        "voter_turnout": result[1],
        "national_parties": result[2],
        "regional_parties": result[3]
    }

def get_seat_distribution(db):
    query = """
        SELECT party_name, seats_won
        FROM party_analytics_table_aggregate
        WHERE elct_type = 'Lok Sabha' AND elect_state = 'India';
    """
    results = db.execute(text(query)).fetchall()
    total = sum(row[1] for row in results)
    return [
        {
            "party": row[0],
            "seats": row[1],
            "percentage": round((row[1] / total) * 100, 1) if total else 0.0
        } for row in results
    ]

def get_vote_share(db):
    query = """
        SELECT party, SUM(votes) AS total_votes, SUM(electors) AS total_electors
        FROM master
        WHERE year = 2024 AND electtype = 'Lok Sabha'
        GROUP BY party;
    """
    results = db.execute(text(query)).fetchall()
    return [
        {
            "party": row[0],
            "vote_share": round((row[1] / row[2]) * 100, 1) if row[2] else 0.0
        } for row in results
    ]

def get_national_regional_parties(db):
    query = """
        SELECT party_name, year_found, party_pres, party_status
        FROM party_details
        WHERE party_status IN ('National', 'Regional');
    """
    results = db.execute(text(query)).fetchall()
    return [
        {
            "party": row[0],
            "year_founded": row[1],
            "president": row[2],
            "status": row[3]
        } for row in results
    ]

def get_vote_share_by_state(db: Session, state: str, year: int = 2024, election_type: str = "Lok Sabha"):
    query = text("""
        SELECT party, SUM(votes) AS total_votes, SUM(electors) AS total_electors
        FROM master
        WHERE year = :year AND electtype = :election_type AND statename = :state
        GROUP BY party;
    """)
    results = db.execute(query, {"year": year, "election_type": election_type, "state": state}).fetchall()
    return [
        {
            "party": row[0],
            "vote_share": round((row[1] / row[2]) * 100, 1) if row[2] else 0.0
        } for row in results
    ]
def get_national_regional_parties_with_seats(db):
    query = text("""
        SELECT 
            p.party_name,
            p.party_abbr,
            p.year_found,
            pa.seats_won
        FROM party_details p
        JOIN party_analytics_table_aggregate pa 
            ON p.party_name = pa.party_name
        WHERE 
            p.party_status IN ('National', 'Regional') AND
            pa.elct_type = 'Lok Sabha' AND 
            pa.elect_state = 'India'
    """)
    results = db.execute(query).fetchall()
    return [
        {
            "party": row[0],
            "abbreviation": row[1],
            "founded": row[2],
            "seats": row[3]
        } for row in results
    ]
def get_comparative_analysis(db):
    # Query seat data
    seat_query = """
        SELECT party_name, elect_year, seats_won 
        FROM party_analytics_table_aggregate
        WHERE elect_state = 'India' AND elct_type = 'Lok Sabha' AND party_name IN ('BJP', 'Indian National Congress')
    """
    seat_data = db.execute(text(seat_query)).fetchall()

    seat_map = {"BJP": {}, "Congress": {}}
    for row in seat_data:
        party = "BJP" if row[0] == "BJP" else "Congress"
        seat_map[party][row[1]] = row[2]

    # Query vote share
    vote_query = """
        SELECT party_name, elect_year, vote_share 
        FROM party_analytics_table_aggregate
        WHERE elect_state = 'India' AND elct_type = 'Lok Sabha' AND party_name = 'BJP'
    """
    vote_data = db.execute(text(vote_query)).fetchall()
    vote_share = {row[1]: row[2] for row in vote_data}

    # Query turnout
    turnout_query = """
        SELECT elect_year, turnout_percentage 
        FROM electsumsummary
        WHERE elect_state = 'India' AND elect_type = 'Lok Sabha'
    """
    turnout_data = db.execute(text(turnout_query)).fetchall()
    turnout = {row[0]: row[1] for row in turnout_data}

    # Repetitive candidates
    repeat_query = """
        SELECT party_name, COUNT(*) 
        FROM candidate_analytics_table
        WHERE repeated_in_both = 1 AND elct_type = 'Lok Sabha'
        GROUP BY party_name
    """
    repeat_data = db.execute(text(repeat_query)).fetchall()

    # Others bucket
    major_parties = {"BJP", "Congress", "TMC", "DMK"}
    repetitive = []
    others_count = 0
    for party, count in repeat_data:
        name = party
        if name in ["BJP", "Indian National Congress"]:
            name = "BJP" if name == "BJP" else "Congress"
        elif name not in major_parties:
            others_count += count
            continue
        repetitive.append({"party": name, "count": count})
    repetitive.append({"party": "Others", "count": others_count})

    return {
        "bjp_seats": {
            "current": seat_map["BJP"].get(2024, 0),
            "previous": seat_map["BJP"].get(2019, 0),
            "diff": seat_map["BJP"].get(2024, 0) - seat_map["BJP"].get(2019, 0)
        },
        "congress_seats": {
            "current": seat_map["Congress"].get(2024, 0),
            "previous": seat_map["Congress"].get(2019, 0),
            "diff": seat_map["Congress"].get(2024, 0) - seat_map["Congress"].get(2019, 0)
        },
        "bjp_vote_share": {
            "current": vote_share.get(2024, 0.0),
            "previous": vote_share.get(2019, 0.0),
            "diff": round(vote_share.get(2024, 0.0) - vote_share.get(2019, 0.0), 2)
        },
        "voter_turnout": {
            "current": turnout.get(2024, 0.0),
            "previous": turnout.get(2019, 0.0),
            "diff": round(turnout.get(2024, 0.0) - turnout.get(2019, 0.0), 2)
        },
        "repetitive_candidates": repetitive
    }
def get_seat_distribution_comparison(db):
    query = """
        SELECT party_name, elect_year, seats_won
        FROM party_analytics_table_aggregate
        WHERE elect_state = 'India' AND elct_type = 'Lok Sabha'
        AND party_name IN ('BJP', 'Indian National Congress', 'DMK', 'TMC', 'YSRCP')
    """
    result = db.execute(text(query)).fetchall()

    # Organize by party
    data = {}
    for row in result:
        party_raw = row[0]
        year = row[1]
        seats = row[2]

        party = "INC" if party_raw == "Indian National Congress" else party_raw
        if party not in data:
            data[party] = {"seats_2019": 0, "seats_2024": 0}

        if year == 2019:
            data[party]["seats_2019"] = seats
        elif year == 2024:
            data[party]["seats_2024"] = seats

    # Convert to list
    response = [{"party": k, **v} for k, v in data.items()]
    return response

