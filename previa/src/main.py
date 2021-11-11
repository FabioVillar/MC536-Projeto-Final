from requests.api import get
from web_scraping_functions import *
from models import *

def get_world_cups():
    start_year = 1991
    final_year = 2019
    page_id = 1779
    cup_list = [
        create_new_cup(i, page_id) for i in range(start_year, final_year + 1, 4)
    ]
    for year in range(start_year, final_year + 1, 4):
        cup_list.append(create_new_cup(year,page_id))
        page_id+=1
    