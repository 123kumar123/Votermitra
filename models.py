from sqlalchemy import Column, Integer, String, Float,Text
from database import Base
from sqlalchemy.ext.declarative import declarative_base

class ConstituencyAnalytics(Base):
    __tablename__ = "constituency_analytics"

    id = Column(Integer, primary_key=True, index=True)
    election_year = Column(Integer, nullable=False)
    election_type = Column(String(50), nullable=False)
    state = Column(String(100), nullable=False)
    constituency = Column(String(100), nullable=False)

    percentage = Column(Float)
    winning_margin = Column(Float)
    winning_margin_votes = Column(Integer)

    winners = Column(String(100))
    second_position = Column(String(100))
    third_position = Column(String(100))
    fourth_position = Column(String(100))
    partywin = Column(String(100))


class MasterTable(Base):
    __tablename__ = "master_table"

    id = Column(Integer, primary_key=True, index=True)
    electors = Column(Integer)
    votes = Column(Integer)
    percentage = Column(Float)
    year = Column(Integer)
    rank = Column(Integer)
    age = Column(Integer)
    general = Column(Integer)
    postal = Column(Integer)
    total = Column(Integer)
    deplost = Column(Integer)
    constituency = Column(String(255))
    curr_election = Column(String(255))
    statename = Column(String(255))
    candidate = Column(String(255))
    party = Column(String(255))
    symbol = Column(String(255))
    sex = Column(String(10))
    result = Column(String(50))
    electtype = Column(String(50))
    category = Column(String(50))


class PartyDetails(Base):
    __tablename__ = "party_details"

    id = Column(Integer, primary_key=True, index=True)
    year_found = Column(Integer)
    party_pres = Column(String(255))
    party_status = Column(String(50))
    party_name = Column(String(255))
    party_founder = Column(String(255))
    party_symbol = Column(String(255))
    manifesto = Column(Text)


class PartyAnalyticsAggregate(Base):
    __tablename__ = "party_analytics_aggregate"

    id = Column(Integer, primary_key=True, index=True)
    seats_con = Column(Integer)
    seats_won = Column(Integer)
    seats_los = Column(Integer)
    dep_lost_count = Column(Integer)
    elct_type = Column(String(50))
    elect_state = Column(String(255))
    party_name = Column(String(255))
    party_symbol = Column(String(255))
    party_pres = Column(String(255))
    party_status = Column(String(50))


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    constituency = Column(String(255))
    party = Column(String(255))
    image_url = Column(String(255))
    contested = Column(Integer)
    won = Column(Integer)
    win_loss_ratio = Column(Integer)
    election_year = Column(String(4)) 