import mysql.connector as connection
from mysql.connector import errorcode
from models import *





def insert_player_wc(cursor, player_obj: Player):
    pass



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
            return cursor.execute(add_team, team_obj_sql)
        except Exception as e:
            print("error in team insertion: ", e)
            raise
    else:
        print(f"Anos diferentes entre copa do mundo e time.\nAno copa: {year_wc}\nAno time: {team_obj.year}")
        return None     

def insert_world_cup(cursor, wc_object: WorldCup):
    add_wc = ("INSERT INTO WorldCup "
              "(year_wc, host, winner) "
              "VALUES (%s, %s, %s)")
    wc_object_sql = {
        "year_wc": wc_object.year,
        "host": wc_object.host,
        "winner": wc_object.winner
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