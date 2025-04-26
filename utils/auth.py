# utils/auth.py

import pymongo
import bcrypt
import os

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://adminUser:drowsy-ankit@droswy-cluster.yozjvoc.mongodb.net/?retryWrites=true&w=majority&appName=droswy-cluster")
client = pymongo.MongoClient(MONGO_URI)
db = client["drowsyme"]
users_collection = db["users"]

def register_user(username, password, user_type):
    existing_user = users_collection.find_one({"username": username})
    if existing_user:
        return False, "Username already exists."

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users_collection.insert_one({
        "username": username,
        "password": hashed_pw,
        "user_type": user_type
    })
    return True, "User registered successfully."

def authenticate_user(username, password, user_type):
    user = users_collection.find_one({"username": username, "user_type": user_type})
    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        return True
    else:
        return False
