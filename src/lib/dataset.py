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


def breast_cancer_at_a_glance():
    result = json.loads(dataset([
        {"$group": {
            "_id": "$year-of-diagnosis",
            "count": {"$sum": 1}}},
        {"$sort": SON([("_id", 1)])}]))

    return {
        'labels': list(map(lambda x: x['_id'], result)),
        'datasets': [{
            'data': list(map(lambda x: x['count'], result)),
            'label': "Deaths",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def breast_cancer_by_age():
    result = json.loads(dataset([
        {"$group": {
            "_id": "$age-recode-with-1-year-olds",
            "count": {"$sum": 1}}},
        {"$sort": SON([("_id", 1)])}]))

    return {
        'labels': list(map(lambda x: x['_id'], result)),
        'datasets': [{
            'data': list(map(lambda x: x['count'], result)),
            'label': "Deaths",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def get_breast_cancer_by_grade():
    """
    Custom func for cancer_by_grade
    :return:
    """
    r = breast_cancer_by_grade_age_30_40
    j = dataset(r)
    l = json.loads(j)
    # pprint(l)
    res = {'Grade-3': 0}
    for i in l:
        if isinstance(i['_id'], float) and i['_id'] == 1.0:
            res['Grade-1'] = i['count']
        elif isinstance(i['_id'], float) and i['_id'] == 2.0:
            res['Grade-2'] = i['count']
        elif isinstance(i['_id'], float) and i['_id'] == 3.0:
            res['Grade-3'] = i['count']
        elif isinstance(i['_id'], float) and i['_id'] == 4.0:
            res['Grade-3'] = res['Grade-3'] + i['count']
    return json.dumps(res)


def get_breast_cancer_by_size():
    """
    Custom func for cancer_by_size
    :return:
    """
    r = breast_cancer_by_size_age_30_40
    j = dataset(r)
    l = json.loads(j)
    res = {'<1cm': 0}
    for i in l:
        if i['_id'] == '<1cm':
            res['<1cm'] =  res['<1cm'] + i['count']
        elif i['_id'] == '<2cm':
            res['<2cm'] = i['count']
        elif i['_id'] == '<3cm':
            res['<3cm'] = i['count']
        elif i['_id'] == '>3cm':
            res['>3cm'] = i['count']
        elif i['_id'] == '>5cm':
            res['>5cm'] = i['count']
        elif i['_id'] == 'Micro':
            res['<1cm'] = res['<1cm'] + i['count']
    return json.dumps(res)


if __name__ == '__main__':
    breast_cancer_by_state = [{"$group": {
        "_id": "$state",
        "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1), ("_id", -1)])}]

    breast_cancer_at_a_glance = [
        {"$group": {
            "_id": "$year-of-diagnosis",
            "count": {"$sum": 1}}},
        {"$sort": SON([("_id", 1)])}]

    breast_cancer_by_age = [
        {"$group": {
            "_id": "$age-recode-with-1-year-olds",
            "count": {"$sum": 1}}},
        {"$sort": SON([("_id", 1)])}]

    age_30_39_annualy_diagnosed = [
        {"$match": {
            "$or": [
                {"age-recode-with-1-year-olds": "35-39 years"},
                {"age-recode-with-1-year-olds": "30-34 years"}
            ]
        }},
        {"$group": {
            "_id": "$year-of-diagnosis",
            "count": {"$sum": 1}}},
        {"$sort": SON([("_id", 1)])}]

    er_pos_pr_neg_her2_neg_annual_diagnoses = [
        {"$match": {
            "$and": [
                {"er-status-recode-breast-cancer-1990": "+"},
                {"pr-status-recode-breast-cancer-1990": "-"},
                {"derived-her2-recode-2010": "-"}
            ]
        }},
        {"$group": {
            "_id": "$year-of-diagnosis",
            "count": {"$sum": 1}}},
        {"$sort": SON([("_id", 1)])}]



    distribution_of_stage_of_cancer_for_ages_30_40 = [
        {"$match": {
            "$or": [
                {"age-recode-with-1-year-olds": "35-39 years"},
                {"age-recode-with-1-year-olds": "30-34 years"}
            ]
        }},
        {"$group": {
            "_id": "$1998-stage",
            "count": {"$sum": 1}}},
        {"$sort": SON([("_id", 1)])}]

    percent_of_women_with_cancer_by_race = [
        {"$group": {
            "_id": "$race-recode-w-b-ai-api",
            "count": {"$sum": 1},
        }},
        {"$project": {
            "count": 1,
            "percentage": {"$multiply": [{"$divide": [100, 1546698]}, "$count"]}
        }},
        {"$sort": SON([("_id", -1)])}]

    surgery_decisions_within_ages_30_40 = [
        {"$match": {
            "$or": [
                {"age-recode-with-1-year-olds": "35-39 years"},
                {"age-recode-with-1-year-olds": "30-34 years"}
            ]
        }},
        {"$group": {
            "_id": "$surgery",
            "count": {"$sum": 1}}},
        {"$sort": SON([("_id", 1)])}]

    chemotherapy_for_ages_30_40 = [
        {"$match": {
            "$or": [
                {"age-recode-with-1-year-olds": "35-39 years"},
                {"age-recode-with-1-year-olds": "30-34 years"}
            ]
        }},
        {"$group": {
            "_id": "",
            "total": {"$sum": 1},
            "chemo_set": {"$push": "$chemo"}
        }},
        {"$unwind": "$chemo_set"},
        {"$group": {
            "_id": {"chemo": "$chemo_set", "total": "$total"},
            "count": {"$sum": 1}}},
        {"$project": {
            "count": 1,
            "percentage": {"$multiply": [{"$divide": [100, "$_id.total"]}, "$count"], }
        }},
        {"$sort": SON([("_id", 1)])}]

    radiation_for_ages_30_40 = [
        {"$match": {
            "$or": [
                {"age-recode-with-1-year-olds": "35-39 years"},
                {"age-recode-with-1-year-olds": "30-34 years"}
            ]
        }},
        {"$group": {
            "_id": "",
            "total": {"$sum": 1},
            "data_subset": {"$push": "$radiation"}
        }},
        {"$unwind": "$data_subset"},
        {"$group": {
            "_id": {"radiation": "$data_subset", "total": "$total"},
            "count": {"$sum": 1}}},
        {"$project": {
            "count": 1,
            "percentage": {"$multiply": [{"$divide": [100, "$_id.total"]}, "$count"], }
        }},
        {"$sort": SON([("_id", 1)])}]

    survival_months_within_ages_30_40 = [
        {"$match": {
            "$or": [
                {"age-recode-with-1-year-olds": "35-39 years"},
                {"age-recode-with-1-year-olds": "30-34 years"}
            ]
        }},
        {"$group": {
            "_id": "$survival-months",
            "count": {"$sum": 1}}},
        {"$sort": SON([("_id", -1)])}]

    cause_of_death_overall = [
        {"$match": {
            "cod-to-site-recode": {"$nin": ["Alive"]}}
        },
        {"$group": {
            "_id": "",
            "total": {"$sum": 1},
            "data_subset": {"$push": "$cod-to-site-recode"}
        }},
        {"$unwind": "$data_subset"},
        {"$group": {
            "_id": {"cod-to-site-recode": "$data_subset", "total": "$total"},
            "count": {"$sum": 1}}},
        {"$project": {
            "count": 1,
            "percentage": {"$multiply": [{"$divide": [100, "$_id.total"]}, "$count"], }
        }},
        {"$sort": SON([("count", -1)])}]

    cause_of_death_within_ages_30_40 = [
        {"$match": {
            "$and": [{"cod-to-site-recode": {"$nin": ["Alive"]}},
                     {"$or": [
                         {"age-recode-with-1-year-olds": "35-39 years"},
                         {"age-recode-with-1-year-olds": "30-34 years"}
                     ]}]
        }},
        {"$group": {
            "_id": "",
            "total": {"$sum": 1},
            "data_subset": {"$push": "$cod-to-site-recode"}
        }},
        {"$unwind": "$data_subset"},
        {"$group": {
            "_id": {"cod-to-site-recode": "$data_subset", "total": "$total"},
            "count": {"$sum": 1}}},
        {"$project": {
            "count": 1,
            "percentage": {"$multiply": [{"$divide": [100, "$_id.total"]}, "$count"], }
        }},
        {"$sort": SON([("count", -1)])}]

    breast_cancer_by_size_age_30_40 = [
        {"$match": {
            "$or": [
                {"age-recode-with-1-year-olds": "35-39 years"},
                {"age-recode-with-1-year-olds": "30-34 years"}
            ]
        }},
        {"$group": {
            "_id": "$t-size-cm",
            "count": {"$sum": 1}}},
        {"$sort": SON([("_id", 1)])}]

    breast_cancer_by_grade_age_30_40 = [
        {"$match": {
            "$or": [
                {"age-recode-with-1-year-olds": "35-39 years"},
                {"age-recode-with-1-year-olds": "30-34 years"}
            ]
        }},
        {"$group": {
            "_id": "$grade",
            "count": {"$sum": 1}}},
        {"$sort": SON([("_id", 1)])}]

    request = breast_cancer_by_size_age_30_40

    json_output = dataset(request)
    pprint(json_output)

    custom_by_size = get_breast_cancer_by_size()
    pprint(custom_by_size)

    custom_by_grade = get_breast_cancer_by_grade()
    pprint(custom_by_grade)



