from bs4 import BeautifulSoup
import requests
from classes import *

def create_new_player(name, stats):
    new_player = Player()
    new_player.name = name
    new_player.position = stats[0].text
    new_player.age = stats[1].text
    new_player.goals_scored = stats[6].text
    new_player.assists = stats[7].text
    new_player.yellow_cards = stats[11].text
    new_player.red_cards = stats[12].text

    return new_player

def create_new_team(link, name, page_id):

    #requests
    team_page = requests.get('https://fbref.com/'+link).text #request
    soup = BeautifulSoup(team_page, 'lxml') #parsing
    content = soup.find('div', id='content')
    table = content.find('div', id=f'div_stats_standard_{page_id}')
    player_links = table.find('tbody')
    players = player_links.find_all('tr')

    
    new_team = Team()
    new_team.name = name

    for i in players:
        stats = i.find_all('td')
        new_player = create_new_player(i.find('th').text, stats)
        new_team.players.append(new_player)
    return new_team

def create_new_cup(year, page_id):

    link = 'https://fbref.com/en/comps/106'
    if (year == 2019):
        link = link + '/qual/Womens-World-Cup-Qualifying-Rounds'
    else:
        link = link + f'/{page_id}/qual/{year}-Womens-World-Cup-Qualifying-Rounds'

    #requests
    cup_page = requests.get(link).text
    soup = BeautifulSoup(cup_page, 'lxml')

    table = soup.find('div', id='div_qualification')
    team_links = table.find('tbody')
    teams = team_links.find_all('tr')

    #creating
    new_cup = WorldCup()
    new_cup.year = year
    new_cup.host = soup.find('div', id='meta').find_all('p')[0].find('a').text

    print(new_cup.host)
    team_count = 0
    for i in teams:
        new_team = create_new_team(i.find('a')['href'], i.find('a').text, page_id)
        new_cup.teams.append(new_team)
        print(i.find('a').text)
        team_count+=1

    new_cup.number_of_teams = team_count

    return new_cup