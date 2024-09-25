from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int

    gemini_api_keys: list[str]

    redis_host: str
    redis_port: int
    redis_db: int
    redis_ttl: int

    minio_url: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket: str

    mongodb_url: str
    mongodb_db: str

    class Config:
        env_file = ".env"

settings = Settings()
