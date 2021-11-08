from pymongo import MongoClient


# id copa do mundo - > ano


def insert_wc_db(collection, object):

    try:
        post_id = collection.insert_one(object, ).inserted_id
    except Exception as e:
        raise e


def create_table(client):
    db = client.womansworldcup
    table = db.wc
    try:
        result = db.table.create_index(
            [('world_cup_id', pymongo.ASCENDING)], unique=True)
    except Exception as e:
        raise e


def main():

    try:
        client = MongoClient('mongodb://localhost:27017/')

    except Exception as e:
        raise e

    wcs = []

    for wc in wcs:
        insert_wc_db(table, wc)


main()
