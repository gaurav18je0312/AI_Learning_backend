from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError
from fastapi import HTTPException
from app.core.config import settings
from bson import ObjectId
import zlib
import pickle


MONGO_URI = settings.mongodb_url 
client = AsyncIOMotorClient(MONGO_URI)

db = client[settings.mongodb_db]

async def check_mongo_connection():
    try:
        await client.admin.command('ping')
    except ServerSelectionTimeoutError:
        raise HTTPException(status_code=500, detail="MongoDB connection failed.")

async def create_object(collection_name, data):
    result = await db[collection_name].insert_one(data)
    return str(result.inserted_id)

async def get_object(collection_name, object_name):
    data = await db[collection_name].find_one({"_id": ObjectId(object_name)})
    if data is not None:
        data["id"] = str(data["_id"])
        data.pop("_id", None)
    return data

async def update_object(collection_name, object_name, data):
    result = await db[collection_name].update_one({"_id": ObjectId(object_name)}, {"$set": data})
    if result.modified_count == 0:
        return None
    data["id"] = object_name
    return data

async def delete_object(collection_name, object_name):
    result = await db[collection_name].delete_one({"_id": ObjectId(object_name)})
    if result.deleted_count == 0:
        return None
    return object_name

async def find_object(collection_name, data):
    data = await db[collection_name].find_one(data)
    if data is not None:
        data["id"] = str(data["_id"])
        data.pop("_id", None)
    return data

async def get_chat(id):
    data = await db["chat"].find_one({"_id": ObjectId(id)})
    if data is not None:
        chat = zlib.decompress(data["chat"])
        return pickle.loads(chat)
    return None

async def update_chat(id, chat):
    pickled_json = pickle.dumps(chat)
    compressed_json = zlib.compress(pickled_json)
    result = await db["chat"].update_one({"_id": ObjectId(id)}, {"$set": {"chat": compressed_json}})
    if result.modified_count == 0:
        return None
    return id

async def create_chat(chat):
    pickled_json = pickle.dumps(chat)
    compressed_json = zlib.compress(pickled_json)
    result = await db["chat"].insert_one({"chat": compressed_json})
    return str(result.inserted_id)