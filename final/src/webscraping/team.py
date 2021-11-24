import bs4
from bs4 import BeautifulSoup
import requests
from models import *
import re
from unidecode import unidecode

def check_name(name): #Fixing some names to match Wikipedia
    if (name == 'Zhang Honghong'):
        return 'Zhang Hongdong'
    elif (name == 'Kim Yoo-mi'):
        return 'Kim Yu-mi'
    elif (name == 'Kim Joo-hee'):
        return 'Kim Ju-hee'
    elif (name == 'Myung-Hwa Lee'):
        return 'Lee Myung-hwa'
    elif (name == 'Mirian Silva de Paixao'):
        return 'Miriam'
    else:
        return name

def fix_name(name):
    if (name == 'Hong Myong-hui'):
        return 'Jon Myong-hui'
    if (name == 'Ester'):
        return 'Ester Aparecida dos Santos'
    else:
        return name

def create_new_player(name, stats, year, team_name): 

    tm = team_name
    #assign stats elements to new_player attributes
    new_player = Player()
    new_player.name = fix_name(unidecode(name).replace(',', ''))
    new_player.position = stats[0].text

    if (stats[1].text!=''):
        new_player.age = int(stats[1].text)
    if (stats[6].text!=''):
        new_player.goals = int(stats[6].text)
    if (stats[7].text!=''):
        new_player.assists = int(stats[7].text)
    if (stats[11].text!=''):   
        new_player.yellow_cards = int(stats[11].text)
    if (stats[12].text!=''):
        new_player.red_cards = int(stats[12].text)

    #Fixing missing infos from player

    problem_count = 0 

    if (new_player.position == '' or new_player.age == 0):
        problem_count = 1
        
    if (problem_count):
        comparing_name = check_name(new_player.name)
        wiki_link = f"https://en.wikipedia.org/wiki/{year}_FIFA_Women's_World_Cup_squads"
        wiki_page = requests.get(wiki_link).text #request
        soup = BeautifulSoup(wiki_page, 'lxml') #parsing
        content = soup.find('div', id='mw-content-text')
        count = 0 #table index in Wikipedia's page

        if (tm == 'Korea DPR'): #Matching Wikipeddia
            tm = 'North Korea'
        if (tm == 'Korea Republic'):
            tm = 'South Korea'

        for i in content.find_all('h3'):
            if (i.find('span').text == tm):
                table = content.find_all('table')[count]
                body = table.find('tbody')
                meter = 0
                for k in body.find_all('tr'):
                    if (meter != 0):
                        if (comparing_name in unidecode(k.find('th').find('a').text) or comparing_name in unidecode(k.find('th').find('a')['href'])
                        or unidecode(k.find('th').find('a').text) in comparing_name):
                            stat = k.find_all('td')
                            if (new_player.position == ''):
                                new_player.position = stat[1].find('a').text
                            if (new_player.age == 0):
                                
                                string  = stat[2].text
                                age = [int(s) for s in string.split() if s.isdigit()]
                                
                                new_player.age = int(year - age[0])
                    else:
                        meter+=1
                break
            else:
                count += 1

    return new_player


def create_new_team(link, name, page_id, year):

    
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
    new_team.coach = soup.find('div', id='meta').find_all('p')[0].text.replace('Manager: ', '', 1)

    for i in players:
        stats = i.find_all('td')
        new_player = create_new_player(i.find('th').text, stats, year, name)
        new_team.players.append(new_player)

    return new_team


