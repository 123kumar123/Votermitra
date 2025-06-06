from pydantic import BaseModel

class ConstituencyData(BaseModel):
    constituency: str
    winners: str
    partywin: str
    winning_margin: float

class MarginChart(BaseModel):
    constituency: str
    winning_margin: float

class TurnoutChart(BaseModel):
    constituency: str
    percentage: float

class PartyDistribution(BaseModel):
    party: str
    seats: int
