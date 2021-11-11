import sys
from requests.api import get
from models import *
sys.path.insert(0, '/previa/src/webscraping/')
from webscraping import cup
from webscraping import matches

if __name__ == "__main__":

    start_year = 2015
    final_year = 2019
    page_id = 1785
    cup_list = []
    while (start_year<=final_year):
        i = cup.create_new_cup(start_year, page_id)
        cup_list.append(i)
        start_year += 4
        page_id += 1