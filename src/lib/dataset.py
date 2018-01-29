import json
from pymongo import MongoClient
from bson.son import SON
from pprint import pprint

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'bcancer'
COLLECTION_NAME = 'dataset'

STATES_NAME_ABRS = {
    "Alabama": "AL",
    "Alaska": "AK",
    "American Samoa": "AS",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "District Of Columbia": "DC",
    "Federated States Of Micronesia": "FM",
    "Florida": "FL",
    "Georgia": "GA",
    "Guam": "GU",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Marshall Islands": "MH",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Northern Mariana Islands": "MP",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Palau": "PW",
    "Pennsylvania": "PA",
    "Puerto Rico": "PR",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virgin Islands": "VI",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY"
}

STATES_ABRS = ["AL", "AK", "AS", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FM", "FL", "GA", "GU", "HI", "ID", "IL",
               "IN",
               "IA", "KS", "KY", "LA", "ME", "MH", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
               "NM",
               "NY", "NC", "ND", "MP", "OH", "OK", "OR", "PW", "PA", "PR", "RI", "SC", "SD", "TN", "TX", "UT", "VT",
               "VI",
               "VA", "WA", "WV", "WI", "WY"]


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


def breast_cancer_at_a_glance():
    result = json.loads(aggregate([
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
    result = json.loads(aggregate([
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


def breast_cancer_by_state():
    result = json.loads(aggregate([{"$group": {
        "_id": "$state",
        "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1), ("_id", -1)])}]))

    values = {}
    for state in STATES_ABRS:
        match = filter(lambda x: STATES_NAME_ABRS[x['_id']] in STATES_ABRS, result)
        if match.count() > 0:
            values["US-" + state] = match[0]['count']
        else:
            values["US-" + state] = 0

    pprint(values)

    return {
        'regions': [{
            'scale': ['#47cfd1', '#48ccf5', '#88d0d1', '#b8e8f5'],
            'attribute': 'fill',
            'values': values
        }]
    }


def breast_cancer_by_grade_age_30_40():
    j = aggregate([{"$match": {
        "$or": [
            {"age-recode-with-1-year-olds": "35-39 years"},
            {"age-recode-with-1-year-olds": "30-34 years"}
        ]
    }},
        {"$group": {
            "_id": "$grade",
            "count": {"$sum": 1}}},
        {"$sort": SON([("_id", 1)])}])
    res = {'Grade 3': 0}
    for i in json.loads(j):
        if isinstance(i['_id'], float) and i['_id'] == 1.0:
            res['Grade 1'] = i['count']
        elif isinstance(i['_id'], float) and i['_id'] == 2.0:
            res['Grade 2'] = i['count']
        elif isinstance(i['_id'], float) and i['_id'] == 3.0:
            res['Grade 3'] = i['count']
        elif isinstance(i['_id'], float) and i['_id'] == 4.0:
            res['Grade 3'] += i['count']

    return {
        'labels': list(map(lambda x: x, res.keys())),
        'datasets': [{
            'data': list(map(lambda x: x, res.values())),
            'label': "Diagnosed",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def breast_cancer_by_size_age_30_40():
    """
    Custom func for cancer_by_size
    :return:
    """
    j = aggregate([{"$match": {
        "$or": [
            {"age-recode-with-1-year-olds": "35-39 years"},
            {"age-recode-with-1-year-olds": "30-34 years"}
        ]
    }},
        {"$group": {
            "_id": "$t-size-cm",
            "count": {"$sum": 1}}},
        {"$sort": SON([("_id", 1)])}])
    l = json.loads(j)
    res = {'< 1cm': 0}
    for i in l:
        if i['_id'] == '<1cm':
            res['< 1cm'] += i['count']
        elif i['_id'] == '<2cm':
            res['< 2cm'] = i['count']
        elif i['_id'] == '<3cm':
            res['< 3cm'] = i['count']
        elif i['_id'] == '>3cm':
            res['> 3cm'] = i['count']
        elif i['_id'] == '>5cm':
            res['> 5cm'] = i['count']
        elif i['_id'] == 'Micro':
            res['< 1cm'] += i['count']

    return {
        'labels': list(map(lambda x: x, res.keys())),
        'datasets': [{
            'data': list(map(lambda x: x, res.values())),
            'label': "Diagnosed",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def woman_age_30_40_annualy_diagnosed():
    result = json.loads(aggregate([{"$match": {
        "$or": [
            {"age-recode-with-1-year-olds": "35-39 years"},
            {"age-recode-with-1-year-olds": "30-34 years"}
        ]
    }},
        {"$group": {
            "_id": "$year-of-diagnosis",
            "count": {"$sum": 1}}},
        {"$sort": SON([("_id", 1)])}]))

    return {
        'labels': list(map(lambda x: x['_id'], result)),
        'datasets': [{
            'data': list(map(lambda x: x['count'], result)),
            'label': "Diagnosed",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def er_pos_pr_neg_her2_neg_annual_diagnoses():
    result = json.loads(aggregate([{"$match": {
        "$and": [
            {"er-status-recode-breast-cancer-1990": "+"},
            {"pr-status-recode-breast-cancer-1990": "-"},
            {"derived-her2-recode-2010": "-"}
        ]
    }},
        {"$group": {
            "_id": "$year-of-diagnosis",
            "count": {"$sum": 1}}},
        {"$sort": SON([("_id", 1)])}]))

    return {
        'labels': list(map(lambda x: x['_id'], result)),
        'datasets': [{
            'data': list(map(lambda x: x['count'], result)),
            'label': "Diagnosed",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def distribution_of_stage_of_cancer_for_ages_30_40():
    result = json.loads(aggregate([{"$match": {
        "$or": [
            {"age-recode-with-1-year-olds": "35-39 years"},
            {"age-recode-with-1-year-olds": "30-34 years"}
        ]
    }},
        {"$group": {
            "_id": "$1998-stage",
            "count": {"$sum": 1}}},
        {"$sort": SON([("_id", 1)])}]))

    return {
        'labels': list(map(lambda x: x['_id'], result)),
        'datasets': [{
            'data': list(map(lambda x: x['count'], result)),
            'label': "Diagnosed",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def percent_of_women_with_cancer_by_race():
    result = json.loads(aggregate([{"$group": {
        "_id": "$race-recode-w-b-ai-api",
        "count": {"$sum": 1},
    }},
        {"$project": {
            "count": 1,
            "percentage": {"$multiply": [{"$divide": [100, 1546698]}, "$count"]}
        }},
        {"$sort": SON([("_id", -1)])}]))

    return {
        'labels': list(map(lambda x: x['_id'], result)),
        'datasets': [{
            'data': list(map(lambda x: x['percentage'], result)),
            'label': "Diagnosed",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def surgery_decisions_within_ages_30_40():
    result = json.loads(aggregate([{"$match": {
        "$or": [
            {"age-recode-with-1-year-olds": "35-39 years"},
            {"age-recode-with-1-year-olds": "30-34 years"}
        ]
    }},
        {"$group": {
            "_id": "",
            "total": {"$sum": 1},
            "surgery_set": {"$push": "$surgery"}
        }},
        {"$unwind": "$surgery_set"},
        {"$group": {
            "_id": {"surgery": "$surgery_set", "total": "$total"},
            "count": {"$sum": 1}
        }},
        {"$project": {
            "count": 1,
            "percentage": {"$multiply": [{"$divide": [100, "$_id.total"]}, "$count"], }
        }},
        {"$sort": SON([("percentage", -1)])}]))

    return {
        'labels': list(map(lambda x: x['_id']['surgery'], result)),
        'datasets': [{
            'data': list(map(lambda x: x['percentage'], result)),
            'label': "Diagnosed",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def chemotherapy_for_ages_30_40():
    result = json.loads(aggregate([{"$match": {
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
        {"$sort": SON([("_id", 1)])}]))

    return {
        'labels': list(map(lambda x: x['_id']['chemo'], result)),
        'datasets': [{
            'data': list(map(lambda x: x['percentage'], result)),
            'label': "Diagnosed",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def radiation_for_ages_30_40():
    result = json.loads(aggregate([{"$match": {
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
        {"$sort": SON([("_id", 1)])}]))

    return {
        'labels': list(map(lambda x: x['_id']['radiation'], result)),
        'datasets': [{
            'data': list(map(lambda x: x['percentage'], result)),
            'label': "Diagnosed",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def survival_months_within_ages_30_40():
    result = json.loads(aggregate([{"$match": {
        "$or": [
            {"age-recode-with-1-year-olds": "35-39 years"},
            {"age-recode-with-1-year-olds": "30-34 years"}
        ]
    }},
        {"$group": {
            "_id": "$survival-months",
            "count": {"$sum": 1}}},
        {"$sort": SON([("_id", -1)])}]))

    res = {'> 120 months': 0, '> 96 months': 0, '> 48 months': 0, '> 24 months': 0}
    for i in result:
        if isinstance(i['_id'], int) and i['_id'] > 120:
            res['> 120 months'] += i['count']
        elif isinstance(i['_id'], int) and i['_id'] > 96:
            res['> 96 months'] += i['count']
        elif isinstance(i['_id'], int) and i['_id'] > 48:
            res['> 48 months'] += i['count']
        elif isinstance(i['_id'], int) and i['_id'] > 24:
            res['> 24 months'] += i['count']

    return {
        'labels': list(map(lambda x: x, res.keys())),
        'datasets': [{
            'data': list(map(lambda x: x, res.values())),
            'label': "Diagnosed",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def cause_of_death_overall():
    result = json.loads(aggregate([{"$match": {
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
        {"$sort": SON([("count", -1)])}]))

    return {
        'labels': list(map(lambda x: x['_id']['cod-to-site-recode'], result)),
        'datasets': [{
            'data': list(map(lambda x: x['percentage'], result)),
            'label': "Diagnosed",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def cause_of_death_within_ages_30_40():
    result = json.loads(aggregate([{"$match": {
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
        {"$sort": SON([("count", -1)])}]))

    return {
        'labels': list(map(lambda x: x['_id']['cod-to-site-recode'], result)),
        'datasets': [{
            'data': list(map(lambda x: x['percentage'], result)),
            'label': "Diagnosed",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def diagnosis(input_json):
    input = json.loads(input_json)
    if input['age'] >= 85:
        age = "85+ years"
    elif input['age'] >= 80:
        age = "80-84 years"
    elif input['age'] >= 75:
        age = "75-79 years"
    elif input['age'] >= 70:
        age = "70-74 years"
    elif input['age'] >= 65:
        age = "65-69 years"
    elif input['age'] >= 60:
        age = "60-64 years"
    elif input['age'] >= 55:
        age = "55-59 years"
    elif input['age'] >= 50:
        age = "50-54 years"
    elif input['age'] >= 45:
        age = "45-49 years"
    elif input['age'] >= 40:
        age = "40-44 years"
    elif input['age'] >= 35:
        age = "35-39 years"
    elif input['age'] >= 30:
        age = "30-34 years"
    elif input['age'] >= 25:
        age = "25-29 years"
    elif input['age'] >= 20:
        age = "20-24 years"
    elif input['age'] >= 15:
        age = "15-19 years"
    elif input['age'] >= 10:
        age = "10-14 years"
    elif input['age'] >= 5:
        age = "05-09 years"
    elif input['age'] >= 1:
        age = "01-04 years"

    if input['tumor_size_in_mm'] >= 50:
        t_size_cm = ">5cm"
    elif input['tumor_size_in_mm'] >= 30:
        t_size_cm = ">3cm"
    elif input['tumor_size_in_mm'] >= 20:
        t_size_cm = "<3cm"
    elif input['tumor_size_in_mm'] >= 10:
        t_size_cm = "<2cm"
    elif input['tumor_size_in_mm'] < 10:
        t_size_cm = "<1cm"

    # Find request must be dict

    r = find(SON([
        ("age-recode-with-1-year-olds", age),
        ("grade", input["tumor_grade"]),
        ("er-status-recode-breast-cancer-1990", input["er_status"]),
        ("pr-status-recode-breast-cancer-1990", input["pr_status"]),
        ("derived-her2-recode-2010", input['her2_status']),
        ("t-size-cm", t_size_cm),
        ("regional-nodes-positive-1988", input['num_pos_nodes']),
        ("race-recode-w-b-ai-api", input["ethnicity"])
    ]), limit=10)

    return r


if __name__ == '__main__':
    # test1 = cause_of_death_within_ages_30_40()
    # pprint(test1)

    test2 = diagnosis('{"age": 39, '
                      '"tumor_grade": 1, '
                      '"er_status": "+", '
                      '"pr_status": "+", '
                      '"tumor_size_in_mm": 22, '
                      '"num_pos_nodes": 1, '
                      '"her2_status": "+", '
                      '"ethnicity": "White"}')
    pprint(test2)
    print(len(test2))
