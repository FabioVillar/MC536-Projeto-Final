import sys
from requests.api import get
from models import *
sys.path.insert(0, '/previa/src/webscraping/')
from webscraping import cup
from webscraping import matches
import json

if __name__ == "__main__":

    start_year = 1991
    final_year = 1991
    page_id = 1779
    cup_list = []
    while (start_year<=final_year):
        i = cup.create_new_cup(start_year, page_id)
        cup_list.append(i)
        start_year += 4
        page_id += 1

with open(f'webscraping/teste.json', 'w+') as f:
            json.dump(
                cup_list[0].dict(exclude_none=True),
                f,
                ensure_ascii=False,
                indent=2
            )
    