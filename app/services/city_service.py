from bson import ObjectId, json_util

from settings.db import mongo_db
from settings.utils import MongoDbJSONCoder

from models import City


class CityService:
    async def create_city(self, city_data: City) -> str:
        result = await mongo_db.city.insert_one(city_data.dict())
        return str(result.inserted_id)

    async def get_all_cities(self):
        cities_cursor = mongo_db.city.find()
        cities_json = json_util.dumps(
                await cities_cursor.to_list(length=None),
                default=MongoDbJSONCoder.custom_json_decoder
            )
        return MongoDbJSONCoder.custom_json_decoder(cities_json)

    async def get_city(self, city_id: str):
        city_json = json_util.dumps(
                await mongo_db.city.find_one({"_id": ObjectId(city_id)}),
                default=MongoDbJSONCoder.custom_json_decoder
            )
        return MongoDbJSONCoder.custom_json_decoder(city_json)

    async def update_city(self, city_id: str, city_data: City):
        city_id_obj = ObjectId(city_id)
        result = await mongo_db.city.update_one({"_id": city_id_obj}, {"$set": city_data.dict()})
        if result.modified_count == 1:
            return await self.get_city(city_id)

        return None

    async def delete_city(self, city_id: str):
        city_id_obj = ObjectId(city_id)
        result = await mongo_db.city.delete_one({"_id": city_id_obj})
        return result.deleted_count
