from pydantic import BaseModel

class ConstituencyData(BaseModel):
    constituency: str
    winners: str
    partywin: str
    winning_margin: float

    class Config:
        orm_mode = True

class MarginChart(BaseModel):
    constituency: str
    winning_margin: float

    class Config:
        orm_mode = True

class TurnoutChart(BaseModel):
    constituency: str
    percentage: float

    class Config:
        orm_mode = True

class PartyDistribution(BaseModel):
    party: str
    seats: int

    class Config:
        orm_mode = True
