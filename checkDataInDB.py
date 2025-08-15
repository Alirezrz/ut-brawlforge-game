from pymongo import MongoClient
MONGO_URI = "mongodb+srv://admin:%40Rman123@cluster0.hrgfoi9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
db = MongoClient(MONGO_URI)["my_game_db"]




collections = db.list_collection_names()
print("Collections:", collections)

for collection_name in collections:
    print(f"\n--- Collection: {collection_name} ---")
    for doc in db[collection_name].find():
        print(doc)