"""CraftWoodAIVision Backend — Application Configuration"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings:
    # App
    APP_NAME: str = "CraftWoodAIVision API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    # Database (defaults to local MySQL)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:123456@localhost:3306/craftwood"
    )

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "craftwood-dev-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # CORS
    CORS_ORIGINS: list[str] = ["*"]

    # File upload
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB


settings = Settings()
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
