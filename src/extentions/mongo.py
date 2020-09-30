from motor.motor_asyncio import AsyncIOMotorClient
from umongo import MotorAsyncIOInstance


instance = MotorAsyncIOInstance()


async def init_mongo(app):
    conn = AsyncIOMotorClient(app.config.MONGO_URI)
    db = conn[app.config.MONGO_DBNAME]
    instance.init(db)

    async def close_mongo(app):
        db.client.close()

    app.on_cleanup.append(close_mongo)
    app.db = db