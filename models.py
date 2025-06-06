from sqlalchemy import Column, Integer, String, Float
from database import Base

class ConstituencyAnalytics(Base):
    __tablename__ = "constituency_analytics"

    id = Column(Integer, primary_key=True, index=True)
    percentage = Column(Float)
    election_year = Column(Integer)
    winning_margin = Column(Float)
    winning_margin_votes = Column(Integer)
    election_type = Column(String)
    winners = Column(String)
    second_position = Column(String)
    third_position = Column(String)
    fourth_position = Column(String)
    constituency = Column(String)
    state = Column(String)
    partywin = Column(String)
