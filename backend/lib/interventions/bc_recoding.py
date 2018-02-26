import json, os
import pandas as pd
from slugify import slugify
from collections import OrderedDict
from pymongo import MongoClient
from bson.son import SON
from pprint import pprint

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'bcancer'
COLLECTION_NAME = 'dataset3'


def aggregate(request):
    mongo_client = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = mongo_client[DBS_NAME][COLLECTION_NAME]
    response = []
    data = collection.aggregate(request)
    for row in data:
        response.append(row)
    mongo_client.close()
    return json.dumps(response)


def find(request, **kwargs):
    mongo_client = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = mongo_client[DBS_NAME][COLLECTION_NAME]
    response = []
    data = collection.find(request, **kwargs)
    for row in data:
        response.append(row)
    mongo_client.close()
    return response


def display_group(group):
    if group:
        group = '$' + str(group)
        result = json.loads(aggregate([
            {"$group": {
                "_id": group,
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}]))
        d = {}
        for i in result:
            d[i['_id']] = i['count']
        pprint(d)
    return None


t_size_2004 = {
    "888": "N/A",
    "990": "Micro",
    "991": "<1cm",
    "992": "<2cm",
    "993": "<3cm",
    "994": ">3cm",
    "995": ">5cm",
    "996": "N/A",
    "997": "N/A",
    "998": "N/A",
    "999": "N/A",
}

t_size_1988 = {
    "Diffuse": "Micro",
    "Less than or equal to 3mm (0.3 cm)": "Micro",
    "Mammo/xerography dx with no size given": "N/A",
    "Microscopic focus of foci only": "Micro",
    "No primary tumor found, no pagets disease": "N/A",
    "Paget disease of nipple with no demonstrable tumor": "N/A",
    "Unknown": "N/A",
    "Values Under Review": "N/A",
    "[OTHER]": "N/A"
}

if __name__ == '__main__':
    display_group('t-size-mm-1988')
