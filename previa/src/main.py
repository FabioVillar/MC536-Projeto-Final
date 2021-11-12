import sys
from requests.api import get
from models import *
sys.path.insert(0, '/previa/src/webscraping/')
from webscraping import cup
from webscraping import matches
from webscraping import awards
import json


def get_awards_by_year(awards_list, year):
    awards_list_year = []
    for awards in awards_list:
        for award in awards:
            if award.year == year:
                awards_list_year.append(award)
    return awards_list_year

def get_world_cups():

    start_year = 1991
    final_year = 1991
    page_id = 1779
    cup_list=[]
    awards_list = awards.create_awards()
    while (start_year<=final_year):
        new_cup = cup.create_new_cup(start_year, page_id)
        new_cup.awards = get_awards_by_year(awards_list, start_year)
        cup_list.append(new_cup)
        with open(f'webscraping/teste{start_year}.json', 'w+', encoding="utf-8") as f:
            json.dump(
                new_cup.dict(exclude_none=True),
                f,
                ensure_ascii=False,
                indent=2
            )
        start_year += 4
        page_id += 1
    
    return cup_list

get_world_cups()

    