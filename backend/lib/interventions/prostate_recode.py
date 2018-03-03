import json, os
# import pandas as pd
# from slugify import slugify
from collections import OrderedDict
from pymongo import MongoClient
from bson.son import SON
from pprint import pprint

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'prostate'
COLLECTION_NAME = 'dataset2'

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
        return d
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
    999: None
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


def gleason_recode(document):
    if document['gleason-12'] not in ['Blank(s)', 0, 99, 998, 999, 988]:
        return document['gleason-12']
    if document['gleason-121'] not in ['Blank(s)', 0, 99, 998, 999, 988]:
        return document['gleason-121']
    return None


def gleasoncmb_recode(document):
    if document['gleason-comb'] not in ['Blank(s)', 0, 99, 998, 999, 988]:
        return document['gleason-comb']
    if document['gleason-comb1'] not in ['Blank(s)', 0, 99, 998, 999, 988]:
        return document['gleason-comb1']
    return None


def grade_recode(document):
    if document['grade-1'] == 'Moderately differentiated; Grade II':
        return 2
    if document['grade-1'] == 'Poorly differentiated; Grade III':
        return 3
    if document['grade-1'] == 'Undifferentiated; anaplastic; Grade IV':
        return 4
    if document['grade-1'] == 'Well differentiated; Grade I':
        return 1
    return None


def mstage_recode(document):
    if document['m-stage-1998'] not in ['Blank(s)']:
        return document['m-stage-1998']
    if document['m-stage-2004'] not in ['Blank(s)', None]:
        return document['m-stage-2004']
    if document['m-stage-2010'] not in ['Blank(s)', None]:
        return document['m-stage-2010']
    return None


def nstage_recode(document):
    if document['n-stage-1998'] not in ['Blank(s)']:
        return document['n-stage-1998']
    if document['n-stage-2004'] not in ['Blank(s)', None]:
        return document['n-stage-2004']
    if document['n-stage-2010'] not in ['Blank(s)', None]:
        return document['n-stage-2010']
    return None


def psa_recode(document):
    if document['psa-value-1'] not in ['Blank(s)', 0, 997, 998, 999]:
        return document['psa-value-1']
    return None


def stage_recode(document):
    if document['stage-2004'] not in ['Blank(s)', None, 'UNK Stage']:
        return document['stage-2004']
    if document['stage-2010'] not in ['Blank(s)', None, 'UNK Stage']:
        return document['stage-2010']
    return None


def surgery_recode(document):
    if 'surgery-1988-1997' in document and document['surgery-1988-1997'] not in ['Blank(s)', None]:
        if document['surgery-1988-1997'] < 20:
            return 'No'
        elif document['surgery-1988-1997'] <= 90:
            return 'Yes'
    if 'surgery-code-1998' in document and document['surgery-code-1998'] not in ['Blank(s)', None]:
        if document['surgery-code-1998'] < 20:
            return 'No'
        elif document['surgery-code-1998'] <= 90:
            return 'Yes'


def tstage_recode(document):
    if document['t-stage-1998_'] not in ['Blank(s)']:
        return document['t-stage-1998_']
    if document['t-stage-2004'] not in ['Blank(s)', None]:
        return document['t-stage-2004']
    if document['t-stage-2010'] not in ['Blank(s)', None]:
        return document['t-stage-2010']
    return None


def t_size_recode(document):
    size = document['tumor-size-2004']
    if size not in ['Blank(s)', 999, 888]:
        if size < 990:
            return size
        elif size in [990, 991]:
            return '< 1cm'
        elif size == 992:
            return '< 2cm'
        elif size == 993:
            return '< 3cm'
        elif size == 994:
            return '< 4cm'
        elif size == 995:
            return '< 5cm'
        elif size == 989:
            return '> 5cm'
    return None


def tsize_mm_to_cm(mm):
    if isinstance(mm, int):
        if mm == 0:
            return 0
        elif mm < 20:
            return '< 2cm'
        elif mm < 50:
            return '< 5cm'
        elif 50 <= mm < 888:
            return '> 5cm'
        else:
            return None
    if mm in ['< 1cm', '< 2cm']:
        return '< 2cm'
    elif mm in ['< 3cm', '< 4cm', '< 5cm']:
        return '< 5cm'
    elif mm == '> 5cm':
        return '> 5cm'
    else:
        return None


