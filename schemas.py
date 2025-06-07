from pydantic import BaseModel
from typing import Optional

# Schema for Top VS Constituency data
class ConstituencyData(BaseModel):
    constituency: str
    winners: str
    partywin: str
    winning_margin: float

    class Config:
        orm_mode = True

# Schema for Margin Comparison Chart
class MarginChart(BaseModel):
    constituency: str
    winning_margin: float

    class Config:
        orm_mode = True

# Schema for Voter Turnout Chart
class TurnoutChart(BaseModel):
    constituency: str
    percentage: float

    class Config:
        orm_mode = True

class PartyDistribution(BaseModel):
    party: Optional[str]  # <- change from `str` to `Optional[str]`
    votes: int

    class Config:
        orm_mode = True
