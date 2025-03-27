from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")


client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

def get_collection(collection_name: str):
    print(db[collection_name])
    return db[collection_name]

