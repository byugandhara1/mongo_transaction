import logging
import motor.motor_asyncio
LOGGER = logging.getLogger(__name__)


async def get_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        "mongodb://localhost:27017/test123", serverSelectionTimeoutMS=5000)
    try:
        db = client.template_api
        yield db
    finally:
        client.close()

# mongodb://{0}:{1}@template_engine_api_db:27017/{2}?authSource=admin&socketTimeoutMS=60000
