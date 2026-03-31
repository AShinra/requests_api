import os
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

app = FastAPI()


# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["requestdb"]
collection = db["users"]

class User(BaseModel):
    name: str
    username: str

@app.get("/")
def home():
    return {"status": "API is running"}

# @app.post("/users")
# def create_user(user: User):
#     result = collection.insert_one(user.model_dump())
#     return {
#         "message": "User created",
#         "id": str(result.inserted_id)
#     }

@app.get("/users")
def get_users():
    users = []
    for user in collection.find():
        user["_id"] = str(user["_id"])
        user['name'] = str(user["name"])
        users.append(user)
    return users

@app.get("/tickets")
def get_tickets():
    tickets = []
    for ticket in collection.find():
        ticket["_id"] = str(ticket["_id"])
        ticket['leave_credits'] = str(ticket["leave_credits"])
        tickets.append(ticket)
    return tickets

@app.get("/users/{name}")
def get_user(name: str):
    user = collection.find_one({"name": name})

    if not user:
        raise HTTPException(status_code=404, detail="No such user")

    user["_id"] = str(user["_id"])
    return user