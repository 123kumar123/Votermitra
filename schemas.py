from pydantic import BaseModel
from typing import Optional
from typing import List

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

class SummaryData(BaseModel):
    constituencies: int
    voter_turnout: float
    national_parties: int
    regional_parties: int

class SeatDistribution(BaseModel):
    party: str
    seats: int
    percentage: float

class VoteShare(BaseModel):
    party: str
    vote_share: float

class PartyInfo(BaseModel):
    party: str
    year_founded: int
    president: str
    status: str

class PartyInfo(BaseModel):
    party: str             # Full party name (e.g., "Bharatiya Janata Party")
    abbreviation: str      # Short name (e.g., "BJP")
    founded: int           # Year founded
    seats: int
    logo_url: str              # Number of Lok Sabha seats

    class Config:
        orm_mode = True

class SeatChange(BaseModel):
    current: int
    previous: int
    diff: int

class VoteShareChange(BaseModel):
    current: float
    previous: float
    diff: float

class TurnoutChange(BaseModel):
    current: float
    previous: float
    diff: float

class RepetitiveCandidate(BaseModel):
    party: str
    count: int

class ComparativeAnalysis(BaseModel):
    bjp_seats: SeatChange
    congress_seats: SeatChange
    bjp_vote_share: VoteShareChange
    voter_turnout: TurnoutChange
    repetitive_candidates: List[RepetitiveCandidate]

class CandidateSchema(BaseModel):
    name: str
    constituency: str
    party: str
    image_url: str
    contested: int
    won: int
    win_loss_ratio: int

    class Config:
        orm_mode = True

