import mysql.connector as connection
from mysql.connector import errorcode


def insert_teams_wc(year_wc, cursor, team_obj):
    add_team = ("INSERT INTO Team_wc "
                "(year_wc, team_name, coach, group_in_wc, group_points, ranking_group, goals_scored, goals_suffered, wins, draws, losses) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    


def insert_world_cup(cursor, wc_object):
    add_wc = ("INSERT INTO WorldCup "
              "(year_wc, host, winner) "
              "VALUES (%s, %s, %s)")
    cursor.execute(add_wc, wc_object)
    return cursor.lastrowid


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

    cnx = mysql_connection()
    cursor = cnx.cursor()

    # função pega copa
    year_wc = insert_world_cup(cursor, 0)
