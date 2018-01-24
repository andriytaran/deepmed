import json
from pymongo import MongoClient
from bson.son import SON
from pprint import pprint

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'bcancer'
COLLECTION_NAME = 'dataset'


def dataset(request):
    mongo_client = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = mongo_client[DBS_NAME][COLLECTION_NAME]
    response = []
    data = collection.aggregate(request)
    for row in data:
        response.append(row)
    mongo_client.close()
    return json.dumps(response)


if __name__ == '__main__':
    request = [{"$group": {
        "_id": "$state",
        "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1), ("_id", -1)])}]

    json_output = dataset(request)
    pprint(json_output)
