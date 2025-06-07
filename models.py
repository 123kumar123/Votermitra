from sqlalchemy import Column, Integer, String, Float
from database import Base

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
