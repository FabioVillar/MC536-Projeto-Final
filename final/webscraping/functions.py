from bs4 import BeautifulSoup
import requests
from classes import *


def create_new_team(link, name):

    new_team = Team()
    new_team.name = name
    team_page = requests.get('https://fbref.com/'+link).text #request
    soup = BeautifulSoup(team_page, 'lxml') #parsing
    content = soup.find('div', id='content')
    table = content.find('div', class_='table_container current is_setup')
    print(table)
    player_links = table.find('tbody')
    players = player_links.find_all('tr')
    for i in players:
        stats = i.find_all('td')
        new_player = Player(i.find('th')['csk'], stats[0].text, stats[1].text, stats[6].text, stats[7].text, stats[11].text, stats[12].text)
        Team.players.append(new_player)
    return new_team

def create_new_cup(year, page_id):
    link = None
    if (year == 2019):

        link = 'https://fbref.com/en/comps/106/qual/Womens-World-Cup-Qualifying-Rounds'
    else:

        link = f'https://fbref.com/en/comps/106/{page_id}/qual/{year}-Womens-World-Cup-Qualifying-Rounds'
    
    new_cup = WorldCup()
    new_cup.year = year

    cup_page = requests.get(link).text #request
    soup = BeautifulSoup(cup_page, 'lxml') #parsing
    table = soup.find('div', id='div_qualification')
    team_links = table.find('tbody')
    teams = team_links.find_all('tr')

    team_count = 0
    for i in teams:
        new_team = create_new_team(i.find('a')['href'], i.find('a').text)
        WorldCup.teams.append(new_team)
        team_count+=1

    new_cup.number_of_teams = team_count

    return new_cup