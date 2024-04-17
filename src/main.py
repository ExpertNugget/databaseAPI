from fastapi import FastAPI
from config import *
import firebase_admin, json
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter

app = FastAPI()

cred = credentials.Certificate(firebaseKey)
fbapp = firebase_admin.initialize_app(cred)

db = firestore.client()


def set_user_discord(userId: str, points: str = "0"):
    new_user_ref = db.collection("users").document()
    new_user_ref.set(
        {
            "discordIds": [userId],
            "points": points,
            "accountCreationDate": firestore.SERVER_TIMESTAMP,
        }
    )


def set_user_twitch(userId: str, points: str = "0"):
    new_user_ref = db.collection("users").document()
    new_user_ref.set(
        {
            "twitchIds": [userId],
            "points": points,
            "accountCreationDate": firestore.SERVER_TIMESTAMP,
        }
    )


def set_user_youtube(userId: str, points: str = "0"):
    new_user_ref = db.collection("users").document()
    new_user_ref.set(
        {
            "youtubeIds": [userId],
            "points": points,
            "accountCreationDate": firestore.SERVER_TIMESTAMP,
        }
    )


@app.post("/add-points/discord/{userId}/{points}")
async def add_points_discord(userId: str, points: str):
    print(f"Adding {points} points to {userId}")
    query = (
        db.collection("users")
        .where(filter=FieldFilter("discordIds", "array_contains", userId))
        .limit(1)
    )
    docs = query.get()
    if not docs:
        set_user_discord(userId, points)
        return
    for doc in docs:
        data = doc.to_dict()
    dbpoints = int(data["points"])
    dbpoints += int(points)
    data["points"] = str(dbpoints)
    db.collection("users").document(doc.id).update({"points": data["points"]})
    return data


@app.post("/add-points/twitch/{userId}/{points}")
async def add_points_twitch(userId: str, points: str):
    print(f"Adding {points} points to {userId}")
    query = (
        db.collection("users")
        .where(filter=FieldFilter("twitchIds", "array_contains", userId))
        .limit(1)
    )
    docs = query.get()
    if not docs:
        set_user_twitch(userId, points)
        return
    for doc in docs:
        data = doc.to_dict()
    dbpoints = int(data["points"])
    dbpoints += int(points)
    data["points"] = str(dbpoints)
    db.collection("users").document(doc.id).update({"points": data["points"]})
    return data


@app.post("/add-points/youtube/{userId}/{points}")
async def add_points_youtube(userId: str, points: str):
    print(f"Adding {points} points to {userId}")
    query = (
        db.collection("users")
        .where(filter=FieldFilter("youtubeIds", "array_contains", userId))
        .limit(1)
    )
    docs = query.get()
    if not docs:
        set_user_youtube(userId, points)
        return
    for doc in docs:
        data = doc.to_dict()
    dbpoints = int(data["points"])
    dbpoints += int(points)
    data["points"] = str(dbpoints)
    db.collection("users").document(doc.id).update({"points": data["points"]})
    return data
