import mysql.connector
from mysql.connector import errorcode
from models import *
from main import *
import json
def insert_award(cursor, year_wc, player_id, team_id, award_obj: Award):
    add_award = ("INSERT INTO Awards"
                 "(award_type, year_wc, player_id, team_id) "
                 "VALUES (%s, %s, %s, %s)")

    award_data = (award_obj.award, year_wc, player_id, team_id)
    try:
        return cursor.execute(add_award, award_data)
    except Exception as e:
        print("Erro na inserção de evento na partida", e)
        raise


def find_player_id(cursor, player: Player):
    query = (
        "SELECT player_id FROM Player_wc"
        " WHERE Player_wc.player_name = %s"
    )
    data = (player.name, )
    try:
        cursor.execute(query, data)
        return cursor.fetchall()
    except Exception as e:
        print("Erro na busca pelo Id do time", e)
        raise


def find_team_id(cursor, team: Team):

    query = ("SELECT team_id FROM Team_wc"
             " WHERE Team_wc.team_name = %s")
    data = (team.name,)
    try:
        cursor.execute(query, data)
        return cursor.fetchall()
    except Exception as e:
        print("Erro na busca pelo Id do time\n", e)
        raise


def insert_event(cursor, match_id, event_obj: Event, event_id):
    add_event = ("INSERT INTO Events_wc"
                 "(event_id, match_id, event_desc, match_time, team, player) "
                 "VALUES (%s, %s, %s, %s, %s, %s)")
    data_event = (event_id, match_id, event_obj.event, event_obj.time, event_obj.team, event_obj.player)
    try:
        return cursor.execute(add_event, data_event)
    except Exception as e:
        print("Erro na inserção de evento na partida", e)
        raise


def insert_matches(cursor, id1, id2, match_obj: Match, match_id):
    add_match = ("INSERT INTO Match_wc "
                 "(match_id, penalties, phase, teamA, teamB, score, stadium, attendance, referee, formation_A, formation_B, lineupA, lineupB, reservesA, reservesB, possesion) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)")

    data_match = (match_id, match_obj.penalties, match_obj.phase, id1, id2, match_obj.score, match_obj.stadium, 
                  match_obj.attendance, match_obj.referee, match_obj.formations[0], match_obj.formations[1], match_obj.initial_squad1,
                  match_obj.initial_squad2, match_obj.bench_players1, match_obj.bench_players2, match_obj.possesion
                  )
    print(data_match)
    try:
        cursor.execute(add_match, data_match)
        return cursor.lastrowid
    except Exception as e:
        print("error in match insertion: ", e)
        raise


def insert_player_wc(time_id, cursor, player_obj: Player, player_id):
    add_player = ("INSERT INTO Player_wc "
                  "(player_id, team_id, player_name, age, position, goals, assists,yellow_cards, red_cards) "
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    player_data = (player_id, time_id, player_obj.name, player_obj.age, player_obj.position,
                   player_obj.goals, player_obj.assists, player_obj.yellow_cards, player_obj.red_cards)

    try:
        cursor.execute(add_player, player_data)
        return cursor.lastrowid
    except Exception as e:
        print("error in player insertion: ", e)
        raise


def insert_teams_wc(cursor, year_wc, team_obj: Team, team_id):
    if year_wc == team_obj.year:
        add_team = ("INSERT INTO Team_wc "
                    "(team_id, year_wc, team_name, coach, group_in_wc, group_points, overall_points, goals_scored, goals_conceded, wins, draws, losses) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        data_team = (team_id, team_obj.year, team_obj.name, team_obj.coach, team_obj.group, team_obj.points_group_stage,
                     team_obj.points_overall, team_obj.goals[0], team_obj.goals[1], team_obj.ved[0], team_obj.ved[1], team_obj.ved[2])

        try:
            cursor.execute(add_team, data_team)
            return cursor.lastrowid
        except Exception as e:
            print("error in team insertion: ", e)
            raise
    else:
        print(
            f"Anos diferentes entre copa do mundo e time.\nAno copa: {year_wc}\nAno time: {team_obj.year}")
        return None


def insert_world_cup(cursor, wc_object: WorldCup):
    add_wc = ("INSERT INTO WorldCup "
              "(id, host) "
              "VALUES (%(id)s, %(host)s)")
    wc_object_sql = {
        "id": wc_object.year,
        "host": wc_object.host
    }
    try:
        cursor.execute(add_wc, wc_object_sql)
        return cursor.lastrowid

    except Exception as e:
        print("error in wc insertion: ", e)
        raise


def main():
    user, password, database = 'root', 'admin123', 'womens_world_cup'
    try:
        cnx = mysql.connector.connect(
            user=user, password=password, database=database, host='localhost')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    cursor = cnx.cursor(buffered=True)
    # wc_list = get_world_cups()
    
    cnx.commit()
    cursor.close()
    cnx.close()


main()
