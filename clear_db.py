from pymongo import MongoClient
MONGO_URI = "mongodb+srv://admin:%40Rman123@cluster0.hrgfoi9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
db = MongoClient(MONGO_URI)["my_game_db"]



for collection_name in db.list_collection_names():
    db[collection_name].delete_many({})
    print(f"Collection '{collection_name}' cleared.")