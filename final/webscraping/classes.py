from pydantic import BaseModel
from typing import List

class Player(BaseModel):
    name: str = '' #done
    position: str = '' #done
    age: int = 0 #done
    goals: int = 0 #done
    assists: int = 0 #done
    yellow_cards: int = 0 #done
    red_cards: int = 0 #done


class Team(BaseModel):
    name: str = '' #done
    coach: str ='' #done
    points_group_stage: int = 0
    group: str = ''
    points_overall: int = 0
    goals: List[int] = []
    ved: List[int] = []
    players: List[Player] = [] #done
    year: int = 0 #done


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
    total_audience: int = 0
    referee: str = ''
    penalties: List[int] = []
    formations: List[str] = []
    initial_squads: List[List[Player]] = []
    bench_players: List[List[Player]] = []
    events: List[Event] = []


class WorldCup(BaseModel):
    year: int = 0 #done
    host: str = '' #done
    awards: List[Award] = []
    teams: List[Team] = [] #done
    matches: List[Match] = []