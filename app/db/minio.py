from minio import Minio
from app.core.config import settings
import os

minio_client = None

minio_bucket = settings.minio_bucket

async def connect_minio():
    global minio_client
    minio_client = Minio(
        settings.minio_url,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=False
        )
    if not minio_client.bucket_exists(minio_bucket):
        minio_client.make_bucket(minio_bucket)

async def upload_default_book_to_minio(file_path, file_name, subject_name):
    try:
        object_name = f"books/{subject_name}/{file_name}"
        minio_client.fput_object(minio_bucket, object_name, file_path, content_type="application/pdf")
        return object_name
    except Exception as e:
        print(f"Error uploading file to MinIO: {e}")
        return None

async def upload_user_book_to_minio(file_path, file_name, user_id):
    try:
        object_name = f"users/{user_id}/books/{file_name}"
        minio_client.fput_object(minio_bucket, object_name, file_path, content_type="application/pdf")
        os.remove(file_path)
        return object_name
    except Exception as e:
        print(f"Error uploading file to MinIO: {e}")
        return None

async def upload_user_chat_image_to_minio(file_path, file_name, user_id, chat_id):
    try:
        object_name = f"users/{user_id}/images/{chat_id}/{file_name}"
        minio_client.fput_object(minio_bucket, object_name, file_path, content_type="image/jpeg")
        os.remove(file_path)
        return object_name
    except Exception as e:
        print(f"Error uploading file to MinIO: {e}")
        return None

async def get_url_from_minio(object_name):
    try:
        url = minio_client.presigned_get_object(minio_bucket, object_name)
        return url
    except Exception as e:
        print(f"Error getting URL from MinIO: {e}")
        return False