def get_stats(year, new_cup):

    

    stats_link = f"https://en.wikipedia.org/wiki/{year}_FIFA_Women's_World_Cup"
    stats_page = requests.get(stats_link).text
    stats_soup = BeautifulSoup(stats_page, 'lxml')
    content = stats_soup.find('div', class_='mw-parser-output')
    tables = content.find_all('table', class_='wikitable')

    for j in tables[-1].find('tbody').find_all('tr'):
        for i in new_cup.teams:
            comparing_name = ''
            if (i.name == 'Korea DPR'):
                comparing_name = 'North Korea'
            elif (i.name == 'Korea Republic'):
                comparing_name = 'South Korea'
            elif (i.name == "Côte d'Ivoire"):
                comparing_name = 'Ivory Coast'
            else:
                comparing_name = i.name

            if (j.find('th') == None or j.find('th').find('a') == None):
                continue
            elif (comparing_name == j.find('th').find('a').text):
                st = j.find_all('td')
                i.group = st[1].find('a').text
                # #print(i.name, i.group)
                i.ved.append(int(st[3].text))
                i.ved.append(int(st[4].text))
                i.ved.append(int(st[5].text))
                i.goals.append(int(st[6].text))
                i.goals.append(int(st[7].text))
                i.goals.append(i.goals[0] - i.goals[1]) 
                i.points_overall = int(st[9].text)
    return    

def get_stats_2019(new_cup):

    wiki_link = f"https://en.wikipedia.org/wiki/2019_FIFA_Women's_World_Cup_squads"
    wiki_page = requests.get(wiki_link).text #request
    soup = BeautifulSoup(wiki_page, 'lxml') #parsing
    content = soup.find('div', id='mw-content-text')
    teams = content.find_all('h3')
    # #print(2019)
    # #print()

    for i in new_cup.teams:
        comparing_name = ''
        group_count = 0
        if (i.name == 'Korea DPR'):
            comparing_name = 'North Korea'
        elif (i.name == 'Korea Republic'):
            comparing_name = 'South Korea'
        elif (i.name == "Côte d'Ivoire"):
            comparing_name = 'Ivory Coast'
        else:
            comparing_name = i.name
        for k in teams:
            if (k.find('span').text == comparing_name):
                if (group_count <= 3):
                    i.group = 'A'
                    #print(i.name, i.group)
                elif (group_count > 3 and group_count <= 7):
                    i.group = 'B'
                    #print(i.name, i.group)
                elif (group_count > 7 and group_count <= 11):
                    i.group = 'C'
                    #print(i.name, i.group)
                elif (group_count > 11 and group_count <= 15):
                    i.group = 'D'
                    #print(i.name, i.group)
                elif (group_count > 15 and group_count <= 19):
                    i.group = 'E'
                    #print(i.name, i.group)
                else:
                    i.group = 'F'
                    #print(i.name, i.group)
            else:
                group_count+=1
    
    fbref_link = 'https://fbref.com/en/comps/106/Womens-World-Cup-Stats'
    fbref_page = requests.get(fbref_link).text #request
    soup = BeautifulSoup(fbref_page, 'lxml') #parsing
    content = soup.find('div', id='content')
    results = content.find('div', id='all_results17860')
    table = results.find('table', id='results17860_overall')
    body = table.find('tbody')

    for i in body.find_all('tr'):
        if (not i.has_attr('class')):
            info = i.find_all('td')
            for k in new_cup.teams:
                if (k.name == info[0].find('span')['title']):
                    k.ved.append(int(info[2].text))
                    k.ved.append(int(info[3].text))
                    k.ved.append(int(info[4].text))
                    k.goals.append(int(info[5].text))
                    k.goals.append(int(info[6].text))
                    k.goals.append(k.goals[0] - k.goals[1])
                    k.points_overall = int(info[8].text)

def get_points_group_stage(year, world_cup, page_id):

    if (year == 2019):
        fbref_link = 'https://fbref.com/en/comps/106/Womens-World-Cup-Stats'
    else:
        fbref_link = f'https://fbref.com/en/comps/106/{page_id}/{year}-Womens-World-Cup-Stats'

    fbref_page = requests.get(fbref_link).text #request
    soup = BeautifulSoup(fbref_page, 'lxml') #parsing
    content = soup.find('div', id='content')
    group_stage = content.find('div', id = 'all_Group stage')
    group_div = group_stage.find('div', id='div_Group stage')
    groups = group_div.find_all('div', class_='table_wrapper tabbed')

    for i in groups:
        results = i.find_all('div')
        body = results[2].find('tbody').find_all('tr')
        for k in body:
            stats = k.find_all('td')
            name = stats[0].find('span')['title']
            for j in world_cup.teams:
                if (j.name == name):
                    j.points_group_stage = int(stats[8].text)

    return
                


