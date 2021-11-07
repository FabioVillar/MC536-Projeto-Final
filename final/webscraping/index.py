from functions import *
from classes import *

if __name__ == "__main__":

    start_year = 1991
    final_year = 2019
    page_id = 1779
    cup_list = []


    while (start_year<=final_year):
        print()
        print(start_year)
        i = create_new_cup(start_year, page_id)
        print()
        for j in i.teams:
            print(j.name)
            print()
            print("Players:")
            print()
            for k in j.players:
                print(k.name, k.age, k.position, k.goals_scored)
            print()
        cup_list.append(i)
        start_year += 4
        page_id += 1