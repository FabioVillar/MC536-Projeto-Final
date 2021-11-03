from functions import *
from classes import *

if __name__ == "__main__":

    start_year = 1991
    final_year = 2019
    page_id = 1779
    cup_list = [0]*8

    for i in cup_list:
        i = create_new_cup(start_year, page_id)
        start_year += 4
        page_id += 1
        print("Copa do ano de " + str(i.year))
        print(i.teams)