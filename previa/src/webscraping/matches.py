import bs4
from bs4 import BeautifulSoup
import requests
from models import *
import re
from unidecode import unidecode


def fix_name(name, year):
    if (name == "Karasiova Ol'ga Valentinovna"):
        return 'Olga Karasseva'
    if (name == "Monica Hickmann Alves" and year != 2015 and year != 2019):
        return 'Monica Angelica de Paula'
    if (name == "Michelle O'Neill"):
        return "Natalia Pablos"
    if (name == 'Monica Angelica de Paula' and year == 2015):
        return "Monica Hickmann Alves"
    else:
        return name

def get_matches(year, page_id, new_cup):

    print("Getting Matches...", end="")

    link = 'https://fbref.com/en/comps/106/'

    if year == 2019:
        link = link+'schedule/Womens-World-Cup-Scores-and-Fixture'
    else:
        link = link+f'{page_id}/schedule/{year}-Womens-World-Cup-Scores-and-Fixtures'


    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'lxml')

    if year == 2019:
        content = soup.find('div', id = 'content')
        switcher = content.find('div', id = 'div_sched_all')
        table = switcher.find('table', id = 'sched_all')

        for i in table.find('tbody').find_all('tr'):

            if i.has_attr('class') == True:
                continue

            match_data = i.find_all('td')
            team1 = match_data[4].find('span')['title']
            team2 = match_data[8].find('span')['title']
            score = match_data[6].find('a').text.split('–')
            match_link = 'https://fbref.com' + match_data[12].find('a').get('href')

            #Object match created:
            match = Match()
            
            if team1 == 'USA':
                team1 = 'United States'
            elif team2 == 'USA':
                team2 = 'United States'
            if team1 == 'Korea Rep':
                team1 = 'Korea Republic'
            elif team2 == 'Korea Rep':
                team2 = 'Korea Republic'    

            match.phase = i.find('th').find('a').text
            match.teams = [team1, team2]
            match.score = [int(score[0]), int(score[1])]
            match.stadium = match_data[10].text
            match.attendance = match_data[9].text
            match.referee = match_data[11].text

            for team in new_cup.teams:
                if match.phase == 'Group stage':
                    if team.name == match.teams[0] or team.name == match.teams[1]:
                        match.group = team.group
            
            match_report_2015_and_2019(match_link, match, new_cup)
            new_cup.matches.append(match)
    else:

        wrap = soup.find('div',id = 'wrap')
        content = wrap.find('div', id = 'content')
        schedule = content.find('div', id = 'all_sched')
        switcher = schedule.find('div', id = 'switcher_sched')
        table = switcher.find('div', id = 'div_sched_all')

        for i in table.find('tbody').find_all('tr'):

            if i.has_attr('class') == True:
                continue

            match_data = i.find_all('td')

            if year == 2015 or year == 2011:
                team1 = match_data[4].find('a').text
                team2 = match_data[6].find('a').text
                score = match_data[5].find('a').text.split('–')
                attendance = match_data[7].text
                stadium = match_data[8].text
                referee = match_data[9].text
                match_link = 'https://fbref.com' + match_data[10].find('a').get('href')
            else:
                team1 = match_data[3].find('a').text
                team2 = match_data[5].find('a').text
                score = match_data[4].find('a').text.split('–')
                attendance = match_data[6].text
                stadium = match_data[7].text
                referee = match_data[8].text
                match_link = 'https://fbref.com' + match_data[9].find('a').get('href')

            #Object match created:
            match = Match()

            if team1 == 'USA':
                team1 = 'United States'
            elif team2 == 'USA':
                team2 = 'United States'
            if team1 == 'Korea Rep':
                team1 = 'Korea Republic'
            elif team2 == 'Korea Rep':
                team2 = 'Korea Republic'    
                
            match.phase = i.find('th').find('a').text
            match.teams = [team1, team2]
            match.score = [int(score[0]), int(score[1])]
            match.stadium = stadium
            match.attendance = attendance
            match.referee = referee

            for team in new_cup.teams:
                if match.phase == 'Group stage':
                    if team.name == match.teams[0] or team.name == match.teams[1]:
                        match.group = team.group

            if year == 2015:
                match_report_2015_and_2019(match_link, match, new_cup)
            else:
                match_report(match_link, match, new_cup)

            new_cup.matches.append(match)
    
    print("Ok!")
    return


