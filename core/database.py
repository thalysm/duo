from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "duo")

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

def get_collection(collection_name: str):
    print(db[collection_name])
    return db[collection_name]
