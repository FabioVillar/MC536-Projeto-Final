from pydantic import BaseModel
from typing import List

class Player(BaseModel):
    name: str = ''
    position: str = ''
    age: int = 0
    goals_scored: int = 0
    assists: int = 0
    yellow_cards: int = 0
    red_cards: int = 0


class Award(BaseModel):
    award: str = ''
    winner: List[Player] = []


class Stage(BaseModel):
    type: str = ''


class Team(BaseModel):
    name: str = ''
    number_of_players: int = 0
    coach: str =''
    points_group_stage: int = 0
    points_overall: int = 0
    goals: List[int] = []
    ved: List[int] = []
    players: List[Player] = []

class Event(BaseModel):
    event: str = ''
    time: Team
    player: str = ''


class Match(BaseModel):
    stage: Stage
    teams: List[Team] = []
    score: List[int] = []
    stadium: str = ''
    total_audience: int = 0
    referee: str = ''
    formations: List[str] = []
    initial_squads: List[List[Player]] = []
    bench_players: List[List[Player]] = []
    events: List[Event] = []


class Group(BaseModel):
    id: str = ''
    number_of_teams: int = 0
    placements: List[Team]


class WorldCup(BaseModel):
    phases: List[Stage] = []
    awards: List[Award] = []
    year: int = 0
    host: str = ''
    number_of_teams: int = 0
    teams: List[Team] = []