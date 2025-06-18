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

class PartyCount(BaseModel):
    party: str
    count: int

class ComparativeAnalysis(BaseModel):
    bjp_seats: SeatChange
    congress_seats: SeatChange
    bjp_vote_share: VoteShareChange
    voter_turnout: TurnoutChange
    repetitive_candidates: List[PartyCount]

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

class PartyCard(BaseModel):
    party: str
    seats: int
    color: str
class PartyShare(BaseModel):
    party_name: str
    seats_won: int
    seats_contested: int
    percentage: float  # Or whatever fields are relevant

    class Config:
        orm_mode = True


class CandidateOut(BaseModel):
    name: str
    constituency: str
    party: str
    elections_contested: int
    elections_won: int
    win_loss_ratio: float

    class Config:
        orm_mode = True
class CandidateOut(BaseModel):
    candidate_name: str
    party_name: str
    constituency: str
    state: str
    total_votes: int
    victory_margin: int
    vote_percentage: float

    class Config:
        orm_mode = True

class PartySeatShare(BaseModel):
    party: str
    seats: float  # or int

class PartyVoteShare(BaseModel):
    party: str
    vote_share: float

class LokSabhaSummaryOut(BaseModel):
    total_constituencies: int
    voter_turnout: float
    leading_party: str
    government: str
    seat_distribution: List[PartySeatShare]
    vote_share_distribution: List[PartyVoteShare]

class SummaryStats(BaseModel):
    constituencies: int
    voter_turnout: float
    leading_party: str
    government: str

class PartySeatShare(BaseModel):
    party: str
    seats: int
    percentage: float

class PartyVoteShare(BaseModel):
    party: str
    vote_share: float

class YearlyData(BaseModel):
    year: int
    bjp: float
    congress: float
    others: float

class PartyPerformancePoint(BaseModel):
    year: int
    bjp: float
    congress: float
    others: float

class AgeDistributionPoint(BaseModel):
    age_group: str
    count: int

class NewPartiesIndependentsPoint(BaseModel):
    year: int
    new_parties: int
    independents: int

class VSRulingPartyOut(BaseModel):
    state: str
    cm_name: str
    party_in_power: str
    last_election_year: int
    next_poll_year: int
    total_seats: int

    class Config:
        orm_mode = True
