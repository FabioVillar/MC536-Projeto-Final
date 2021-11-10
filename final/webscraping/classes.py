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
    group: str = '' #done
    points_overall: int = 0 #done
    goals: List[int] = [] #done
    ved: List[int] = [] #done
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
    phase: str = '' #done
    group: str = '' 
    teams: List[Team] = [] #done
    score: List[int] = [] #done
    stadium: str = '' #done
    attendance: int = 0 #done
    referee: str = '' #done
    penalties: List[int] = []
    formations: List[str] = [] #done
    initial_squads: List[List[Player]] = [] #almost done
    bench_players: List[List[Player]] = [] #almost done
    events: List[Event] = []


class WorldCup(BaseModel):
    year: int = 0 #done
    host: str = '' #done
    awards: List[Award] = []
    teams: List[Team] = [] #done
    matches: List[Match] = []