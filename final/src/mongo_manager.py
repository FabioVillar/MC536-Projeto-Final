from pymongo import MongoClient
import sys
sys.path.insert(0, '/previa/data/')
from models import *
import pymongo
import json
import os
# id copa do mundo - > ano


def insert_wc_db(collection, object):

    try:
        post_id = collection.insert_one(object).inserted_id
        return post_id
    except Exception as e:
        raise e


def mongo():

    try:
        client = MongoClient('mongodb://localhost:27017/')

    except Exception as e:
        raise e

    basedir = os.path.abspath(os.path.dirname(__file__))
    basedir = basedir.replace('/src','')
    db = client.womens_world_cup
    table = db.world_cups
    for i in range(1991, 2020, 4):
        with open(f'{basedir}/data/processed/world_cup{i}.json','r+',errors='ignore') as f:
            wc_obj = json.load(f)
        print(insert_wc_db(table, wc_obj))
mongo()
