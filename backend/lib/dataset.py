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


def get_age_group(age):
    age_group = None
    # if age >= 85:
    #     age_group = "85+ years"
    if age >= 80:
        age_group = ["80-84 years", "85+ years"]
    # elif age >= 75:
    #     age_group = "75-79 years"
    elif age >= 70:
        age_group = ["70-74 years", "75-79 years"]
    # elif age >= 65:
    #     age_group = "65-69 years"
    elif age >= 60:
        age_group = ["60-64 years", "65-69 years"]
    # elif age >= 55:
    #     age_group = "55-59 years"
    elif age >= 50:
        age_group = ["50-54 years", "55-59 years"]
    # elif age >= 45:
    #     age_group = "45-49 years"
    elif age >= 40:
        age_group = ["40-44 years", "45-49 years"]
    # elif age >= 35:
    #     age_group = "35-39 years"
    elif age >= 30:
        age_group = ["30-34 years", "35-39 years"]
    # elif age >= 25:
    #     age_group = "25-29 years"
    elif age >= 20:
        age_group = ["20-24 years", "25-29 years"]
    # elif age >= 15:
    #     age_group = "15-19 years"
    elif age >= 10:
        age_group = ["10-14 years", "15-19 years"]
    # elif age >= 5:
    #     age_group = "05-09 years"
    elif age >= 1:
        age_group = ["01-04 years", "05-09 years"]

    return age_group


def get_t_size_cm(size_mm):
    t_size_cm = None
    if size_mm >= 50:
        t_size_cm = ">5cm"
    elif size_mm >= 30:
        t_size_cm = ">3cm"
    elif size_mm >= 20:
        t_size_cm = "<3cm"
    elif size_mm >= 10:
        t_size_cm = "<2cm"
    elif size_mm < 10:
        t_size_cm = "<1cm"

    return t_size_cm


def create_filter(input_data, operator='$and'):
    input_data = json.loads(input_data)
    filter_list = []
    if 'age' in input_data.keys():
        age = get_age_group(input_data['age'])
        filter_list.append({"age-recode-with-1-year-olds": {"$in": age}})
    if 'tumor_size_in_mm' in input_data.keys():
        t_size_cm = get_t_size_cm(input_data['tumor_size_in_mm'])
        filter_list.append({"t-size-cm": t_size_cm})
    if 'sex' in input_data.keys():
        filter_list.append({"sex": input_data["sex"]})
    if 'tumor_grade' in input_data.keys():
        filter_list.append({"grade": input_data["tumor_grade"]})
    if 'er_status' in input_data.keys():
        filter_list.append({"er-status-recode-breast-cancer-1990": input_data["er_status"]})
    if 'pr_status' in input_data.keys():
        filter_list.append({"pr-status-recode-breast-cancer-1990": input_data["pr_status"]})
    if 'her2_status' in input_data.keys():
        filter_list.append({"derived-her2-recode-2010": input_data['her2_status']})
    if 'num_pos_nodes' in input_data.keys():
        filter_list.append({"regional-nodes-positive-1988": input_data['num_pos_nodes']})
    if 'ethnicity' in input_data.keys():
        filter_list.append({"race-recode-w-b-ai-api": input_data["ethnicity"]})
    if 'type' in input_data.keys():
        filter_list.append({"type": input_data["type"]})
    if 'breast-adjusted-ajcc-6th-stage-1988' in input_data.keys():
        filter_list.append({"breast-adjusted-ajcc-6th-stage-1988": input_data["breast-adjusted-ajcc-6th-stage-1988"]})
    if 'chemo' in input_data.keys():
        filter_list.append({"chemo": input_data["chemo"]})
    if 'radiation' in input_data.keys():
        filter_list.append({"radiation": input_data["radiation"]})

    return {operator: filter_list}


def diagnosis(input_json, limit=0):
    input_data = json.loads(input_json)
    filter_list = []
    if 'age' in input_data.keys():
        age = get_age_group(input_data['age'])
        filter_list.append(("age-recode-with-1-year-olds", age))
    if 'tumor_size_in_mm' in input_data.keys():
        t_size_cm = get_t_size_cm(input_data['tumor_size_in_mm'])
        filter_list.append(("t-size-cm", t_size_cm))
    if 'tumor_grade' in input_data.keys():
        filter_list.append(("grade", input_data["tumor_grade"]))
    if 'er_status' in input_data.keys():
        filter_list.append(("er-status-recode-breast-cancer-1990", input_data["er_status"]))
    if 'pr_status' in input_data.keys():
        filter_list.append(("pr-status-recode-breast-cancer-1990", input_data["pr_status"]))
    if 'her2_status' in input_data.keys():
        filter_list.append(("derived-her2-recode-2010", input_data["her2_status"]))
    if 'num_pos_nodes' in input_data.keys():
        filter_list.append(("regional-nodes-positive-1988", input_data["num_pos_nodes"]))
    if 'ethnicity' in input_data.keys():
        filter_list.append(("race-recode-w-b-ai-api", input_data["ethnicity"]))

    return find(SON(filter_list), limit=limit)


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


