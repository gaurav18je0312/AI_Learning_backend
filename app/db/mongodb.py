from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError
from fastapi import HTTPException
from app.core.config import settings
from bson import ObjectId


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
        data["_id"] = str(data["_id"])
    return data

async def update_object(collection_name, object_name, data):
    result = await db[collection_name].update_one({"_id": ObjectId(object_name)}, {"$set": data})
    if result.modified_count == 0:
        return None
    data["_id"] = object_name
    return data

async def delete_object(collection_name, object_name):
    result = await db[collection_name].delete_one({"_id": ObjectId(object_name)})
    if result.deleted_count == 0:
        return None
    return object_name