import bs4
from bs4 import BeautifulSoup
import requests
from models import *
import re

def get_matches(year, page_id, new_cup):
    if year == 2019:
        link = 'https://fbref.com/en/comps/106/schedule/Womens-World-Cup-Scores-and-Fixture'
    else:
        link = 'https://fbref.com/en/comps/106/' + str(int(1785-((2015-year))*(1/4)))+'/schedule/'+str(year)+'-Womens-World-Cup-Scores-and-Fixtures'
    r = requests.get(link)
    #print(r.status_code)
    soup = BeautifulSoup(r.content, 'lxml')
    if year == 2019:
        c = soup.find('div', id = 'content')
        switcher = c.find('div', id = 'div_sched_all')
        t = switcher.find('table', id = 'sched_all')
        rows = t.select('tbody tr')
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
            print("Phase:", phase)
            print("Home:", team1, "/ Guest:", team2, " /Score:", result)
            print("Attendance: ", attendance, " /Stadium: ", stadium, " /Referee: ", referee)
            print(match_link)
            match_report_2015_and_2019(match_link, match)
            print("\n")
            count += 1
            if count == 52: #count vai no max ate 52
                break
    else:
        fb = soup.find('div',id = 'wrap')
        c = fb.find('div', id = 'content')
        c = c.find('div', id = 'all_sched')
        c = c.find('div', id = 'switcher_sched')
        c = c.find('div', id = 'div_sched_all')
        body = c.find('tbody')
        rows = body.find_all('tr')
        for i in rows:
            if i.has_attr('class') == True:
                continue
            phase = i.find('th').find('a').text
            match_data = i.find_all('td')
            if year == 2015 or year == 2011:
                team1 = match_data[4].find('a').text
                team2 = match_data[6].find('a').text
                result = match_data[5].find('a').text
                attendance = match_data[7].text
                stadium = match_data[8].text
                referee = match_data[9].text
                match_link = 'https://fbref.com' + match_data[10].find('a').get('href')
            else:
                team1 = match_data[3].find('a').text
                team2 = match_data[5].find('a').text
                result = match_data[4].find('a').text
                attendance = match_data[6].text
                stadium = match_data[7].text
                referee = match_data[8].text
                match_link = 'https://fbref.com' + match_data[9].find('a').get('href')
            #Object match created:
            match = Match()
            match.phase = phase
            match.teams = [team1, team2]
            match.score = [result[0], result[2]]
            match.stadium = stadium
            match.attendance = attendance
            match.referee = referee
            print("\n\nPhase:", phase)
            print("Home:", team1, "/ Guest:", team2, " /Score:", result)
            print("Attendance: ", attendance, " /Stadium: ", stadium, " /Referee: ", referee)
            print(match_link)
            if year == 2015:
                match_report_2015_and_2019(match_link, match)
            else:
                match_report(match_link, match)

    return


def match_report(link, match):
    r = requests.get(link)
    #print(r.status_code)
    soup = BeautifulSoup(r.content, 'lxml')
    c = soup.find('div', id = 'content')
    #Finding the initial squads and bench
    t = c.find_all('div', class_ = 'table_wrapper tabbed')
    y = 0
    for x in t:
        id = x['id']
        v = id.split('_')
        id = v[3]
        x = x.find('div', id = 'div_stats_' + id + '_summary')
        body = x.find('tbody')
        rows = body.find_all('tr')
        for i in rows:
            name = i.find('th').text
            data = i.find_all('td')
            time_played = data[3].text
            if name[0].isascii() == True:#This separates the initial squad from the substitutes
                if y == 0:
                    match.initial_squad1.append(name)
                else:
                    match.initial_squad2.append(name)
            else:
                name = name.split()
                new_name = ''
                count = 0
                for k in name:
                    new_name = new_name + k
                    if count+1 < len(name):
                        new_name = new_name + ' '
                    count += 1
                if y == 0:
                    match.bench_players1.append(new_name)
                else:
                    match.bench_players2.append(new_name)
        y += 1
        if y == 2:
            break
    #Append on unused reserves
    count = 0
    for x in t:
        id = x['id']
        v = id.split('_')
        id = v[3]
        x = x.find('div', id = 'div_stats_' + id + '_summary')
        x = x.find('div', id = 'tfooter_stats_'+ id + '_summary')
        y = x.find_all('a')
        for z in y:
            if count == 0:
                match.bench_players1.append(z.text)
            else:
                match.bench_players2.append(z.text)
        count += 1
        if count == 2:
            break
    #Print of the players
    print("\nTeam: ", match.teams[0])
    print("\nInitial squad:\n")
    for i in match.initial_squad1:
        print(i)
    print("\nBench:")
    for i in match.bench_players1:
        print(i)
    print("\nTeam: ", match.teams[1])
    print("\nInitial squad:\n")
    for i in match.initial_squad2:
        print(i)
    print("\nBench:")
    for i in match.bench_players2:
        print(i)
    #Events:
    print("\nEvents:")
    match_report_event(c, match, 'event a')
    match_report_event(c, match, 'event b')


