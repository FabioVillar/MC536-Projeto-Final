import mysql.connector as connection
from mysql.connector import errorcode
from models import *


def insert_award(cursor, year_wc, player_id, team_id, award_obj: Award):
    add_award = ("INSERT INTO Awards"
                 "(award_type, year_wc, player_id, team_id) "
                 "VALUES (%s, %s, %s, %s, %s)")
    award_obj_sql = {
        "award_type": award_obj.award,
        "year_wc": year_wc,
        "player_id": player_id,
        "team_id": team_id
    }
    try:
        return cursor.execute(add_award, award_obj_sql)
    except Exception as e:
        print("Erro na inserção de evento na partida", e)
        raise


def find_player_id(cursor, player: Player):
    query = (
        "SELECT P.player_id"
        "FROM Player P"
        "WHERE P.player_name = %s"
    )
    try:
        return cursor.execute(query, player.name)
    except Exception as e:
        print("Erro na busca pelo Id do time", e)
        raise

def find_team_id(cursor, team: Team):

    query = (
        "SELECT T.team_id"
        "FROM Team_wc T"
        "WHERE T.team_name = %s"
    )
    try:
        return cursor.execute(query, team.name)
    except Exception as e:
        print("Erro na busca pelo Id do time", e)
        raise


def insert_event(cursor, match_id, event_obj: Event):
    add_event = ("INSERT INTO Events_wc"
                 "(match_id, event_desc, match_time, team, player) "
                 "VALUES (%s, %s, %s, %s, %s)")
    event_obj_sql = {
        "match_id": match_id,
        "event_desc": event_obj.event,
        "match_time": event_obj.time,
        "team": event_obj.team,
        "player": event_obj.player
    }
    try:
        return cursor.execute(add_event, event_obj_sql)
    except Exception as e:
        print("Erro na inserção de evento na partida", e)
        raise


def insert_matches(cursor, id1, id2, match_obj: Match):
    add_match = ("INSERT INTO Player_wc "
                 "(penaltys, phase, teamA, teamB, score, stadium, attendance, referee, formation_A, formation_B, lineupA, lineupB, reservesA, reservesB, possesion) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    match_obj_sql = {
        "penaltys": match_obj.penalties,
        "phase": match_obj.phase,
        "teamA": id1,
        "teamB": id2,
        "score": match_obj.score,
        "stadium": match_obj.stadium,
        "attendance": match_obj.attendance,
        "referee": match_obj.referee,
        "formation_A": match_obj.formations[0],
        "formation_B": match_obj.formations[1],
        "lineupA": match_obj.initial_squad1,
        "lineupB": match_obj.initial_squad2,
        "reservesA": match_obj.bench_players1,
        "reservesB": match_obj.bench_players2,
        "possesion": match_obj.possesion
    }
    try:
        cursor.execute(add_match, match_obj_sql)
        return cursor.lastrowid
    except Exception as e:
        print("error in match insertion: ", e)
        raise


def insert_player_wc(time_id, cursor, player_obj: Player):
    add_player = ("INSERT INTO Player_wc "
                  "(team_id, player_name, player_number, age, position, goals, assists,yellow_cards, red_cards) "
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    player_obj_sql = {
        "team_id": time_id,
        "player_name": player_obj.name,
        "player_number": player_obj.number,
        "age": player_obj.age,
        "position": player_obj.position,
        "goals": player_obj.goals,
        "assists": player_obj.assists,
        "yellow_cards": player_obj.yellow_cards,
        "red_cards": player_obj.red_cards
    }

    try:
        cursor.execute(add_player, player_obj_sql)
        return cursor.lastrowid
    except Exception as e:
        print("error in player insertion: ", e)
        raise


def insert_teams_wc(cursor, year_wc, team_obj: Team):
    if year_wc == team_obj.year:
        add_team = ("INSERT INTO Team_wc "
                    "(year_wc, team_name, coach, group_in_wc, group_points, ranking_group, goals_scored, goals_suffered, wins, draws, losses) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        team_obj_sql = {
            "year_wc": team_obj.year,
            "team_name": team_obj.name,
            "coach": team_obj.coach,
            "group_in_wc": team_obj.group,
            "group_points": team_obj.points_group_stage,
            "ranking_group": team_obj.position_group,
            "goals_scored": team_obj.goals[0],
            "goals_suffered": team_obj.goals[1],
            "wins": team_obj.ved[0],
            "draws": team_obj.ved[1],
            "losses": team_obj.ved[2]
        }
        try:
            cursor.execute(add_team, team_obj_sql)
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
              "(year_wc, host, winner) "
              "VALUES (%s, %s, %s)")
    wc_object_sql = {
        "year_wc": wc_object.year,
        "host": wc_object.host
    }
    try:
        cursor.execute(add_wc, wc_object_sql)
        return cursor.lastrowid

    except Exception as e:
        print("error in wc insertion: ", e)
        raise


def mysql_connection(user, database, password):
    try:
        cnx = connection.connect(
            user=user, password=password, database=database)
    except connection.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    return cnx


def main():
    print('bgfhryj')
    # cnx = mysql_connection()
    # cursor = cnx.cursor()


    # cnx.commit()
    # cursor.close()
    # cnx.close()
main()
