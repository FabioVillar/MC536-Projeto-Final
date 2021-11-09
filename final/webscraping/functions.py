from bs4 import BeautifulSoup
import requests
from classes import *

def create_new_player(name, stats): 

    #assign stats elements to new_player attributes
    new_player = Player()
    new_player.name = name
    new_player.position = stats[0].text
    new_player.age = stats[1].text
    new_player.goals = stats[6].text
    new_player.assists = stats[7].text
    new_player.yellow_cards = stats[11].text
    new_player.red_cards = stats[12].text

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
        new_player = create_new_player(i.find('th').text, stats)
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

    #creating teams
    for i in teams:
        new_team = create_new_team(i.find('a')['href'], i.find('a').text, page_id, year)
        new_cup.teams.append(new_team)

    #getting teams overall stats
    get_stats(year, new_cup)

    #getting matches
    get_matches(year, page_id, new_cup)
    
    return new_cup


def get_matches(year, page_id, new_cup):

    link = 'https://fbref.com/en/comps/106'

    if (year == 2019):
        link = link + '/schedule/Womens-World-Cup-Scores-and-Fixtures'
    else:
        link = link + f'/{page_id}/schedule/{year}-Womens-World-Cup-Scores-and-Fixtures'

    print(link)

    matches_page = requests.get(link).text
    soup = BeautifulSoup(matches_page, 'lxml')
    content = soup.find('div', id='content')
    table1 = content.find('div', id='div_sched_all')
    body = table1.find('tbody')
    
    for i in body.find_all('tr'):

        if (i.has_attr('class')):
            continue
        else:   
            new_match = Match()
            info = i.find_all('td')
            stage = i.find('th').find('a').text
            team_name1 = None
            team_name2 = None

            if(year < 2011):
                team_name1 = info[3].find('a').text
                team_name2 = info[5].find('a').text
                new_match.attendance = info[6].text
                new_match.stadium = info[7].text
                new_match.referee = info[8].text
            elif (year == 2019):
                team_name1 = info[4].find('a').text
                team_name2 = info[8].find('a').text
                new_match.attendance = info[9].text
                new_match.stadium = info[10].text
                new_match.referee = info[11].text
            else:
                team_name1 = info[4].find('a').text
                team_name2 = info[6].find('a').text
                new_match.attendance = info[7].text
                new_match.stadium = info[8].text
                new_match.referee = info[9].text
            
            for j in new_cup.teams:
                if (team_name1 == j.name):
                    new_match.teams.append(j)
            for j in new_cup.teams:
                if (team_name2 == j.name):
                    new_match.teams.append(j)

            if (stage == "Group stage"):
                new_match.phase = "GP"
                new_match.group = new_match.teams[0].group
            elif (stage == "Round of 16"):
                new_match.phase = "OF"
            elif (stage == "Quarter-finals"):
                new_match.phase = "QF"
            elif (stage == "Semi-finals"):
                new_match.phase = "SF"
            elif (stage == "Third-place match"):
                new_match.phase = "TF"
            elif (stage == "Final"):
                new_match.phase = "F"

    return