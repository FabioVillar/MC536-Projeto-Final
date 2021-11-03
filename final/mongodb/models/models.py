from pydantic import BaseModel
from typing import List, Optional


class Player(BaseModel):
    name: str
    position: str
    number: str
    age: str
    goals_scored: int = 0
    yellow_cards: int = 0
    red_cards: int = 0


class Award(BaseModel):
    award: str
    winner: List[Player] = []


class Stage(BaseModel):
    type: str


class Team(BaseModel):
    name: str
    number_of_players: str
    coach: str
    points_group_stage: str
    goals: List[int] = []
    vtd: List[int] = []


class Event(BaseModel):
    event: str
    time: int
    players_involved: Optional(List[Player]) = []


class Match(BaseModel):
    stage: Stage
    teams: List[Team] = []
    score: List[int] = []
    stadium: Optional(str)
    total_audience: Optional(float)
    referee: Optional(str)
    formations: List[str] = []
    initial_squads: List[List[Player]] = []
    bench_players: List[List[Player]] = []
    events: List[Event] = []


class Group(BaseModel):
    id: str
    number_of_teams: str
    placements: List[Team]


class WorldCup(BaseModel):
    phases: List[Stage] = []
    awards: List[Award] = []
    year: int
    host: str
    number_of_teams: int
    teams: List[Team] = []
    placing: List[Team] = []
