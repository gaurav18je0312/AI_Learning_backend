from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import router
from app.db.mongodb import check_mongo_connection, db
from app.db.minio import connect_minio
from app.db.redis import connect_redis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

app.include_router(router.api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_db_client():
    await check_mongo_connection()
    await connect_minio()
    await connect_redis()

@app.on_event("shutdown")
async def shutdown_db_client():
    db.client.close()