import bs4
from bs4 import BeautifulSoup
import requests
from models import *
import re
from unidecode import unidecode

def fix_name(name):
    if name == 'Victoria Svensson':
        return 'Victoria Sandell Svensson'
    else:
        return name


def get_regex_single_winners(tags):
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



def get_individual_award(award_, tags):
    award_list = []
    candidates = get_regex_single_winners(tags)
    i = 0
    while i < len(candidates)-1:
        if re.match(r'\d+\s\w+',candidates[i]):
            infos = candidates[i].split()
            if len(infos) > 2:
                year = infos[0]
                infos.pop(0)
                host = ' '.join(infos)
            else:
                year, host = candidates[i].split()
            i+=1
        else:
            j = i 
            while j < len(candidates) and not bool(re.match(r'\d+\s\w+',candidates[j])):
                award_obj = Award(
                        award = award_,
                        year = int(year),
                        team = candidates[i],
                        player = fix_name(unidecode(str(candidates[i+1])))
                    )
                award_list.append(award_obj)
                j+=2
            i = j
    return award_list
    
    


def get_multiple_award(award_, tags):
    award_list = []
    candidates = get_regex_single_winners(tags)
    
    i = 0
    while i < len(candidates) - 3:
        if re.match(r'\d+\s\w+',candidates[i]):
            infos = candidates[i].split()
            if len(infos) > 2:
                year = infos[0]
                infos.pop(0)
                host = ' '.join(infos)
            else:
                year, host = candidates[i].split()
            i+=1
        else:
            j = i
            position = 1
            while j < len(candidates) and not bool(re.match(r'\d+\s\w+',candidates[j])):
                award_obj = Award(
                    award = award_+' '+str(position),
                    year = int(year),
                    team = candidates[j],
                    player = fix_name(unidecode(str(candidates[j+1])))
                )
                position +=1
                award_list.append(award_obj)
                j+=2
            i = j
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
    func_list = [get_multiple_award, get_multiple_award, get_individual_award, get_individual_award]
    awards_list = [
        func_list[i](possible_awards[i], tags[i]) for i in range(len(tags))
    ]
    return awards_list

def get_awards_by_year(awards_list, year):
    awards_list_year = []
    for awards in awards_list:
        for award in awards:
            if award.year == year:
                awards_list_year.append(award)
    return awards_list_year

create_awards()