import bs4
from bs4 import BeautifulSoup
import requests
from models import *
import re

def get_regex_single_winners(tags):
    tags_re = []

    for i in range(len(tags)):
        for p in tags[i]:
            if isinstance(p, bs4.element.NavigableString):
                tags_re.append(p)
    return tags_re


def get_regex_multiple_winners(tags):
    tags_re = []
    for i in range(len(tags)):
        for p in tags[i]:
            if isinstance(p, bs4.element.NavigableString):
                tags_re.append(p)
            else:
                string = str(p)
                regex = r"\"(.*?)\""
                substring = re.search(regex,string)
                if substring:
                    tags_re.append(substring.group(1))
    return tags_re


def get_young_player_award(award_, tags):
    award_list = []
    candidates = get_regex_single_winners(tags)
    for i in range(0,len(candidates)-1,2):
        year, team = candidates[i].split()
        award_obj = Award(
            award = award_,
            year = int(year),
            team = team,
            winner = candidates[i+1]
        )
        award_list.append(award_obj)

    return award_list



def get_golden_glove(award_, tags):
    award_list = []
    candidates = get_regex_single_winners(tags)
    aux = candidates[0]
    candidates[0] = candidates[1]
    candidates[1] = aux
    for i in range(0,len(candidates)-1,2):
        infos = candidates[i+1].split()
        if len(infos) > 2:
            year = infos[0]
            infos.pop(0)
            team = ' '.join(infos)
        else:
            year, team = candidates[i+1].split()
        award_obj = Award(
            award = award_,
            year = int(year),
            team = str(team),
            winner = str(candidates[i])
        )
        award_list.append(award_obj)

    return award_list
    


def get_multiple_award(award_, tags):
    award_list = []
    candidates = get_regex_multiple_winners(tags)
    for i in range(len(candidates)-1):
        if re.match(r'\d+\s\w+',candidates[i]):
            infos = candidates[i].split()
            if len(infos) > 2:
                year = infos[0]
                infos.pop(0)
                host = ' '.join(infos)
            else:
                year, host = candidates[i].split()
        else:
            award_obj = Award(
                award = award_,
                year = int(year),
                team = candidates[i],
                winner = str(candidates[i+1])
            )
            award_list.append(award_obj)
    
    return award_list
    


def create_awards():

    awards = requests.get(
        "https://en.wikipedia.org/wiki/FIFA_Women's_World_Cup_awards").text
    soup = BeautifulSoup(awards, 'html.parser')  # parsing
    awards_headers = soup.find_all('h2')
    lista_tags = []
    possible_awards = []
    for award in awards_headers:
        lista_tags.append(award.find_all('span', {'class': 'mw-headline'}))
    for a in lista_tags:
        for tag in a:
            possible_awards.append(tag['id'])
    possible_awards = possible_awards[1:5]
    tables = soup.find_all('table', {'class': 'wikitable'})
    tags = [
        table.find_all('a') for table in tables
    ]
    tags = tags[:len(possible_awards)]
    func_list = [get_multiple_award, get_multiple_award, get_golden_glove, get_young_player_award]
    awards_list = [
        func_list[i](possible_awards[i], tags[i]) for i in range(len(tags))
    ]
    return awards_list
