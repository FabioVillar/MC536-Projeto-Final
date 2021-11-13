import mysql.connector
from mysql.connector import errorcode
from models import *
import uuid
# from main import *
import json
from unidecode import unidecode


def find_player_id(cursor, player, year_wc):
    
    query = (
        "SELECT id FROM Player_wc P"
        " WHERE INSTR(P.player_name, %s) > 0 and P.year_wc = %s"
    )
    data = (player, year_wc)
    try:
        cursor.execute(query, data)
        return cursor.fetchall()
    except Exception as e:
        print("Erro na busca pelo Id do time", e)
        raise


def find_team_id(cursor, team, year_wc):

    query = ("SELECT id FROM Team_wc AS T"
             " WHERE instr(team_name, %s) and T.year_wc = %s")
    data = (team, year_wc)
    try:
        cursor.execute(query, data)
        return cursor.fetchall()
    except Exception as e:
        print("Erro na busca pelo Id do time\n", e)
        raise


def insert_award_sql(cursor, year_wc, player_id, team_id, award_obj: Award):

    add_award = ("INSERT INTO Awards_wc"
                 "(award_type, year_wc, player_id, team) "
                 "VALUES (%s, %s, %s, %s)")

    award_data = (award_obj['award'], year_wc, player_id, team_id)
    try:
        return cursor.execute(add_award, award_data)
    except Exception as e:
        print("Erro na inserção de evento na partida", e)
        raise


def insert_event_sql(cursor, match_id, event_obj: Event):
    id_key = uuid.uuid4()
    add_event = ("INSERT INTO Events_wc"
                 "(id, match_id, event_desc, match_time, team, player) "
                 "VALUES (%s, %s, %s, %s, %s, %s)")
    data_event = (str(id_key), str(
        match_id), event_obj['event'], str(event_obj['time']), event_obj['team'], event_obj['player'])
    try:
        return cursor.execute(add_event, data_event)
    except Exception as e:
        print("Erro na inserção de evento na partida", e)
        raise


def insert_matches_sql(cursor, id1, id2, match_obj: Match, year_wc):
    id_key = uuid.uuid4()
    add_match = ("INSERT INTO Match_wc "
                 "(id, penalties, phase, teamA, teamB, score, stadium, attendance, referee, formation_A, formation_B, lineupA, lineupB, reservesA, reservesB, possesion, year_wc) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)")
    penalties = [str(a) for a in match_obj['penalties'] ]
    penalties = 'x'.join(penalties)
    score = 'x'.join(match_obj['score'])
    form1 = [str(a) for a in match_obj['formation1']]
    form2 = [str(a) for a in match_obj['formation2']]
    formation1 = '-'.join(form1)
    formation2 = '-'.join(form2)
    initial1 = ', '.join(match_obj['initial_squad1'])
    initial2 = ', '.join(match_obj['initial_squad2'])
    bench1 = ', '.join(match_obj['bench_players1'])
    bench2 = ', '.join(match_obj['bench_players2'])

    data_match = (str(id_key), penalties, match_obj['phase'], id1, id2, score, match_obj['stadium'],
                  (str(match_obj['attendance'])
                   ), match_obj['referee'], formation1, formation2, initial1,
                  initial2, bench1, bench2, match_obj['possesion'], year_wc
                  )

    try:
        cursor.execute(add_match, data_match)
        return id_key
    except Exception as e:
        print("error in match insertion: ", e)
        raise


def insert_player_wc_sql(time_id, cursor, player_obj: Player, year_wc):
    add_player = ("INSERT INTO Player_wc "
                  "(id, team_id, player_name, age, position, goals, assists,yellow_cards, red_cards, year_wc) "
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)")
    player_data = (str(uuid.uuid4()), str(time_id), player_obj['name'], player_obj['age'], player_obj['position'],
                   player_obj['goals'], player_obj['assists'], player_obj['yellow_cards'], player_obj['red_cards'], year_wc)

    try:
        cursor.execute(add_player, player_data)
        return cursor.lastrowid
    except Exception as e:
        print("error in player insertion: ", e)
        raise


