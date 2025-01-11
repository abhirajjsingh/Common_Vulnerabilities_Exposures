from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings
import logging

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    db = None
    cve_collection = None

    async def connect_to_mongodb(self):
        try:
            self.client = AsyncIOMotorClient(settings.MONGODB_URL)
            self.db = self.client[settings.DATABASE_NAME]
            self.cve_collection = self.db[settings.COLLECTION_NAME]
            
            # Create indexes
            await self.cve_collection.create_index("cve_id", unique=True)
            await self.cve_collection.create_index("published_date")
            await self.cve_collection.create_index("last_modified_date")
            
            logger.info("Connected to MongoDB successfully")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    async def close_mongodb_connection(self):
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

db = Database()