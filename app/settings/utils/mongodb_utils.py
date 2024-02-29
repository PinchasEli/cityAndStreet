import json

from bson import ObjectId, json_util


class MongoDbJSONCoder:

    @classmethod
    def custom_json_encoder(cls, obj):
        if isinstance(obj, ObjectId):
            return str(obj)

        return json_util.default(obj)

    @classmethod
    def custom_json_decoder(cls, json_data):
        def hook(dct):
            for key, value in dct.items():
                if key == "_id" and isinstance(value, str):
                    dct[key] = ObjectId(value)

            return dct

        return json.loads(json_data, object_hook=hook)
