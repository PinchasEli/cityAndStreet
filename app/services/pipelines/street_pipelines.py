from bson import ObjectId


class StreetPipelines:

    @staticmethod
    def join_with_city(**kwargs):  # street_name: str = None, city_name: str = None):
        pipeline = []
        if kwargs.get('street_name'):
            pipeline.append(
                {
                    "$match": {"name": kwargs.get('street_name')}
                }
            )
        elif kwargs.get('street_id'):
            pipeline.append(
                {
                    "$match": {"_id": ObjectId(kwargs.get('street_id'))}
                }
            )
        # annonate on street collection that convert the id to object from str
        pipeline.append(
            {
                "$addFields": {
                   "city_id": {"$toObjectId": "$city"}
                }
            }
        )
        # build JOIN
        pipeline.append(
            {
                "$lookup": {
                    "from": "city",
                    "localField": "city_id",
                    "foreignField": "_id",
                    "as": "city_info"
                }
            }
        )
        # UNION between collections
        pipeline.append(
            {
                "$unwind": "$city_info"
            }
        )
        # set the columns of the new collection result
        pipeline.append(
            {
                "$project": {
                    "_id": 1,
                    "street_name": "$name",
                    "city_name": "$city_info.name",
                    "city": "$city"
                }
            }
        )
        # print(pipeline)
        return pipeline
