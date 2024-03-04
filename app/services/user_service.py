from bson import ObjectId, json_util

from settings.db import mongo_db
from settings.utils import MongoDbJSONCoder

from models import User
from enums import SearchUserBy


class UserService:
    async def create_user(self, user_data: User) -> str:
        result = await mongo_db.user.insert_one(user_data.dict())
        print(result)
        return str(user_data.api_key)

    async def get_all_users(self):
        users_cursor = mongo_db.user.find()
        users_json = json_util.dumps(
                await users_cursor.to_list(length=None),
                default=MongoDbJSONCoder.custom_json_decoder
            )
        return MongoDbJSONCoder.custom_json_decoder(users_json)

    async def get_user(self, value: str, by: SearchUserBy):
        query_dict = {"_id": ObjectId(value)} if by == SearchUserBy.user_id else {"api_key": value}

        user_json = json_util.dumps(
                await mongo_db.user.find_one(query_dict),
                default=MongoDbJSONCoder.custom_json_decoder
            )
        return MongoDbJSONCoder.custom_json_decoder(user_json)

    async def update_user(self, user_id: str, user_data: User):
        user_id_obj = ObjectId(user_id)
        result = await mongo_db.user.update_one({"_id": user_id_obj}, {"$set": user_data.dict()})
        if result.modified_count == 1:
            return await self.get_user(user_id)

        return None

    async def delete_user(self, user_id: str):
        user_id_obj = ObjectId(user_id)
        result = await mongo_db.user.delete_one({"_id": user_id_obj})
        return result.deleted_count

    @staticmethod
    async def authenticate_by_api_key(api_key: str):
        print(api_key)
        user_data = await mongo_db.user.find_one({'api_key': api_key})
        print(user_data)
        return user_data is not None