def match_report_goal_related(match, event, a, t2):
    time = event.time
    if a.find('div', class_ = 'event_icon goal') or a.find('div', class_ = 'event_icon penalty_goal'):
        event.event = 'Goal'
    elif a.find('div', class_ = 'event_icon penalty_miss'):
        event.event = 'Penalty Missed'
    elif a.find('div', class_ = 'event_icon own_goal'):
        event.event = 'Own Goal'
    name = ''
    for i in t2:
        if i == 'Assist:' or i == 'Penalty' or i == '—' or i == 'Own':
            break
        name = name + ' ' + i
    event.player = name
    if event.event != 'Penalty Missed' and event.event != 'Own Goal':
        if i == 'Assist:':
            assist = Event()
            assist.event = 'Assist'
            assist.time = time
            boolean_assist = False
            name = ''
            for j in t2:
                if j == i:
                    boolean_assist = True
                    continue
                elif j != i and boolean_assist == False:
                    continue
                else:
                    if j == '—':
                        break
                    name = name + ' ' + j
            assist.player = name
            assist.team = event.team
            print(assist.event, assist.time, assist.team, assist.player)
        elif i == 'Penalty':
            penalty = Event()
            penalty.event = 'Penalty'
            penalty.time = time
            penalty.player = event.player
            penalty.team = event.team
            print(penalty.event, penalty.time, penalty.team, penalty.player)


def match_report_substitution(event, t2):
    event.event = 'Substitute'
    name = ''
    for i in t2:
        if i == 'for':
            break
        name = name + ' ' + i
    event.player = name
    s = Event()
    s.event = "Substituted"
    s.time = event.time
    s.team = event.team
    name = ''
    boolean_substitute = False
    for j in t2:
        if j == i:
            boolean_substitute = True
            continue
        elif j != i and boolean_substitute == False:
            continue
        else:
            if j == '—':
                break
            name = name + ' ' + j
    s.player = name
    print(s.event, s.time, s.team, s.player)


def match_report_card(event, t2, card):
    name = ''
    for i in t2:
        if i == '—':
            break
        name = name + ' ' + i
    event.player = name
    if card == 'Both':
        event.event = 'Yellow Card'
        red_card = Event()
        red_card.event = 'Red Card'
        red_card.time = event.time
        red_card.team = event.team
        red_card.player = event.player
        print(red_card.event, red_card.time, red_card.team, red_card.player)
    else:
        event.event = card


def match_report_penalties(match, event, a, t2):
    if a.find('div', class_ = 'event_icon penalty_shootout_goal'):
        event.event = 'Penalty shootout goal'
        name = ''
        for i in t2:
            if i == '—':
                break
            name = name + ' ' + i
        event.player = name
    else:
        event.event = 'Penalty shootout miss'
        name = ''
        for i in t2:
            if i == '—':
                break
            name = name + ' ' + i
        event.player = name
    match.penalties.append(event)


def match_report_event(c, match, cl):
    m = c.find('div', id = 'events_wrap')
    m = m.find('div', id = '')
    eventsa = m.find_all('div', class_ = cl)
    for a in eventsa:
        all_div = a.find_all('div')
        t1 = all_div[0].text.split()
        t2 = all_div[1].text.split()
        t3 = all_div[2].text.split()
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
            match_report_goal_related(match, event, a, t2)
        elif a.find('div', class_ = 'event_icon substitute_in'):
            match_report_substitution(event, t2)
        elif a.find('div', class_ = 'event_icon yellow_card'):
            match_report_card(event, t2, 'Yellow Card')
        elif a.find('div', class_ = 'event_icon red_card'):
            match_report_card(event, t2, 'Red Card')
        elif a.find('div', class_ = 'event_icon yellow_red_card'):
            match_report_card(event, t2, 'Both')
        elif a.find('div', class_ = 'event_icon penalty_shootout_goal') or a.find('div', class_ = 'event_icon penalty_shootout_miss'):
            match_report_penalties(match, event, a, t2)
        print(event.event, event.time, event.team, event.player)
        match.events.append(event)


def match_report_2015_and_2019(link, match):
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
    print("Team :", match.teams[0])
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
            match.initial_squad1.append(player_name)
        elif count > 13:
            match.bench_players1.append(player_name)
        count += 1
    #Info from team2:
    b = f.find('div', id = 'b')
    n = b.find('tr')
    n = n.text.split(' ')
    formation2 = n[-1]
    print("Team :", match.teams[1])
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
        if count < 13:
            match.initial_squad2.append(player_name)
        elif count > 13:
            match.bench_players2.append(player_name)
        count += 1
    match.formations.append(formation1)
    match.formations.append(formation2)
    #Events:
    print("\nEvent/ Time/ Country/ Player:")
    match_report_event(c, match, 'event a')
    match_report_event(c, match, 'event b')