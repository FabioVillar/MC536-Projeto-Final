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

def match_report_2019(link, match):
    r = requests.get(link)
    #print(r.status_code)
    soup = BeautifulSoup(r.content, 'lxml')
    #Formations:
    c = soup.find('div', id = 'content')
    f = c.find('div', id = 'field_wrap')
    #Info from team1:
    a = f.find('div', id = 'a')
    n = a.find('tr')
    n = n.text.split(' ')
    formation1 = n[-1]
    print("Formation 1:", formation1)
    print("Starters:")
    rows = a.select('tr')
    count = 1
    for player in rows:
        if count == 1 or count == 13:
            if count == 13:
                print("\nBench:")
            count += 1
            continue
        aux = player.find('a')
        player_name = aux.text
        print(player_name)
        if count < 13:
            match
        count += 1
    #Info from team2:
    b = f.find('div', id = 'b')
    n = b.find('tr')
    n = n.text.split(' ')
    formation2 = n[-1]
    print("\nFormation 2:", formation2)
    print("Starters:")
    rows = b.select('tr')
    count = 1
    for player in rows:
        if count == 1 or count == 13:
            if count == 13:
                print("\nBench:")
            count += 1
            continue
        aux = player.find('a')
        player_name = aux.text
        print(player_name)
        count += 1
    match.formations.append(formation1)
    match.formations.append(formation2)
    #Penalties:

def get_matches(year, page_id, new_cup):
    if year == 2019:
        link = 'https://fbref.com/en/comps/106/schedule/Womens-World-Cup-Scores-and-Fixture'
    r = requests.get(link)
    #print(r.status_code)
    soup = BeautifulSoup(r.content, 'lxml')
    c = soup.find('div', id = 'content')
    switcher = c.find('div', id = 'div_sched_all')
    t = switcher.find('table', id = 'sched_all')
    rows = soup.select('tbody tr')
    count = 0
    for i in rows:
        if i.has_attr('class') == True:
            continue
        phase = i.find('th').find('a').text
        match_data = i.find_all('td')
        team1 = match_data[4].find('a').text
        team2 = match_data[8].find('a').text
        result = match_data[6].find('a').text
        attendance = match_data[9].text
        stadium = match_data[10].text
        referee = match_data[11].text
        match_link = 'https://fbref.com' + match_data[12].find('a').get('href')
        #Object match created:
        match = Match()
        match.phase = phase
        match.teams = [team1, team2]
        match.score = [result[0], result[2]]
        match.stadium = stadium
        match.attendance = attendance
        match.referee = referee
        #Prints:
        print(attendance)
        print("Phase:", phase)
        print("Home:", team1, "/ Guest:", team2, " /Score:", result)
        print("Attendance: ", attendance, " /Stadium: ", stadium, " /Referee: ", referee)
        print(match_link)
        if year == 2019:
            match_report_2019(match_link, match)
        print("\n")
        count += 1
        if count == 52: #count vai no max ate 52
            break
    return