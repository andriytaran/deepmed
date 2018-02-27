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

mongo_client = MongoClient(MONGODB_HOST, MONGODB_PORT)
collection = mongo_client[DBS_NAME][COLLECTION_NAME]

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
    888: "N/A",
    990: "< 1cm",
    991: "< 1cm",
    992: "< 2cm",
    993: "< 3cm",
    994: "< 5cm",
    995: "> 5cm",
    996: "N/A",
    997: "N/A",
    998: "N/A",
    999: "N/A",
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


def mm_to_cm(mm):
    if 1 <= mm < 10:
        return '< 1cm'
    elif 11 <= mm < 20:
        return '< 2cm'
    elif 21 <= mm < 30:
        return '< 3cm'
    elif 31 <= mm < 50:
        return '< 5cm'
    elif 51 <= mm < 888:
        return '> 5cm'
    else:
        return None


def recode_t_size(document):
    if isinstance(document['t-size-mm-2004'], int):
        if document['t-size-mm-2004'] not in [888, 990, 991, 992, 993, 994, 995, 996, 997, 998, 999]:
            t_size_mm = document['t-size-mm-2004']
            return mm_to_cm(t_size_mm)
        elif document['t-size-mm-2004'] in [990, 991, 992, 993, 994, 995]:
            return t_size_2004[document['t-size-mm-2004']]
    tlist = document['t-size-mm-1988'].split()
    try:
        t_size_mm = int(tlist[0])
        return mm_to_cm(t_size_mm)
    except:
        pass
    if tlist[0] in t_size_1988 and t_size_1988[tlist[0]] == "Micro":
        return "< 1cm"


if __name__ == '__main__':
    display_group('t-size-mm-2004')
    display_group('t-size-mm-1988')
    exit()

    for document in collection.find():
        print(document['t-size-mm-1988'], document['t-size-mm-2004'], recode_t_size(document))
