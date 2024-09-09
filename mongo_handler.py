from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME
from pymongo.server_api import ServerApi
class MongoHandler:
    def __init__(self):
        self.client = MongoClient(MONGO_URI,server_api=ServerApi('1'))
        self.db = self.client[MONGO_DB_NAME]
        self.collection = self.db[MONGO_COLLECTION_NAME]

    def insert_deposit(self, deposit):
        self.collection.insert_one(deposit)

    def get_all_deposits(self):
        return list(self.collection.find())
