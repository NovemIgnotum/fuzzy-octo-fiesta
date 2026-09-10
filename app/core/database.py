from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import get_settings
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class Database:
    client: Optional[AsyncIOMotorClient] = None
    database: Optional[AsyncIOMotorDatabase] = None

db = Database()

async def connect_to_mongodb() -> None:
    settings = get_settings()

    logger.info("Connexion à MongoDB...")
    db.client = AsyncIOMotorClient(
        settings.mongodb_url,
        minPoolSize=settings.mongodb_min_pool_size,
        maxPoolSize=settings.mongodb_max_pool_size,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=10000,
        socketTimeoutMS=10000
    )

    db.database = db.client[settings.mongodb_database]

    try:
        await db.client.admin.command("ping")
        logger.info("Connection to database successful")
    except Exception as e:
        logger.error(f"Error while connecting to database: {str(e)}")
        raise

async def close_mongodb_connection() -> None:
    if db.client:
        logger.info("Closing connection to database")
        db.client.close()
        db.client = None
        db.database = None

def get_database() -> AsyncIOMotorDatabase:
    if db.database is None:
        raise RuntimeError("Database connection not established")
    return db.database

    