def match_report(link, match, new_cup):

    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'lxml')

    content = soup.find('div', id = 'content')

    #Finding the initial squads and bench
    y = 0 #Variable used to iterate the for on line 111 two times

    for x in content.find_all('div', class_ = 'table_wrapper tabbed'):

        id = x['id']
        v = id.split('_')
        id = v[3]
        stats = x.find('div', id = 'div_stats_' + id + '_summary')
        
        for i in stats.find('tbody').find_all('tr'):

            name = i.find('th').text.replace(',', '')
            data = i.find_all('td')
            player_position = data[1].text
            player_position = player_position.split(',')[0]

            if name[0].isascii() == True or name[1].isascii() == True:#This separates the initial squad from the substitutes
                if player_position == '':
                    for team in new_cup.teams:
                        if (match.teams[y] == team.name):
                            for player in team.players:
                                if (unidecode(player.name) == unidecode(name)):
                                    player_position = player.position.split(',')[0]
                                    # print("Fixed: " + player_position)
                if y == 0:
                    match.initial_squad1.append(unidecode(fix_name(name, new_cup.year)))
                    if (player_position == 'DF' or player_position == 'LB' or
                    player_position == 'CB' or player_position == 'RB'):
                        match.formation1[0] += 1
                    elif (player_position == 'MF' or player_position == 'DM' or 
                    player_position == 'CM'):
                        match.formation1[1] += 1
                    elif (player_position == 'FW' or player_position == 'RW' or
                    player_position == 'LW'):
                        match.formation1[2] += 1
                    
                else:
                    match.initial_squad2.append(name)
                    if (player_position == 'FW' or player_position == 'RW' or
                    player_position == 'LW'):
                        match.formation2[2] += 1
                    elif (player_position == 'MF' or player_position == 'DM' or 
                    player_position == 'CM'):
                        match.formation2[1] += 1
                    elif (player_position == 'DF' or player_position == 'LB' or
                    player_position == 'CB' or player_position == 'RB'):
                        match.formation2[0] += 1
            else:
                new_name = fix_name(unidecode(i.find('th').find('a').text).replace(',', ''), new_cup.year)
                if y == 0:
                    match.bench_players1.append(new_name)
                else:
                    match.bench_players2.append(new_name)
        y += 1
        if y == 2:
            break

    #Append on unused reserves
    y = 0
    for x in content.find_all('div', class_ = 'table_wrapper tabbed'):
        id = x['id']
        v = id.split('_')
        id = v[3]
        div_stats = x.find('div', id = 'div_stats_' + id + '_summary')
        t_stats = div_stats.find('div', id = 'tfooter_stats_'+ id + '_summary')

        for z in t_stats.find_all('a'):
            name = fix_name(unidecode(z.text).replace(',', ''), new_cup.year)
            if y == 0:
                match.bench_players1.append(name)
            else:
                match.bench_players2.append(name)
        y += 1
        if y == 2:
            break

    match_report_event(content, match, 'event a')
    match_report_event(content, match, 'event b')
    return


def match_report_goal_related(match, event, a, t2, new_cup):
    time = event.time
    if a.find('div', class_ = 'event_icon goal'):
        event.event = 'Goal'
    elif a.find('div', class_ = 'event_icon penalty_goal'):
        event.event = 'Penalty Goal'
    elif a.find('div', class_ = 'event_icon penalty_miss'):
        event.event = 'Penalty Missed'
    elif a.find('div', class_ = 'event_icon own_goal'):
        event.event = 'Own Goal'

    links = t2.find_all('a')
    name = unidecode(links[0].text).replace(',', '')
    event.player = fix_name(name, new_cup.year)
 
    if (len(links)>1): 
        assist = Event()
        assist.event = 'Assist'
        assist.time = time
        name = fix_name(unidecode(links[1].text).replace(',', ''), new_cup.year)
        assist.player = name
        assist.team = event.team
        match.events.append(assist)
    return


def match_report_substitution(match, event, t2, new_cup):
    event.event = 'Substitute in'
    name = unidecode(t2.find_all('a')[0].text).replace(',', '')
    event.player = fix_name(name, new_cup.year)

    s = Event()
    s.event = "Substitute out"
    s.time = event.time
    s.team = event.team
    name = unidecode(t2.find_all('a')[1].text).replace(',', '')
    s.player = fix_name(name, new_cup.year)
    match.events.append(s)
    return

def match_report_card(match, event, t2, card, new_cup):
    name = unidecode(t2.find('a').text).replace(',', '')
    event.player = fix_name(name, new_cup.year)
    if card == 'Both':
        event.event = 'Yellow Card'
        red_card = Event()
        red_card.event = 'Red Card'
        red_card.time = event.time
        red_card.team = event.team
        name = event.player
        red_card.player = name
        match.events.append(red_card)
    else:
        event.event = card
    return


