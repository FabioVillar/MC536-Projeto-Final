import bs4
from bs4 import BeautifulSoup
import requests
from models import *
import re

def create_new_player(name, stats, year, team_name): 

    #assign stats elements to new_player attributes
    new_player = Player()
    new_player.name = name
    new_player.position = stats[0].text
    new_player.age = stats[1].text
    new_player.goals = stats[6].text
    new_player.assists = stats[7].text
    new_player.yellow_cards = stats[11].text
    new_player.red_cards = stats[12].text

    problem_count = 0

    if (new_player.position == '' or new_player.age == 0):
        problem_count = 1
        
    if (problem_count):
        print(new_player.name)
        wiki_link = f"https://en.wikipedia.org/wiki/{year}_FIFA_Women's_World_Cup_squads"
        wiki_page = requests.get(wiki_link).text #request
        soup = BeautifulSoup(wiki_page, 'lxml') #parsing
        content = soup.find('div', id='mw-content-text')
        count = 0
        for i in content.find_all('h3'):
            if (i.find('span').text == team_name):
                print("count = " + str(count))
                table = content.find_all('table')[count]
                body = table.find('tbody')
                meter = 0
                for k in body.find_all('tr'):
                    if (meter != 0):
                        if (name in k.find('th').find('a').text or name in  k.find('th').find('a')['href']):
                            stat = k.find_all('td')
                            if (new_player.position == ''):
                                new_player.position = stat[1].find('a').text
                                print(new_player.position)
                            if (new_player.age == 0):
                                string  = stat[2].find('span').text
                                age = [int(s) for s in string.split() if s.isdigit()]
                                new_player.age = age[0]
                                print(new_player.age)
                    else:
                        meter+=1
                break
            else:
                count += 1

    return new_player


def create_new_team(link, name, page_id, year):

    new_link = 'https://fbref.com'+link
    print(new_link)
    #requests
    team_page = requests.get('https://fbref.com'+link).text #request
    soup = BeautifulSoup(team_page, 'lxml') #parsing
    content = soup.find('div', id='content')
    table = content.find('div', id=f'div_stats_standard_{page_id}')
    player_links = table.find('tbody')
    players = player_links.find_all('tr')

    #creating object
    new_team = Team()
    new_team.name = name
    new_team.year = year
    new_team.coach = soup.find('div', id='meta').find_all('p')[0].text

    for i in players:
        stats = i.find_all('td')
        new_player = create_new_player(i.find('th').text, stats, year, name)
        new_team.players.append(new_player)

    return new_team


def get_stats(year, new_cup):

    print(year)
    print()

    stats_link = f"https://en.wikipedia.org/wiki/{year}_FIFA_Women's_World_Cup"
    stats_page = requests.get(stats_link).text
    stats_soup = BeautifulSoup(stats_page, 'lxml')
    content = stats_soup.find('div', class_='mw-parser-output')
    tables = content.find_all('table', class_='wikitable')

    for j in tables[-1].find('tbody').find_all('tr'):
        print(j)
        for i in new_cup.teams:
            if (j.find('th') == None or j.find('th').find('a') == None):
                continue
            elif (i.name == j.find('th').find('a').text):
                st = j.find_all('td')
                i.group = st[1].find('a').text
                i.ved.append(int(st[3].text))
                i.ved.append(int(st[4].text))
                i.ved.append(int(st[5].text))
                i.goals.append(int(st[6].text))
                i.goals.append(int(st[7].text))
                i.goals.append(i.goals[0] - i.goals[1]) 
                i.points_overall = int(st[9].text)

    return    