if __name__ == '__main__':
    # pprint(display_group('race-1'), width=100)
    # pprint(display_group('race-detail'), width=100)
    # pprint(display_group('origin-recode-nhia-hispanic-non-hisp'), width=100)

    # hispanic_filter = {'$and': []}
    # hispanic_filter['$and'].append({"origin-recode-nhia-hispanic-non-hisp": "Spanish-Hispanic-Latino"})
    # count = json.loads(aggregate([
    #     {"$match": hispanic_filter},
    #     {"$group": {
    #         "_id": "",
    #         "count": {"$sum": 1}}},
    #     {"$sort": SON([("_id", 1)])}]))
    # pprint(count)
    #
    exit()

    # test_documents = []
    # for k, v in display_group('grade-1').items():
    #     test_doc = {'grade-1': k}
    #     test_documents.append(test_doc)
    # for k, v in display_group('gleason-comb1').items():
    #     test_doc = {'gleason-comb': None, 'gleason-comb1': k}
    #     test_documents.append(test_doc)
    # for d in test_documents:
    # pprint(d)
    # d['grade'] = grade_recode(d)
    # if d['grade'] is None:
    #     print(k, d['grade'])

    # display_group('surgery')
    exit()

    # i = 0
    i = 0
    for document in collection.find():
        # print(document['_id'])

        if 'origin-recode-nhia-hispanic-non-hisp' in document and document[
            'origin-recode-nhia-hispanic-non-hisp'] == 'Spanish-Hispanic-Latino':
            if document['race'] in ['White', 'Unknown']:
                document['race'] = 'Hispanic'
            if document['race-detail'] in ['White', 'Unknown']:
                document['race-detail'] = 'Hispanic'
            if document['raceethnicity'] in ['White', 'Unknown']:
                document['raceethnicity'] = 'Hispanic'
            print(document['race'], document['race-detail'])

        # pprint(document)

        # print(document['gleason-12'], document['gleason-121'])
        document['gleason'] = gleason_recode(document)
        # print(document['gleason'])

        # print(document['gleason-comb'], document['gleason-comb1'])
        document['gleason-comb-recode'] = gleasoncmb_recode(document)
        # print(document['gleason-comb-recode'])

        # print(document['grade-1'])
        document['grade'] = grade_recode(document)
        # print(document['grade'])

        # print(document['m-stage-1998'], document['m-stage-2004'], document['m-stage-2010'])
        document['m-stage'] = mstage_recode(document)
        # print(document['m-stage'])

        # print(document['n-stage-1998'], document['n-stage-2004'], document['n-stage-2010'])
        document['n-stage'] = nstage_recode(document)
        # print(document['n-stage'])

        # print(document['psa-value-1'])
        document['psa-value'] = psa_recode(document)
        # print(document['psa-value'])

        # print(document['stage-2004'], document['stage-2010'])
        document['stage'] = stage_recode(document)
        # print(document['stage'])

        # print(document['surgery-1988-1997']) if 'surgery-1988-1997' in document else None
        # print(document['surgery-code-1998']) if 'surgery-code-1998' in document else None
        document['surgery'] = surgery_recode(document)
        # print(document['surgery'])

        # print(document['t-stage-1998']) if 't-stage-1998' in document else None
        # print(document['t-stage-2004']) if 't-stage-2004' in document else None
        # print(document['t-stage-2010']) if 't-stage-2010' in document else None
        # print(document['t-stage-1998'], document['t-stage-2004'], document['t-stage-2010'])
        document['t-stage'] = tstage_recode(document)
        # print(document['t-stage'])

        # print(document['tumor-size-2004'])
        document['t-size-mm'] = t_size_recode(document)
        document['t-size-cm'] = tsize_mm_to_cm(document['t-size-mm'])
        # print(document['t-size-mm'], document['t-size-cm'])

        i += 1
        # collection.update_one({'_id': document['_id']}, {"$set": document}, upsert=False)
        print(i, '/ 1212874  ')
    print('ALL DONE.')
    exit()