def insert_teams_wc_sql(cursor, year_wc, team_obj: Team):
    if year_wc == team_obj['year']:
        id_team = uuid.uuid4()
        add_team = ("INSERT INTO Team_wc "
                    "(id, year_wc, team_name, coach, group_in_wc, group_points, overall_points, goals_scored, goals_conceded, wins, draws, losses) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        data_team = (str(id_team), team_obj['year'], team_obj['name'], team_obj['coach'], team_obj['group'], team_obj['points_group_stage'],
                     team_obj['points_overall'], team_obj['goals'][0], team_obj['goals'][1], team_obj['ved'][0], team_obj['ved'][1], team_obj['ved'][2])

        try:
            cursor.execute(add_team, data_team)
            return id_team
        except Exception as e:
            print("error in team insertion: ", e)
            raise
    else:
        print(
            f"Anos diferentes entre copa do mundo e time.\nAno copa: {year_wc}\nAno time: {team_obj.year}")
        return None


def insert_world_cup_sql(cursor, wc_object: WorldCup):
    add_wc = ("INSERT INTO WorldCup "
              "(id, host) "
              "VALUES (%(id)s, %(host)s)")
    wc_object_sql = {
        "id": wc_object['year'],
        "host": wc_object['host']
    }

    try:
        cursor.execute(add_wc, wc_object_sql)
        return cursor.lastrowid

    except Exception as e:
        print("error in wc insertion: ", e)
        raise


def insert_team_and_players(teams):
    teams_id = 0
    for team in teams:
        team
        teams_id += 1
        for player in team['players']:
            print(player)


def insert_matches_and_events(matches):
    matches_id = 0
    for match in matches:
        matches_id += 1
        events = 0
        for event in match['events']:
            event
            events += 1


def insert_awards(awards):
    for award in awards:
        print(award)


def object_management(wc_obj):
    # wc_id = insert_world_cup(wc_obj)
    teams = wc_obj['teams']
    matches = wc_obj['matches']
    awards = wc_obj['awards']


def sql_manager():
    # user = os.environ.get('sql_user')
    # password = os.environ.get('sql_password')
    database = 'womens_world_cup'
    try:
        cnx = mysql.connector.connect(
            user='root', password='admin123', database=database, host='localhost')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    cursor = cnx.cursor(buffered=True)
    start_year = 1991
    last_year = 2019
    for year in range(start_year,last_year +1,4):
        with open(f'world_cup{year}.json', 'r+', errors='ignore') as f:
            wc_obj = json.load(f)
        id_wc = wc_obj['year']
        id_wc = insert_world_cup_sql(cursor, wc_obj)
        teams = wc_obj['teams']
        for team in teams:
            team_id = insert_teams_wc_sql(cursor, id_wc, team)
            for player in team['players']:
                insert_player_wc_sql(team_id, cursor, player, id_wc)
        matches = wc_obj['matches']
        for match in matches:
            id1 = find_team_id(cursor, match['teams'][0].strip(), id_wc)
            id2 = find_team_id(cursor, match['teams'][1].strip(), id_wc)
            match_id = insert_matches_sql(
                cursor, id1[0][0], id2[0][0], match, id_wc)
            for event in match['events']:
                print(event, id_wc)
                event['player'] = find_player_id(
                    cursor, unidecode(event['player'].strip()), id_wc)[0][0]
                event['team'] = find_team_id(
                    cursor, event['team'].strip(), id_wc)[0][0]
                print(event, id_wc)
                insert_event_sql(cursor, match_id, event)
        awards = wc_obj['awards']
        for award in awards:
            print(award)
            player_id_award = find_player_id(
                cursor, unidecode(award['player']), id_wc)[0][0]
            team_id = find_team_id(cursor, award['team'], id_wc)[0][0]
            insert_award_sql(cursor, id_wc, player_id_award, team_id, award)

    cnx.commit()
    cursor.close()
    cnx.close()


sql_manager()
