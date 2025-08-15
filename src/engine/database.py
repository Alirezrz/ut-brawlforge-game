import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI")) 
db = client["my_game_db"]  
users_collection = db["users"]  

def get_user_info(username):
    return users_collection.find_one({"username": username})
