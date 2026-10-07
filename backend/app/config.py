from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str = "postgresql://app:app@postgres:5432/meshes"
    REDIS_URL: str = "redis://redis:6379/0"
    CELERY_BROKER_URL: str = "redis://redis:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/2"
    S3_ENDPOINT: str = "http://minio:9000"
    S3_ACCESS_KEY: str = "minio"
    S3_SECRET_KEY: str = "minio123"
    S3_BUCKET: str = "meshes"
    STORAGE_BACKEND: str = "s3"
    LOCAL_STORAGE_ROOT: str = "./data/objects"
    MAX_VRAM_GB: float = 8.0
    RATE_LIMIT_PER_HOUR: int = 20

    class Config:
        env_file = ".env"

settings = Settings()