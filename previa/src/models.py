from pydantic import BaseModel
from typing import List

class Player(BaseModel):
    name: str = '' 
    position: str = '' 
    age: int = 0 
    goals: int = 0 
    assists: int = 0 
    yellow_cards: int = 0 
    red_cards: int = 0 


class Team(BaseModel):
    name: str = '' 
    coach: str ='' 
    points_group_stage: int = 0
    group: str = '' 
    position_group: int
    goals: List[int] = [] 
    ved: List[int] = [] 
    players: List[Player] = [] 
    year: int = 0 


class Event(BaseModel):
    event: str = ''
    time: int
    team: Team
    player: Player


class Award(BaseModel):
    award: str = ''
    team: Team
    winner: Player


class Match(BaseModel):
    phase: str = '' 
    group: str = '' 
    teams: List[Team] = [] 
    score: List[int] = []
    stadium: str = '' 
    attendance: int = 0 
    referee: str = '' 
    penalties: List[int] = []
    formations: List[str] = []
    initial_squads: List[List[Player]] = []
    bench_players: List[List[Player]] = []
    events: List[Event] = []


class WorldCup(BaseModel):
    year: int = 0 
    host: str = ''
    winner: str
    awards: List[Award] = []
    teams: List[Team] = [] 
    matches: List[Match] = []