def breast_cancer_by_grade(age):
    dec_age = age - age % 10
    age_filter1 = "%s-%s years" % (dec_age, dec_age + 4)
    age_filter2 = "%s-%s years" % (dec_age + 5, dec_age + 9)

    j = aggregate([{"$match": {
        "$or": [
            {"age-recode-with-1-year-olds": age_filter1},
            {"age-recode-with-1-year-olds": age_filter2}
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


def percent_of_women_with_cancer_by_race_overall():
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


def cause_of_death_overall():
    """
    Does not need any input parameters
    Returns percentage of Breast and Others
    :return: json
    """
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

    data = {"Breast": 0, "Other": 0}
    for i, label in enumerate(list(map(lambda x: x['_id']['cod-to-site-recode'], result))):
        if label == 'Breast':
            data['Breast'] = result[i]['percentage']
        else:
            data['Other'] += result[i]['percentage']

    return {
        'labels': list(map(lambda x: x, data.keys())),
        'datasets': [{
            'data': list(map(lambda x: x, data.values())),
            'label': "Diagnosed",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def er_pos_pr_neg_her2_neg_annual_diagnoses():
    """
    Does not needs an input parameter
    :return: json
    """
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


def cause_of_death(input_json):
    """
    sample request input_json = '{"age": 48, ' \
                   '"sex": "Female", ' \
                   '"tumor_grade": 1, ' \
                   '"er_status": "+", ' \
                   '"pr_status": "+", ' \
                   '"tumor_size_in_mm": 22, ' \
                   '"num_pos_nodes": 0, ' \
                   '"her2_status": "+", ' \
                   '"ethnicity": "White"}'
    :param input_json:
    :return: json
    """
    filters = create_filter(input_json)
    result = json.loads(aggregate([
        {"$match": filters},
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


def survival_months(input_json):
    """
    sample request input_json = '{"age": 48, ' \
                   '"sex": "Female", ' \
                   '"tumor_grade": 1, ' \
                   '"er_status": "+", ' \
                   '"pr_status": "+", ' \
                   '"tumor_size_in_mm": 22, ' \
                   '"num_pos_nodes": 0, ' \
                   '"her2_status": "+", ' \
                   '"ethnicity": "White"}'
    :param input_json:
    :return: json
    """
    filters = create_filter(input_json)
    result = json.loads(aggregate([
        {"$match": filters},
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


def breast_cancer_by_size(input_json):
    """
    sample request input_json = '{"age": 48, ' \
                   '"sex": "Female", ' \
                   '"tumor_grade": 1, ' \
                   '"er_status": "+", ' \
                   '"pr_status": "+", ' \
                   '"tumor_size_in_mm": 22, ' \
                   '"num_pos_nodes": 0, ' \
                   '"her2_status": "+", ' \
                   '"ethnicity": "White"}'
    :param input_json:
    :return: json
    """
    filters = create_filter(input_json)
    j = aggregate([
        {"$match": filters},
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


def radiation(input_json):
    """
    sample request input_json = '{"age": 48, ' \
                   '"sex": "Female", ' \
                   '"tumor_grade": 1, ' \
                   '"er_status": "+", ' \
                   '"pr_status": "+", ' \
                   '"tumor_size_in_mm": 22, ' \
                   '"num_pos_nodes": 0, ' \
                   '"her2_status": "+", ' \
                   '"ethnicity": "White"}'
    :param input_json:
    :return: json
    """
    filters = create_filter(input_json)
    result = json.loads(aggregate([
        {"$match": filters},
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


def chemotherapy(input_json):
    """
    sample request input_json = '{"age": 48, ' \
                   '"sex": "Female", ' \
                   '"tumor_grade": 1, ' \
                   '"er_status": "+", ' \
                   '"pr_status": "+", ' \
                   '"tumor_size_in_mm": 22, ' \
                   '"num_pos_nodes": 0, ' \
                   '"her2_status": "+", ' \
                   '"ethnicity": "White"}'
    :param input_json:
    :return:
    """
    filters = create_filter(input_json)
    result = json.loads(aggregate([
        {"$match": filters},
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


def surgery_decisions(input_json):
    """
    sample request input_json = '{"age": 48, ' \
                   '"sex": "Female", ' \
                   '"tumor_grade": 1, ' \
                   '"er_status": "+", ' \
                   '"pr_status": "+", ' \
                   '"tumor_size_in_mm": 22, ' \
                   '"num_pos_nodes": 0, ' \
                   '"her2_status": "+", ' \
                   '"ethnicity": "White"}'
    :param input_json:
    :return: json
    """
    filters = create_filter(input_json)
    result = json.loads(aggregate([
        {"$match": filters},
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


def distribution_of_stage_of_cancer(input_json):
    """
    sample request input_json = '{"age": 48, ' \
                   '"sex": "Female", ' \
                   '"tumor_grade": 1, ' \
                   '"er_status": "+", ' \
                   '"pr_status": "+", ' \
                   '"tumor_size_in_mm": 22, ' \
                   '"num_pos_nodes": 0, ' \
                   '"her2_status": "+", ' \
                   '"ethnicity": "White"}'
    :param input_json:
    :return:
    """
    filters = create_filter(input_json)
    result = json.loads(aggregate([
        {"$match": filters},
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


def woman_annualy_diagnosed(input_json):
    """
    sample request input_json = '{"age": 48, ' \
                   '"sex": "Female", ' \
                   '"tumor_grade": 1, ' \
                   '"er_status": "+", ' \
                   '"pr_status": "+", ' \
                   '"tumor_size_in_mm": 22, ' \
                   '"num_pos_nodes": 0, ' \
                   '"her2_status": "+", ' \
                   '"ethnicity": "White"}'
    :param input_json:
    :return: json
    """
    filters = create_filter(input_json)
    result = json.loads(aggregate([
        {"$match": filters},
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


def growth_by_specific_type(input_json, operator="$and"):
    """
    Sample requests:
    input_json = '{"type": "IDC"}'
    input_json = '{"type": "In-Situ"}'
    input_json = '{"type": "ILC"}'
    input_json = '{"type": "Other", "type": "Mixed", "type": "IBC", "type": "Mixed "}'
    :param input_json:
    :param operator:
    :return: json
    """
    filters = create_filter(input_json, operator)
    result = json.loads(aggregate([
        {"$match": filters},
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


def percent_race_with_cancer_by_age(input_json):
    """
    sample request input_json = '{"age": 48, ' \
                   '"sex": "Female", ' \
                   '"tumor_grade": 1, ' \
                   '"er_status": "+", ' \
                   '"pr_status": "+", ' \
                   '"tumor_size_in_mm": 22, ' \
                   '"num_pos_nodes": 0, ' \
                   '"her2_status": "+", ' \
                   '"ethnicity": "White"}'
    :param input_json:
    :return: json
    """
    filters = create_filter(input_json)
    result = json.loads(aggregate([
        {"$match": filters},
        {"$group": {
            "_id": "",
            "total": {"$sum": 1},
            "race_set": {"$push": "$race-recode-w-b-ai-api"}
        }},
        {"$unwind": "$race_set"},
        {"$group": {
            "_id": {"race-recode-w-b-ai-api": "$race_set", "total": "$total"},
            "count": {"$sum": 1}
        }},
        {"$project": {
            "count": 1,
            "percentage": {"$multiply": [{"$divide": [100, "$_id.total"]}, "$count"], }
        }},
        {"$sort": SON([("percentage", -1)])}]))

    return {
        'labels': list(map(lambda x: x['_id']['race-recode-w-b-ai-api'], result)),
        'datasets': [{
            'data': list(map(lambda x: x['percentage'], result)),
            'label': "Diagnosed",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def breakout_by_stage(input_json):
    """
    Returns breakeout by stage discarding the nulls and "Blank" fields
    example filter:
    input_json = '{"age": 48, ' \
                 '"chemo": "Yes", ' \
                 '"breast-adjusted-ajcc-6th-stage-1988": {"$in": ' \
                 '["I", "IIA", "IIB", "IIIA", "IIIB", "IIIC", "IIINOS", "IV", 0]}}'
    :param input_json: json
    :return: json
    """
    filters = create_filter(input_json, "$and")
    result = json.loads(aggregate([
        {"$match": filters},
        {"$group": {
            "_id": "",
            "total": {"$sum": 1},
            "subset": {"$push": "$breast-adjusted-ajcc-6th-stage-1988"}
        }},
        {"$unwind": "$subset"},
        {"$group": {
            "_id": {"breast-adjusted-ajcc-6th-stage-1988": "$subset", "total": "$total"},
            "count": {"$sum": 1}
        }},
        {"$project": {
            "count": 1,
            "percentage": {"$multiply": [{"$divide": [100, "$_id.total"]}, "$count"], }
        }},
        {"$sort": SON([("percentage", -1)])}]))

    data = {"II": 0, "III": 0, "0": 0}
    for i, label in enumerate(list(map(lambda x: x['_id']['breast-adjusted-ajcc-6th-stage-1988'], result))):
        if label == 'I':
            data['I'] = result[i]['percentage']
        elif label in ['IIA', 'IIB']:
            data['II'] += result[i]['percentage']
        elif label in ['IIIA', 'IIIB', 'IIIC', 'IIINOS']:
            data['III'] += result[i]['percentage']
        elif label == 'IV':
            data['IV'] = result[i]['percentage']
        elif label in [0] or label is None:
            data['0'] += result[i]['percentage']

    return {
        'labels': list(map(lambda x: x, data.keys())),
        'datasets': [{
            'data': list(map(lambda x: x, data.values())),
            'label': "Diagnosed",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


# def breakout_by_stage2(input_json):
#     """
#     Do not use this func it is only for comparation
#     :param input_json:
#     :return:
#     """
#     filters = create_filter(input_json)
#     result = json.loads(aggregate([
#         {"$match": filters},
#         {"$group": {
#             "_id": "",
#             "total": {"$sum": 1},
#             "subset": {"$push": "$1998-stage"}
#         }},
#         {"$unwind": "$subset"},
#         {"$group": {
#             "_id": {"1998-stage": "$subset", "total": "$total"},
#             "count": {"$sum": 1}
#         }},
#         {"$project": {
#             "count": 1,
#             "percentage": {"$multiply": [{"$divide": [100, "$_id.total"]}, "$count"], }
#         }},
#         {"$sort": SON([("percentage", -1)])}]))
#
#     return {
#         'labels': list(map(lambda x: x['_id']['1998-stage'], result)),
#         'datasets': [{
#             'data': list(map(lambda x: x['percentage'], result)),
#             'label': "Diagnosed",
#             'borderColor': '#48ccf5',
#             'fill': False
#         }]
#     }


# def cause_of_death_within_ages_30_40():
#     result = json.loads(aggregate([{"$match": {
#         "$and": [{"cod-to-site-recode": {"$nin": ["Alive"]}},
#                  {"$or": [
#                      {"age-recode-with-1-year-olds": "35-39 years"},
#                      {"age-recode-with-1-year-olds": "30-34 years"}
#                  ]}]
#     }},
#         {"$group": {
#             "_id": "",
#             "total": {"$sum": 1},
#             "data_subset": {"$push": "$cod-to-site-recode"}
#         }},
#         {"$unwind": "$data_subset"},
#         {"$group": {
#             "_id": {"cod-to-site-recode": "$data_subset", "total": "$total"},
#             "count": {"$sum": 1}}},
#         {"$project": {
#             "count": 1,
#             "percentage": {"$multiply": [{"$divide": [100, "$_id.total"]}, "$count"], }
#         }},
#         {"$sort": SON([("count", -1)])}]))
#
#     data = {"Breast": 0, "Other": 0}
#     for i, label in enumerate(list(map(lambda x: x['_id']['cod-to-site-recode'], result))):
#         if label == 'Breast':
#             data['Breast'] = result[i]['percentage']
#         else:
#             data['Other'] += result[i]['percentage']
#
#     return {
#         'labels': list(map(lambda x: x, data.keys())),
#         'datasets': [{
#             'data': list(map(lambda x: x, data.values())),
#             'label': "Diagnosed",
#             'borderColor': '#48ccf5',
#             'fill': False
#         }]
#     }


# def surgery_decisions_within_ages_30_40():
#     result = json.loads(aggregate([{"$match": {
#         "$or": [
#             {"age-recode-with-1-year-olds": "35-39 years"},
#             {"age-recode-with-1-year-olds": "30-34 years"}
#         ]
#     }},
#         {"$group": {
#             "_id": "",
#             "total": {"$sum": 1},
#             "surgery_set": {"$push": "$surgery"}
#         }},
#         {"$unwind": "$surgery_set"},
#         {"$group": {
#             "_id": {"surgery": "$surgery_set", "total": "$total"},
#             "count": {"$sum": 1}
#         }},
#         {"$project": {
#             "count": 1,
#             "percentage": {"$multiply": [{"$divide": [100, "$_id.total"]}, "$count"], }
#         }},
#         {"$sort": SON([("percentage", -1)])}]))
#
#     return {
#         'labels': list(map(lambda x: x['_id']['surgery'], result)),
#         'datasets': [{
#             'data': list(map(lambda x: x['percentage'], result)),
#             'label': "Diagnosed",
#             'borderColor': '#48ccf5',
#             'fill': False
#         }]
#     }


# def chemotherapy_for_ages_30_40():
#     result = json.loads(aggregate([{"$match": {
#         "$or": [
#             {"age-recode-with-1-year-olds": "35-39 years"},
#             {"age-recode-with-1-year-olds": "30-34 years"}
#         ]
#     }},
#         {"$group": {
#             "_id": "",
#             "total": {"$sum": 1},
#             "chemo_set": {"$push": "$chemo"}
#         }},
#         {"$unwind": "$chemo_set"},
#         {"$group": {
#             "_id": {"chemo": "$chemo_set", "total": "$total"},
#             "count": {"$sum": 1}}},
#         {"$project": {
#             "count": 1,
#             "percentage": {"$multiply": [{"$divide": [100, "$_id.total"]}, "$count"], }
#         }},
#         {"$sort": SON([("_id", 1)])}]))
#
#     return {
#         'labels': list(map(lambda x: x['_id']['chemo'], result)),
#         'datasets': [{
#             'data': list(map(lambda x: x['percentage'], result)),
#             'label': "Diagnosed",
#             'borderColor': '#48ccf5',
#             'fill': False
#         }]
#     }


# def radiation_for_ages_30_40():
#     result = json.loads(aggregate([{"$match": {
#         "$or": [
#             {"age-recode-with-1-year-olds": "35-39 years"},
#             {"age-recode-with-1-year-olds": "30-34 years"}
#         ]
#     }},
#         {"$group": {
#             "_id": "",
#             "total": {"$sum": 1},
#             "data_subset": {"$push": "$radiation"}
#         }},
#         {"$unwind": "$data_subset"},
#         {"$group": {
#             "_id": {"radiation": "$data_subset", "total": "$total"},
#             "count": {"$sum": 1}}},
#         {"$project": {
#             "count": 1,
#             "percentage": {"$multiply": [{"$divide": [100, "$_id.total"]}, "$count"], }
#         }},
#         {"$sort": SON([("_id", 1)])}]))
#
#     return {
#         'labels': list(map(lambda x: x['_id']['radiation'], result)),
#         'datasets': [{
#             'data': list(map(lambda x: x['percentage'], result)),
#             'label': "Diagnosed",
#             'borderColor': '#48ccf5',
#             'fill': False
#         }]
#     }


# def survival_months_within_ages_30_40():
#     result = json.loads(aggregate([{"$match": {
#         "$or": [
#             {"age-recode-with-1-year-olds": "35-39 years"},
#             {"age-recode-with-1-year-olds": "30-34 years"}
#         ]
#     }},
#         {"$group": {
#             "_id": "$survival-months",
#             "count": {"$sum": 1}}},
#         {"$sort": SON([("_id", -1)])}]))
#
#     res = {'> 120 months': 0, '> 96 months': 0, '> 48 months': 0, '> 24 months': 0}
#     for i in result:
#         if isinstance(i['_id'], int) and i['_id'] > 120:
#             res['> 120 months'] += i['count']
#         elif isinstance(i['_id'], int) and i['_id'] > 96:
#             res['> 96 months'] += i['count']
#         elif isinstance(i['_id'], int) and i['_id'] > 48:
#             res['> 48 months'] += i['count']
#         elif isinstance(i['_id'], int) and i['_id'] > 24:
#             res['> 24 months'] += i['count']
#
#     return {
#         'labels': list(map(lambda x: x, res.keys())),
#         'datasets': [{
#             'data': list(map(lambda x: x, res.values())),
#             'label': "Diagnosed",
#             'borderColor': '#48ccf5',
#             'fill': False
#         }]
#     }


# def breast_cancer_by_size_age_30_40():
#     """
#     Custom func for cancer_by_size
#     :return:
#     """
#     j = aggregate([{"$match": {
#         "$or": [
#             {"age-recode-with-1-year-olds": "35-39 years"},
#             {"age-recode-with-1-year-olds": "30-34 years"}
#         ]
#     }},
#         {"$group": {
#             "_id": "$t-size-cm",
#             "count": {"$sum": 1}}},
#         {"$sort": SON([("_id", 1)])}])
#     l = json.loads(j)
#     res = {'< 1cm': 0}
#     for i in l:
#         if i['_id'] == '<1cm':
#             res['< 1cm'] += i['count']
#         elif i['_id'] == '<2cm':
#             res['< 2cm'] = i['count']
#         elif i['_id'] == '<3cm':
#             res['< 3cm'] = i['count']
#         elif i['_id'] == '>3cm':
#             res['> 3cm'] = i['count']
#         elif i['_id'] == '>5cm':
#             res['> 5cm'] = i['count']
#         elif i['_id'] == 'Micro':
#             res['< 1cm'] += i['count']
#
#     return {
#         'labels': list(map(lambda x: x, res.keys())),
#         'datasets': [{
#             'data': list(map(lambda x: x, res.values())),
#             'label': "Diagnosed",
#             'borderColor': '#48ccf5',
#             'fill': False
#         }]
#     }


# def woman_age_30_40_annualy_diagnosed():
#     result = json.loads(aggregate([{"$match": {
#         "$or": [
#             {"age-recode-with-1-year-olds": "35-39 years"},
#             {"age-recode-with-1-year-olds": "30-34 years"}
#         ]
#     }},
#         {"$group": {
#             "_id": "$year-of-diagnosis",
#             "count": {"$sum": 1}}},
#         {"$sort": SON([("_id", 1)])}]))
#
#     return {
#         'labels': list(map(lambda x: x['_id'], result)),
#         'datasets': [{
#             'data': list(map(lambda x: x['count'], result)),
#             'label': "Diagnosed",
#             'borderColor': '#48ccf5',
#             'fill': False
#         }]
#     }


# def distribution_of_stage_of_cancer_for_ages_30_40():
#     result = json.loads(aggregate([{"$match": {
#         "$or": [
#             {"age-recode-with-1-year-olds": "35-39 years"},
#             {"age-recode-with-1-year-olds": "30-34 years"}
#         ]
#     }},
#         {"$group": {
#             "_id": "$1998-stage",
#             "count": {"$sum": 1}}},
#         {"$sort": SON([("_id", 1)])}]))
#
#     return {
#         'labels': list(map(lambda x: x['_id'], result)),
#         'datasets': [{
#             'data': list(map(lambda x: x['count'], result)),
#             'label': "Diagnosed",
#             'borderColor': '#48ccf5',
#             'fill': False
#         }]
#     }


if __name__ == '__main__':
    diag_request = '{"age": 48, ' \
                   '"sex": "Female", ' \
                   '"tumor_grade": 1, ' \
                   '"er_status": "+", ' \
                   '"pr_status": "+", ' \
                   '"tumor_size_in_mm": 22, ' \
                   '"num_pos_nodes": 0, ' \
                   '"her2_status": "+", ' \
                   '"ethnicity": "White"}'

    diag_request_age_only = '{"age": 48}'

    # pprint(breast_cancer_by_size(diag_request_age_only))

    # d = diagnosis(diag_request, limit=25)
    # pprint(d)
    type_idc = '{"type": "IDC"}'
    type_insitu = '{"type": "In-Situ"}'
    type_ilc = '{"type": "ILC"}'
    type_others = '{"type": "Other", "type": "Mixed", "type": "IBC", "type": "Mixed "}'

    # pprint(growth_by_specific_type(type_others, "$or"))
    diag_request_age_for_stage = '{"age": 48, ' \
                                 '"breast-adjusted-ajcc-6th-stage-1988": {"$in": ' \
                                 '["I", "IIA", "IIB", "IIIA", "IIIB", "IIIC", "IIINOS", "IV", 0]}}'

    # pprint(breakout_by_stage(diag_request_age_for_stage))
    # pprint(cause_of_death_within_ages_30_40())

    input_json = '{"age": 48, ' \
                 '"chemo": "Yes", ' \
                 '"breast-adjusted-ajcc-6th-stage-1988": {"$in": ' \
                 '["I", "IIA", "IIB", "IIIA", "IIIB", "IIIC", "IIINOS", "IV", 0]}}'
    pprint(breakout_by_stage(input_json))
