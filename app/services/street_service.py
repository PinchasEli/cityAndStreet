from bson import ObjectId, json_util

from settings.db import mongo_db
from settings.utils import MongoDbJSONCoder

from models import Street
from services.pipelines import StreetPipelines


class StreetService:
    async def create_street(self, street: Street):
        city = await mongo_db.city.find_one({"_id": ObjectId(street.city)})
        if not city:
            return None

        await mongo_db.street.insert_one(street.dict())
        return street

    async def get_all_streets(self):
        try:
            pipeline = StreetPipelines.join_with_city()
            street_json = json_util.dumps(
                await mongo_db.street.aggregate(pipeline).to_list(length=None),
                default=MongoDbJSONCoder.custom_json_decoder
            )
            return MongoDbJSONCoder.custom_json_decoder(street_json)
        except StopAsyncIteration:
            return None

    async def get_street(self, street_name: str):
        try:
            pipeline = StreetPipelines.join_with_city(street_name=street_name)
            street_json = json_util.dumps(
                await mongo_db.street.aggregate(pipeline).next(),
                default=MongoDbJSONCoder.custom_json_decoder
            )
            return MongoDbJSONCoder.custom_json_decoder(street_json)
        except StopAsyncIteration:
            return None

    async def update_street(self, street_id: str, street_data: Street):
        try:
            street_id_obj = ObjectId(street_id)
            result = await mongo_db.street.update_one({"_id": street_id_obj}, {"$set": street_data.dict()})
            if result.modified_count == 1:
                pipeline = StreetPipelines.join_with_city(street_id=street_id)
                street_json = json_util.dumps(
                    await mongo_db.street.aggregate(pipeline).next(),
                    default=MongoDbJSONCoder.custom_json_decoder
                )
                return MongoDbJSONCoder.custom_json_decoder(street_json)

            return None
        except Exception as e:
            return None

    async def delete_street(self, street_id: str):
        street_id_obj = ObjectId(street_id)
        result = await mongo_db.street.delete_one({"_id": street_id_obj})
        return result.deleted_count
