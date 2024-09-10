from pymongo import MongoClient, errors
from config import MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME
from logger import logger
class MongoHandler:
    def __init__(self):
        try:
            self.client = MongoClient(MONGO_URI)
            self.db = self.client[MONGO_DB_NAME]
            self.collection = self.db[MONGO_COLLECTION_NAME]
        except errors.ConnectionError as e:
            logger.error(f"Error connecting to MongoDB: {e}")
        except Exception as e:
            logger.error(f"Unexpected error with MongoDB: {e}")


    def insert_deposit(self, deposit):
        try:
            self.collection.insert_one(deposit)
        except errors.PyMongoError as e:
            logger.error(f"Error inserting deposit into MongoDB: {e}")
        except Exception as e:
            logger.error(f"Unexpected error inserting deposit: {e}")

    def get_all_deposits(self):
        return list(self.collection.find())
