from requests.api import get
from web_scraping_functions import *
from models import *

if __name__ == "__main__":

    start_year = 1991
    final_year = 2019
    page_id = 1779
    cup_list = []
    get_matches(2011, 0, 0)
    #while (start_year<=final_year):
        #i = create_new_cup(start_year, page_id)
        #cup_list.append(i)
        #start_year += 4
        #page_id += 1