def match_report_penalties(match, event, a, t2, cl, new_cup):
    if a.find('div', class_ = 'event_icon penalty_shootout_goal'):
        event.event = 'Penalty shootout goal'
        if cl == 'event a':
            match.penalties[0] += 1
        elif cl == 'event b':
            match.penalties[1] += 1
    else:
        event.event = 'Penalty shootout miss'
    name = unidecode(t2.find('a').text).replace(',', '')
    event.player = fix_name(name, new_cup.year)
    return
    


def match_report_event(c, match, cl, new_cup):
    m = c.find('div', id = 'events_wrap')
    m = m.find('div', id = '')
    eventsa = m.find_all('div', class_ = cl)
    for a in eventsa:
        all_div = a.find_all('div')
        t1 = all_div[0].text.split()
        t2 = all_div[1]
        #print(t1, t2, t3)
        event = Event()
        if cl == 'event a':
            event.team = match.teams[0]
        elif cl == 'event b':
            event.team = match.teams[1]
        time = t1[0].split('&')
        time = time[0]
        event.time = time
        if a.find('div', class_ = 'event_icon goal') or a.find('div', class_ = 'event_icon penalty_goal') or a.find('div', class_ = 'event_icon penalty_miss') or a.find('div', class_ = 'event_icon own_goal'):
            match_report_goal_related(match, event, a, t2, new_cup)
        elif a.find('div', class_ = 'event_icon substitute_in'):
            match_report_substitution(match, event, t2, new_cup)
        elif a.find('div', class_ = 'event_icon yellow_card'):
            match_report_card(match, event, t2, 'Yellow Card', new_cup)
        elif a.find('div', class_ = 'event_icon red_card'):
            match_report_card(match, event, t2, 'Red Card', new_cup)
        elif a.find('div', class_ = 'event_icon yellow_red_card'):
            match_report_card(match, event, t2, 'Both', new_cup)
        elif a.find('div', class_ = 'event_icon penalty_shootout_goal') or a.find('div', class_ = 'event_icon penalty_shootout_miss'):
            match_report_penalties(match, event, a, t2, cl, new_cup)
        
        match.events.append(event)
    return


def match_report_2015_and_2019(link, match, new_cup):
    r = requests.get(link)
    #print(r.status_code)
    soup = BeautifulSoup(r.content, 'lxml')
    c = soup.find('div', id = 'content')
    f = c.find('div', id = 'field_wrap')
    #Info from team1:
    a = f.find('div', id = 'a')
    n = a.find('tr')
    n = n.text.split(' ')
    formation1 = n[-1]
    for character in formation1:
        if character == '(' or character == ')':
            formation1 = formation1.replace(character, '')
    formation1 = formation1.split('-')
    new_form1 = []
    for number in formation1:
        try:
            new_form1.append(int(number))
        except ValueError:
            try:
                new_form1.append(int(number[0]))
            except ValueError:
                continue
    formation1 = new_form1
    match.formation1 = formation1
    rows = a.select('tr')
    count = 1
    for player in rows:
        if count == 1 or count == 13:
            #if count == 13:
                #print("\nBench:")
            count += 1
            continue
        aux = player.find('a')
        player_name = unidecode(aux.text).replace(',', '')
        #print(player_name)
        if count < 13: 
            match.initial_squad1.append(player_name)
        elif count > 13:
            match.bench_players1.append(player_name)
        count += 1
    #Info from team2:
    b = f.find('div', id = 'b')
    n = b.find('tr')
    n = n.text.split(' ')
    formation2 = n[-1]
    for character in formation2:
        if character == '(' or character == ')':
            formation2 = formation2.replace(character, '')
    formation2 = formation2.split('-')
    new_form2 = []
    for number in formation2:
        try:
            new_form2.append(int(number))
        except ValueError:
            try:
                new_form2.append(int(number[0]))
            except ValueError:
                continue
    formation2 = new_form2
    match.formation2 = formation2
    # print("Team :", match.teams[0])
    # print("\nTeam :", match.teams[1])
    # print("\nFormation:", match.formation2)
    # print("Starters:")

    rows = b.select('tr')
    count = 1
    for player in rows:
        if count == 1 or count == 13:
            #if count == 13:
                #print("\nBench:")
            count += 1
            continue
        aux = player.find('a')
        player_name = unidecode(aux.text).replace(',', '')
        #print(player_name)
        if count < 13:
            match.initial_squad2.append(player_name)
        elif count > 13:
            match.bench_players2.append(player_name)
        count += 1
    #Events:
    #print("\nEvent/ Time/ Country/ Player:")
    match_report_event(c, match, 'event a', new_cup)
    match_report_event(c, match, 'event b', new_cup)
    return