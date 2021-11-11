from pymongo import MongoClient
from models import *
import pymongo
import json
# id copa do mundo - > ano


def insert_wc_db(collection, object):

    try:
        post_id = collection.insert_one(object).inserted_id
        return post_id
    except Exception as e:
        raise e


def create_table(client):
    db = client.womens_world_cup
    table = db.world_cups
    try:
        result = db.table.create_index(
            [('world_cup_id', pymongo.ASCENDING)], unique=True)
        return table
    except Exception as e:
        raise e


def mongo():

    try:
        client = MongoClient('mongodb://localhost:27017/')

    except Exception as e:
        raise e
    print(client.list_database_names())
    table = create_table(client)
    print(sorted(list(table.index_information())))
    # with open('teste.json','r+',errors='ignore') as f:
    #     wc_obj = json.load(f)
    # print(insert_wc_db(table, wc_obj))
mongo()
