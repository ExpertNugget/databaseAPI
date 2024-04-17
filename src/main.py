from fastapi import FastAPI
from config import *
import firebase_admin, json
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter

app = FastAPI()

cred = credentials.Certificate(firebaseKey)
fbapp = firebase_admin.initialize_app(cred)

db = firestore.client()


def set_user(userId: str, points: str):
    new_user_ref = db.collection("users").document()
    new_user_ref.set(
        {
            "discordIds": [userId],
            "points": points,
            "accountCreationDate": firestore.SERVER_TIMESTAMP,
        }
    )


@app.post("/add-points/discord/{userId}/{points}")
async def add_points(userId: str, points: str):
    print(f"Adding {points} points to {userId}")
    query = (
        db.collection("users")
        .where(filter=FieldFilter("discordIds", "array_contains", userId))
        .limit(1)
    )
    docs = query.get()
    if not docs:
        set_user(userId, points)
        return
    for doc in docs:
        data = doc.to_dict()
    dbpoints = int(data["points"])
    dbpoints += int(points)
    data["points"] = str(dbpoints)
    db.collection("users").document(doc.id).update({"points": data["points"]})
    return data
