import motor.motor_asyncio
from config import DB_NAME, DB_URL

class Database:
    
    default_verify = {
        'is_verified': False,
        'name': None,
        'username': None,
        'phone': None,
        'bikash': None,
        'nogod': None,
        'photo': None,
        'video': None,
        'nid_document': None,
        'passport_document': None,
        'jonmo_nibondon_document': None,
        'address': None
    }   

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.user

    def new_user(self, id):
        return {
            '_id': int(id),                                   
            'verify_status': self.default_verify
        }                

    async def add_user(self, id, user_data):
        user_data['_id'] = int(id)
        await self.col.insert_one(user_data)

    async def get_user(self, id):
        return await self.col.find_one({'_id': int(id)})

    async def update_user(self, id, update_data):
        await self.col.update_one({'_id': int(id)}, {'$set': update_data})

    async def delete_user(self, id):
        await self.col.delete_one({'_id': int(id)})

    async def is_user_verified(self, id):
        user = await self.col.find_one({'_id': int(id)})
        if user:
            return user['verify_status']['is_verified']
        return False

    async def set_user_verification_status(self, id, status):
        await self.col.update_one({'_id': int(id)}, {'$set': {'verify_status.is_verified': status}})

    async def total_users_count(self):
        return await self.col.count_documents({})

    async def get_all_users(self):
        return self.col.find({})

# Usage:
# db = Database(Config.DB_URL, Config.DB_NAME)
# await db.add_user(id, user_data)
# user = await db.get_user(id)
# await db.update_user(id, update_data)
# await db.delete_user(id)
# verified = await db.is_user_verified(id)
# await db.set_user_verification_status(id, True)
# count = await db.total_users_count()
# all_users = await db.get_all_users()


db = Database(DB_URL,DB_NAME)




