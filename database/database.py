#(©)noorxd786

import pymongo, os
from pymongo import MongoClient

DB_URI = os.getenv("DB_URI")

# Temporary Debug — Add this
if not DB_URI:
    raise ValueError("DB_URI is empty or not set!")

dbclient = MongoClient(DB_URI)
from config import DB_URI, DB_NAME

dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]
user_data = database['users']


async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
        
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return
