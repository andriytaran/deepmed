import copy, json
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
        return d
    return None


def get_age_group(age):
    age_group = None
    if age >= 80:
        age_group = ["80-84 years", "85+ years"]
    elif age >= 70:
        age_group = ["70-74 years", "75-79 years"]
    elif age >= 60:
        age_group = ["60-64 years", "65-69 years"]
    elif age >= 50:
        age_group = ["50-54 years", "55-59 years"]
    elif age >= 40:
        age_group = ["40-44 years", "45-49 years"]
    elif age >= 30:
        age_group = ["30-34 years", "35-39 years"]
    elif age >= 20:
        age_group = ["20-24 years", "25-29 years"]
    elif age >= 10:
        age_group = ["10-14 years", "15-19 years"]
    elif age >= 0:
        age_group = ["00-04 years", "05-09 years"]

    return age_group


def get_race_group(race):
    race_group = None
    if race == 'Caucasian':
        race_group = ["White"]
    elif race == 'African American':
        race_group = ["Black"]
    elif race == 'Filipino':
        race_group = ["Filipino"]
    elif race == 'Chinese':
        race_group = ['Chinese']
    elif race == 'Japanese':
        race_group = ["Japanese"]
    elif race == 'Other Asian':
        race_group = ['Other Asian (1991+)', 'Kampuchean (1988+)', 'Laotian (1988+)']
    elif race == 'Korean':
        race_group = ["Korean (1988+)"]
    elif race == 'American Indian':
        race_group = ["American Indian/Alaska Native"]
    elif race == 'Vietnamese':
        race_group = ["Vietnamese (1988+)"]
    elif race == 'Hawaiian':
        race_group = ["Hawaiian"]
    elif race == 'South Asian':
        race_group = ['Asian Indian (2010+)', 'Asian Indian or Pakistani, NOS (1988+)', 'Pakistani (2010+)']
    elif race == 'Thai':
        race_group = ["Thai (1994+)"]
    elif race == 'Pacific Islander':
        race_group = ['Pacific Islander, NOS (1991+)', 'Samoan (1991+)', 'Tongan (1991+)', 'Fiji Islander (1991+)',
                      'Guamanian, NOS (1991+)', 'Micronesian, NOS (1991+)', 'Melanesian, NOS (1991+)',
                      'Polynesian, NOS (1991+)', 'New Guinean (1991+)', 'Chamorran (1991+)', 'Tahitian (1991+)']
    elif race == 'All Asians':
        race_group = ['Pacific Islander, NOS (1991+)', 'Samoan (1991+)', 'Tongan (1991+)', 'Fiji Islander (1991+)',
                      'Guamanian, NOS (1991+)', 'Micronesian, NOS (1991+)', 'Melanesian, NOS (1991+)',
                      'Polynesian, NOS (1991+)', 'New Guinean (1991+)', 'Chamorran (1991+)', 'Tahitian (1991+)',
                      'Filipino', 'Chinese', 'Hmong (1988+)', 'Japanese', 'Other Asian (1991+)', 'Kampuchean (1988+)',
                      'Laotian (1988+)', 'Korean (1988+)', 'Vietnamese (1988+)', 'Asian Indian (2010+)',
                      'Asian Indian or Pakistani, NOS (1988+)', 'Pakistani (2010+)', 'Thai (1994+)']
    elif race == 'Other':
        race_group = ['Unknown', 'NOS (1988+)', 'Other', 'NOS (1991+)']

    return race_group


def ca_get_t_size_cm(group):
    if group == '0-2cm':
        t_size_cm = {"$in": ["<1cm", "<2cm", "Micro"]}
    elif group == '2-5cm':
        t_size_cm = {"$in": ["<3cm", ">3cm"]}
    elif group == '5cm+':
        t_size_cm = ">5cm"
    else:
        t_size_cm = None
    return t_size_cm


def ca_get_node_range(group):
    n_size = None
    if group == "9+":
        # n_size = {"$gte": 10}
        range_list = [x for x in range(10, 90)]
        range_list.append('>9')
        n_size = {"$in": range_list}
    elif group == "4-8":
        n_size = {"$in": [4, 5, 6, 7, 8, 9]}
    elif group == "1-3":
        n_size = {"$in": [1, 2, 3, '>1']}
    elif group == "0":
        n_size = {"$eq": 0}
    return n_size


def get_tumor_number(group):
    t_number = None
    if group == "3+":
        t_number = {"$gte": 3}
    elif group == "2":
        t_number = {"$eq": 2}
    elif group == "1":
        t_number = {"$eq": 1}
    elif group == "0":
        t_number = {"$eq": 0}
    return t_number


def ca_create_filter(input_data, operator='$and'):
    """
    Converts json request to list of dicts formated for use as a match filter in mongodb.
    "age" takes integer age, and groups ages by decades, ex: input 44 (years), outputs ["40-44 years", "45-49 years"]
    "tumor_size_in_mm" takes integer size in mm, and groups by size in cm, ex: input 18 (mm), outputs "<2cm"
    "num_pos_nodes" takes integer number, and groups by custom groups, ex: input 4, output {"$in": [4, 5, 6, 7, 8, 9]}
    :param input_data: json = '{"age": int, ' \
                   '"sex": string, ' \
                   '"tumor_grade": int, ' \
                   '"er_status": "+" or "-", ' \
                   '"pr_status": "+" or "-", ' \
                   '"tumor_size": string, ' \
                   '"num_pos_nodes": string, ' \
                   '"her2_status": "+" or "-", ' \
                   '"ethnicity": string}'
    :param operator: {"$and"} or {"or"} as filtering operators
    :return: list of dicts
    """
    input_data = json.loads(input_data)
    filter_list = []
    if 'age' in input_data.keys():
        age = get_age_group(input_data['age'])
        if age:
            filter_list.append({"age-recode-with-1-year-olds": {"$in": age}})
    if 'tumor_size' in input_data.keys():
        t_size_cm = ca_get_t_size_cm(input_data['tumor_size'])
        if t_size_cm:
            filter_list.append({"t-size-cm": t_size_cm})
    if 'tumor_number' in input_data.keys():
        t_number = get_tumor_number(input_data['tumor_number'])
        if t_number:
            filter_list.append({"total-number-of-in-situ-malignant-tumors-for-patient": t_number})
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
        n_size = ca_get_node_range(input_data['num_pos_nodes'])
        if n_size:
            filter_list.append({"regional-nodes-positive-1988": n_size})
    if 'ethnicity' in input_data.keys():
        race = get_race_group(input_data['ethnicity'])
        if race:
            filter_list.append({"race-ethnicity": {"$in": race}})
    if 'type' in input_data.keys():
        filter_list.append({"type": input_data["type"]})
    if 'stage' in input_data.keys():
        filter_list.append(
            {"breast-adjusted-ajcc-6th-stage-1988": input_data["stage"]})
    if 'chemo' in input_data.keys():
        filter_list.append({"chemo": input_data["chemo"]})
    if 'radiation' in input_data.keys():
        filter_list.append({"radiation": input_data["radiation"]})
    if 'surgery' in input_data.keys():
        filter_list.append({"surgery": input_data["surgery"]})

    return {operator: filter_list}


def custom_analytics(input_json, grouping):
    def ca_by_grade(input_json):
        filters = ca_create_filter(input_json)
        stages = [1.0, 2.0, 3.0, 4.0]
        filters['$and'].append({"grade": {"$in": stages}})
        result = json.loads(aggregate([
            {"$match": filters},
            {"$group": {
                "_id": "",
                "total": {"$sum": 1},
                "subset": {"$push": "$grade"}
            }},
            {"$unwind": "$subset"},
            {"$group": {
                "_id": {"grade": "$subset", "total": "$total"},
                "count": {"$sum": 1}
            }},
            {"$project": {
                "count": 1,
                "percentage": {"$multiply": [{"$divide": [100, "$_id.total"]}, "$count"], }
            }},
            {"$sort": SON([("percentage", -1)])}]))

        data = {'Grade 1': 0, 'Grade 2': 0, 'Grade 3': 0}
        for i, label in enumerate(list(map(lambda x: x['_id']['grade'], result))):
            if label == 1.0:
                data['Grade 1'] += result[i]['percentage']
            elif label == 2.0:
                data['Grade 2'] += result[i]['percentage']
            elif label in [3.0, 4.0]:
                data['Grade 3'] += result[i]['percentage']

        return {
            'labels': list(map(lambda x: x, data.keys())),
            'datasets': [{
                'data': list(map(lambda x: x, data.values())),
                'label': "Diagnosed",
                'borderColor': '#48ccf5',
                'fill': False
            }]
        }

    def ca_by_stage(input_json):
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
        filters = ca_create_filter(input_json)
        stages = ['I', 'IIA', 'IIB', 'IIIA', 'IIIB', 'IIIC', 'IV']
        filters['$and'].append({"breast-adjusted-ajcc-6th-stage-1988": {"$in": stages}})
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

        data = {"I": 0, "II": 0, "III": 0, "IV": 0}
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
                'label': "Stage",
                'borderColor': '#48ccf5',
                'fill': False
            }]
        }

    def ca_by_type(input_json):
        filters = ca_create_filter(input_json)
        result = json.loads(aggregate([
            {"$match": filters},
            {"$group": {
                "_id": "",
                "total": {"$sum": 1},
                "subset": {"$push": "$type"}
            }},
            {"$unwind": "$subset"},
            {"$group": {
                "_id": {"type": "$subset", "total": "$total"},
                "count": {"$sum": 1}
            }},
            {"$project": {
                "count": 1,
                "percentage": {"$multiply": [{"$divide": [100, "$_id.total"]}, "$count"], }
            }},
            {"$sort": SON([("percentage", -1)])}]))

        data = {"IDC": 0, "DCIS": 0, "ILC": 0, "Other": 0}
        for i, label in enumerate(list(map(lambda x: x['_id']['type'], result))):
            if label == 'IDC':
                data['IDC'] += result[i]['percentage']
            elif label == 'In-Situ':
                data['DCIS'] += result[i]['percentage']
            elif label in ['Other', 'Mixed', 'IBC', 'Mixed ']:
                data['Other'] += result[i]['percentage']
            elif label == 'ILC':
                data['ILC'] += result[i]['percentage']

        return {
            'labels': list(map(lambda x: x, data.keys())),
            'datasets': [{
                'data': list(map(lambda x: x, data.values())),
                'label': "Diagnosed",
                'borderColor': '#48ccf5',
                'fill': False
            }]
        }

    def ca_by_size(input_json):
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
        filters = ca_create_filter(input_json)
        sizes = ['< 1cm', '<2cm', '<3cm', '>3cm', '>5cm', 'Micro']
        filters['$and'].append({"t-size-cm": {"$in": sizes}})
        result = json.loads(aggregate([
            {"$match": filters},
            {"$group": {
                "_id": "",
                "total": {"$sum": 1},
                "subset": {"$push": "$t-size-cm"}
            }},
            {"$unwind": "$subset"},
            {"$group": {
                "_id": {"t-size-cm": "$subset", "total": "$total"},
                "count": {"$sum": 1}
            }},
            {"$project": {
                "count": 1,
                "percentage": {"$multiply": [{"$divide": [100, "$_id.total"]}, "$count"], }
            }},
            {"$sort": SON([("percentage", -1)])}]))

        data = {'0-2cm': 0, '2-5cm': 0, '5cm+': 0}
        for i, label in enumerate(list(map(lambda x: x['_id']['t-size-cm'], result))):
            if label in ['Micro', '< 1cm', '<2cm']:
                data['0-2cm'] += result[i]['percentage']
            elif label in ['<3cm', '>3cm']:
                data['2-5cm'] += result[i]['percentage']
            elif label == '>5cm':
                data['5cm+'] += result[i]['percentage']
            else:
                print(label)

        return {
            'labels': list(map(lambda x: x, data.keys())),
            'datasets': [{
                'data': list(map(lambda x: x, data.values())),
                'label': "Diagnosed",
                'borderColor': '#48ccf5',
                'fill': False
            }]
        }

    def ca_by_race(input_json):
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
        filters = ca_create_filter(input_json)
        pre_filters = {'$and': [d for d in filters['$and'] if 'race-ethnicity' not in d]}
        if len(pre_filters) > 1:
            full_result = json.loads(aggregate([
                {"$match": pre_filters},
                {"$group": {
                    "_id": "",
                    "count": {"$sum": 1}}},
                {"$sort": SON([("count", -1), ("_id", -1)])}]))
        else:
            full_result = json.loads(aggregate([
                {"$group": {
                    "_id": "",
                    "count": {"$sum": 1}}},
                {"$sort": SON([("count", -1), ("_id", -1)])}]))

        totalCount = full_result[0]['count']

        result = json.loads(aggregate([
            {"$match": filters},
            {"$group": {
                "_id": "",
                "total": {"$sum": 1},
                "totalFull": {"$sum": 1},
                "race_set": {"$push": "$race-ethnicity"}
            }},
            {"$unwind": "$race_set"},
            {"$group": {
                "_id": {"race-ethnicity": "$race_set", "total": "$total"},
                "count": {"$sum": 1}
            }},
            {"$project": {
                "percentage": {"$multiply": [{"$divide": [100, totalCount]}, "$count"], },
            }},
            {"$sort": SON([("percentage", -1)])}]))

        data = {"Other": 0}
        input_dict = json.loads(input_json)
        if 'ethnicity' in input_dict:
            data[input_dict['ethnicity']] = result[0]['percentage']
            data['Other'] = 100.0 - result[0]['percentage']

        return {
            'labels': list(map(lambda x: x, data.keys())),
            'datasets': [{
                'data': list(map(lambda x: x, data.values())),
                'label': "Diagnosed",
                'borderColor': '#48ccf5',
                'fill': False
            }]
        }

    def ca_by_race2(input_json):
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
        filters = ca_create_filter(input_json)
        result = json.loads(aggregate([
            {"$match": filters},
            {"$group": {
                "_id": "",
                "total": {"$sum": 1},
                "race_set": {"$push": "$race-ethnicity"}
            }},
            {"$unwind": "$race_set"},
            {"$group": {
                "_id": {"race-ethnicity": "$race_set", "total": "$total"},
                "count": {"$sum": 1}
            }},
            {"$project": {
                "count": 1,
                "percentage": {"$multiply": [{"$divide": [100, "$_id.total"]}, "$count"], }
            }},
            {"$sort": SON([("percentage", -1)])}]))

        data = {"Caucasian": 0, "African American": 0, "Asian": 0,
                "American Indian": 0, "Other": 0}
        for i, label in enumerate(list(map(lambda x: x['_id']['race-ethnicity'], result))):
            if label == 'White':
                data['Caucasian'] += result[i]['percentage']
            elif label == 'Black':
                data['African American'] += result[i]['percentage']
            elif label in ['Pacific Islander, NOS (1991+)', 'Samoan (1991+)', 'Tongan (1991+)', 'Fiji Islander (1991+)',
                           'Guamanian, NOS (1991+)', 'Micronesian, NOS (1991+)', 'Melanesian, NOS (1991+)',
                           'Polynesian, NOS (1991+)', 'New Guinean (1991+)', 'Chamorran (1991+)', 'Tahitian (1991+)',
                           'Filipino', 'Chinese', 'Hmong (1988+)', 'Japanese', 'Other Asian (1991+)',
                           'Kampuchean (1988+)',
                           'Laotian (1988+)', 'Korean (1988+)', 'Vietnamese (1988+)', 'Hawaiian',
                           'Asian Indian (2010+)',
                           'Asian Indian or Pakistani, NOS (1988+)', 'Pakistani (2010+)', 'Thai (1994+)']:
                data['Asian'] += result[i]['percentage']
            elif label == 'American Indian/Alaska Native':
                data['American Indian'] += result[i]['percentage']
            elif label in ['Unknown', 'NOS (1988+)', 'Other', 'NOS (1991+)'] or label is None:
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

    def ca_by_race_old(input_json):
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
        filters = ca_create_filter(input_json)
        result = json.loads(aggregate([
            {"$match": filters},
            {"$group": {
                "_id": "",
                "total": {"$sum": 1},
                "race_set": {"$push": "$race-ethnicity"}
            }},
            {"$unwind": "$race_set"},
            {"$group": {
                "_id": {"race-ethnicity": "$race_set", "total": "$total"},
                "count": {"$sum": 1}
            }},
            {"$project": {
                "count": 1,
                "percentage": {"$multiply": [{"$divide": [100, "$_id.total"]}, "$count"], }
            }},
            {"$sort": SON([("percentage", -1)])}]))

        data = {"Caucasian": 0, "African American": 0, "Filipino": 0, "Chinese": 0, "Japanese": 0, "Other Asian": 0,
                "Korean": 0, "American Indian": 0, "Vietnamese": 0, "Other": 0, "Hawaiian": 0, "South Asian": 0,
                "Thai": 0, "Pacific Islander": 0}
        for i, label in enumerate(list(map(lambda x: x['_id']['race-ethnicity'], result))):
            if label == 'White':
                data['Caucasian'] += result[i]['percentage']
            elif label == 'Black':
                data['African American'] += result[i]['percentage']
            elif label == 'Filipino':
                data['Filipino'] += result[i]['percentage']
            elif label in ['Chinese', 'Hmong (1988+)']:
                data['Chinese'] += result[i]['percentage']
            elif label == 'Japanese':
                data['Japanese'] += result[i]['percentage']
            elif label in ['Other Asian (1991+)', 'Kampuchean (1988+)', 'Laotian (1988+)']:
                data['Other Asian'] += result[i]['percentage']
            elif label == 'Korean (1988+)':
                data['Korean'] += result[i]['percentage']
            elif label == 'American Indian/Alaska Native':
                data['American Indian'] += result[i]['percentage']
            elif label == 'Vietnamese (1988+)':
                data['Vietnamese'] += result[i]['percentage']
            elif label == 'Hawaiian':
                data['Hawaiian'] += result[i]['percentage']
            elif label in ['Asian Indian (2010+)', 'Asian Indian or Pakistani, NOS (1988+)', 'Pakistani (2010+)']:
                data['South Asian'] += result[i]['percentage']
            elif label == 'Thai (1994+)':
                data['Thai'] += result[i]['percentage']
            elif label in ['Pacific Islander, NOS (1991+)', 'Samoan (1991+)', 'Tongan (1991+)', 'Fiji Islander (1991+)',
                           'Guamanian, NOS (1991+)', 'Micronesian, NOS (1991+)', 'Melanesian, NOS (1991+)',
                           'Polynesian, NOS (1991+)', 'New Guinean (1991+)', 'Chamorran (1991+)', 'Tahitian (1991+)']:
                data['Pacific Islander'] += result[i]['percentage']
            elif label in ['Unknown', 'NOS (1988+)', 'Other', 'NOS (1991+)'] or label is None:
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

    def ca_cause_of_death(input_json):
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
        filters = ca_create_filter(input_json)
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

        data = {"Alive": 0, "Breast": 0, "Other": 0}
        for i, label in enumerate(list(map(lambda x: x['_id']['cod-to-site-recode'], result))):
            if label == 'Breast':
                data['Breast'] += result[i]['percentage']
            elif label == 'Alive':
                data['Alive'] += result[i]['percentage']
            else:
                data['Other'] += result[i]['percentage']

        return {
            'labels': list(map(lambda x: x, data.keys())),
            'datasets': [{
                'data': list(map(lambda x: x, data.values())),
                'label': "Deaths",
                'borderColor': '#48ccf5',
                'fill': False
            }]
        }

    def radiation_filter(input_json):
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
        filters = ca_create_filter(input_json)
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
            {"$sort": SON([("_id", -1)])}]))

        return {
            'labels': list(map(lambda x: x['_id']['radiation'], result)),
            'datasets': [{
                'data': list(map(lambda x: x['percentage'], result)),
                'label': "Radiation",
                'borderColor': '#48ccf5',
                'fill': False
            }]
        }

    def chemotherapy_filter(input_json):
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
        filters = ca_create_filter(input_json)
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
            {"$sort": SON([("_id", -1)])}]))

        return {
            'labels': list(map(lambda x: x['_id']['chemo'], result)),
            'datasets': [{
                'data': list(map(lambda x: x['percentage'], result)),
                'label': "Chemotherapy",
                'borderColor': '#48ccf5',
                'fill': False
            }]
        }

    def ca_by_surgery(input_json):
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
        filters = ca_create_filter(input_json)
        excluded = ['None']
        filters['$and'].append({"surgery": {"$nin": excluded}})
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

        data = OrderedDict()
        data['Lumpectomy'] = 0
        data['Mastectomy'] = 0
        data['Other'] = 0
        for i, label in enumerate(list(map(lambda x: x['_id']['surgery'], result))):
            if label in ['Lumpectomy', 'Partial Mastectomy']:
                data['Lumpectomy'] += result[i]['percentage']
            elif label in ['Single Mastectomy', 'Mastectomy ', 'Simple Mastectomy']:
                data['Mastectomy'] += result[i]['percentage']
            # elif label == 'Simple Mastectomy':
            #     data['Simple Mastectomy'] = result[i]['percentage']
            elif label == 'Bi-Lateral Mastectomy':
                data['Bi-Lateral Mastectomy'] = result[i]['percentage']
            elif label in ['Other', 'Surgery']:
                data['Other'] += result[i]['percentage']
        data.move_to_end("Other")

        return {
            'labels': list(map(lambda x: x, data.keys())),
            'datasets': [{
                'data': list(map(lambda x: x, data.values())),
                'label': "Surgeries",
                'borderColor': '#48ccf5',
                'fill': False
            }]
        }

    filters = ca_create_filter(input_json)
    if grouping == 'grade':
        filters['$and'] = [d for d in filters['$and'] if 'grade' not in d]
        return ca_by_grade(input_json)
    elif grouping == 'stage':
        filters['$and'] = [d for d in filters['$and'] if 'breast-adjusted-ajcc-6th-stage-1988' not in d]
        return ca_by_stage(input_json)
    elif grouping == 'type':
        filters['$and'] = [d for d in filters['$and'] if 'type' not in d]
        return ca_by_type(input_json)
    elif grouping == 'size':
        filters['$and'] = [d for d in filters['$and'] if 't-size-cm' not in d]
        return ca_by_size(input_json)
    elif grouping == 'race':
        for d in filters['$and']:
            if 'race-ethnicity' in d:
                return ca_by_race(input_json)
        return ca_by_race2(input_json)
    elif grouping == 'cod':
        filters['$and'] = [d for d in filters['$and'] if 'cod-to-site-recode' not in d]
        return ca_cause_of_death(input_json)
    elif grouping == 'radiation':
        filters['$and'] = [d for d in filters['$and'] if 'radiation' not in d]
        return radiation_filter(input_json)
    elif grouping == 'chemo':
        filters['$and'] = [d for d in filters['$and'] if 'chemo' not in d]
        return chemotherapy_filter(input_json)
    elif grouping == 'surgery':
        filters['$and'] = [d for d in filters['$and'] if 'surgery' not in d]
        return ca_by_surgery(input_json)


def survival_months33(input_json, grouping):
    def get_totals(ttf):
        tf120 = copy.deepcopy(ttf)
        tf120['$and'].append({"survival-months": {"$gte": 120}})
        # f120['$and'].append({"year-of-diagnosis": {"$lt": 2010}})
        total120 = json.loads(aggregate([
            {"$match": tf120},
            {"$group": {
                "_id": "",
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}]))
        tf60 = copy.deepcopy(ttf)
        tf60['$and'].append({"survival-months": {"$gte": 60}})
        # f60['$and'].append({"year-of-diagnosis": {"$lt": 2012}})
        total60 = json.loads(aggregate([
            {"$match": tf60},
            {"$group": {
                "_id": "",
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}]))
        tf36 = copy.deepcopy(ttf)
        tf36['$and'].append({"survival-months": {"$gte": 36}})
        # f36['$and'].append({"year-of-diagnosis": {"$gte": 2004}})
        total36 = json.loads(aggregate([
            {"$match": tf36},
            {"$group": {
                "_id": "",
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}]))
        return {'>120': total120[0]['count'], '>60': total60[0]['count'], '>36': total36[0]['count']}

    def get_data(ddf, group):
        if group in ['chemo', 'radiation']:
            ddf['$and'].append({group: "Yes"})
        elif group in ['surgery']:
            ddf['$and'].append({group: {"$nin": ['None']}})
        df120 = copy.deepcopy(ddf)
        df120['$and'].append({"survival-months": {"$gte": 120}})
        # f120['$and'].append({"year-of-diagnosis": {"$gte": 2004}})
        total120 = json.loads(aggregate([
            {"$match": df120},
            {"$group": {
                "_id": "",
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}]))
        df60 = copy.deepcopy(ddf)
        df60['$and'].append({"survival-months": {"$gte": 60}})
        # f60['$and'].append({"year-of-diagnosis": {"$gte": 2004}})
        total60 = json.loads(aggregate([
            {"$match": df60},
            {"$group": {
                "_id": "",
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}]))
        df36 = copy.deepcopy(ddf)
        df36['$and'].append({"survival-months": {"$gte": 36}})
        # f36['$and'].append({"year-of-diagnosis": {"$gte": 2004}})
        total36 = json.loads(aggregate([
            {"$match": df36},
            {"$group": {
                "_id": "",
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}]))
        return {'>120': total120[0]['count'], '>60': total60[0]['count'], '>36': total36[0]['count']}

    def radiation_survival(filters):
        totals = get_totals(filters)
        radiations = get_data(filters, 'radiation')

        data = {'> 120 months': 0, '> 60 months': 0, '> 36 months': 0}
        for months in ['>120', '>60', '>36']:
            if months == '>120':
                if totals[months] > 0:
                    data['> 120 months'] = radiations[months] / totals[months] * 100
                else:
                    data['> 120 months'] = 0
            if months == '>60':
                if totals[months] > 0:
                    data['> 60 months'] = radiations[months] / totals[months] * 100
                else:
                    data['> 60 months'] = 0
            if months == '>36':
                if totals[months] > 0:
                    data['> 36 months'] = radiations[months] / totals[months] * 100
                else:
                    data['> 36 months'] = 0

        return {
            "labels": list(map(lambda x: x, data.keys())),
            "datasets": [{
                "data": list(map(lambda x: x, data.values())),
                "label": "Radiation",
                "borderColor": "#48ccf5",
                "fill": False
            }]
        }

    def chemotherapy_survival(input_json):
        filters = ca_create_filter(input_json)
        totals = get_totals(filters)
        chemos = get_data(filters, 'chemo')

        data = {'> 120 months': 0, '> 60 months': 0, '> 36 months': 0}
        for months in ['>120', '>60', '>36']:
            if months == '>120':
                if totals[months] > 0:
                    data['> 120 months'] = chemos[months] / totals[months] * 100
                else:
                    data['> 120 months'] = 0
            if months == '>60':
                if totals[months] > 0:
                    data['> 60 months'] = chemos[months] / totals[months] * 100
                else:
                    data['> 60 months'] = 0
            if months == '>36':
                if totals[months] > 0:
                    data['> 36 months'] = chemos[months] / totals[months] * 100
                else:
                    data['> 36 months'] = 0

        return {
            "labels": list(map(lambda x: x, data.keys())),
            "datasets": [{
                "data": list(map(lambda x: x, data.values())),
                "label": "Chemotherapy",
                "borderColor": "#48ccf5",
                "fill": False
            }]
        }

    def surgery_survival(input_json):
        filters = ca_create_filter(input_json)
        totals = get_totals(filters)
        surgeries = get_data(filters, 'surgery')

        data = {'> 120 months': 0, '> 60 months': 0, '> 36 months': 0}
        for months in ['>120', '>60', '>36']:
            if months == '>120':
                if totals[months] > 0:
                    data['> 120 months'] = surgeries[months] / totals[months] * 100
                else:
                    data['> 120 months'] = 0
            if months == '>60':
                if totals[months] > 0:
                    data['> 60 months'] = surgeries[months] / totals[months] * 100
                else:
                    data['> 60 months'] = 0
            if months == '>36':
                if totals[months] > 0:
                    data['> 36 months'] = surgeries[months] / totals[months] * 100
                else:
                    data['> 36 months'] = 0

        return {
            "labels": list(map(lambda x: x, data.keys())),
            "datasets": [{
                "data": list(map(lambda x: x, data.values())),
                "label": "Surgery",
                "borderColor": "#48ccf5",
                "fill": False
            }]
        }

    filters = ca_create_filter(input_json)
    if grouping == 'radiation':
        filters['$and'] = [d for d in filters['$and'] if 'radiation' not in d]
        return radiation_survival(filters)
    elif grouping == 'chemo':
        filters['$and'] = [d for d in filters['$and'] if 'chemo' not in d]
        return chemotherapy_survival(filters)
    elif grouping == 'surgery':
        filters['$and'] = [d for d in filters['$and'] if 'surgery' not in d]
        return surgery_survival(filters)


def survival_months22(input_json, grouping):
    def get_totals(filters):
        f120 = copy.deepcopy(filters)
        # f120['$and'].append({"survival-months": {"$gte": 120}})
        f120['$and'].append({"$and": [{"year-of-diagnosis": {"$gte": 2004}},
                                      {"year-of-diagnosis": {"$lte": 2005}}]})
        total120 = json.loads(aggregate([
            {"$match": f120},
            {"$group": {
                "_id": "",
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}]))
        f60 = copy.deepcopy(filters)
        # f60['$and'].append({"survival-months": {"$gte": 60}})
        f60['$and'].append({"$and": [{"year-of-diagnosis": {"$gte": 2004}},
                                     {"year-of-diagnosis": {"$lte": 2010}}]})
        total60 = json.loads(aggregate([
            {"$match": f60},
            {"$group": {
                "_id": "",
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}]))
        f36 = copy.deepcopy(filters)
        # f36['$and'].append({"survival-months": {"$gte": 36}})
        f36['$and'].append({"$and": [{"year-of-diagnosis": {"$gte": 2004}},
                                     {"year-of-diagnosis": {"$lte": 2012}}]})
        total36 = json.loads(aggregate([
            {"$match": f36},
            {"$group": {
                "_id": "",
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}]))
        return {'>120': total120[0]['count'], '>60': total60[0]['count'], '>36': total36[0]['count']}

    def get_data(filters, group):
        if group in ['chemo', 'radiation']:
            filters['$and'].append({group: "Yes"})
        elif group in ['surgery']:
            filters['$and'].append({group: {"$nin": ['None']}})
        pprint(filters)
        filters['$and'].append({"cod-to-site-recode": "Alive"})
        f120 = copy.deepcopy(filters)
        f120['$and'].append({"survival-months": {"$gte": 120}})
        f120['$and'].append({"$and": [{"year-of-diagnosis": {"$gte": 2004}},
                                      {"year-of-diagnosis": {"$lte": 2005}}]})
        pprint(f120)
        total120 = json.loads(aggregate([
            {"$match": f120},
            {"$group": {
                "_id": "",
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}]))
        f60 = copy.deepcopy(filters)
        f60['$and'].append({"survival-months": {"$gte": 60}})
        f60['$and'].append({"$and": [{"year-of-diagnosis": {"$gte": 2004}},
                                     {"year-of-diagnosis": {"$lte": 2005}}]})
        total60 = json.loads(aggregate([
            {"$match": f60},
            {"$group": {
                "_id": "",
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}]))
        f36 = copy.deepcopy(filters)
        f36['$and'].append({"survival-months": {"$gte": 36}})
        f36['$and'].append({"$and": [{"year-of-diagnosis": {"$gte": 2004}},
                                     {"year-of-diagnosis": {"$lte": 2005}}]})
        total36 = json.loads(aggregate([
            {"$match": f36},
            {"$group": {
                "_id": "",
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}]))
        return {'>120': total120[0]['count'], '>60': total60[0]['count'], '>36': total36[0]['count']}

    def radiation_survival(input_json):
        filters = ca_create_filter(input_json)
        totals = get_totals(filters)
        radiations = get_data(filters, 'radiation')
        print(totals)
        print(radiations)

        data = {'> 120 months': 0, '> 60 months': 0, '> 36 months': 0}
        for months in ['>120', '>60', '>36']:
            if months == '>120':
                if totals[months] > 0:
                    data['> 120 months'] = radiations[months] / totals[months] * 100
                else:
                    data['> 120 months'] = 0
            if months == '>60':
                if totals[months] > 0:
                    data['> 60 months'] = radiations[months] / totals[months] * 100
                else:
                    data['> 60 months'] = 0
            if months == '>36':
                if totals[months] > 0:
                    data['> 36 months'] = radiations[months] / totals[months] * 100
                else:
                    data['> 36 months'] = 0

        return {
            "labels": list(map(lambda x: x, data.keys())),
            "datasets": [{
                "data": list(map(lambda x: x, data.values())),
                "label": "Radiation",
                "borderColor": "#48ccf5",
                "fill": False
            }]
        }

    def chemotherapy_survival(input_json):
        filters = ca_create_filter(input_json)
        totals = get_totals(filters)
        chemos = get_data(filters, 'chemo')

        data = {'> 120 months': 0, '> 60 months': 0, '> 36 months': 0}
        for months in ['>120', '>60', '>36']:
            if months == '>120':
                if totals[months] > 0:
                    data['> 120 months'] = chemos[months] / totals[months] * 100
                else:
                    data['> 120 months'] = 0
            if months == '>60':
                if totals[months] > 0:
                    data['> 60 months'] = chemos[months] / totals[months] * 100
                else:
                    data['> 60 months'] = 0
            if months == '>36':
                if totals[months] > 0:
                    data['> 36 months'] = chemos[months] / totals[months] * 100
                else:
                    data['> 36 months'] = 0

        return {
            "labels": list(map(lambda x: x, data.keys())),
            "datasets": [{
                "data": list(map(lambda x: x, data.values())),
                "label": "Chemotherapy",
                "borderColor": "#48ccf5",
                "fill": False
            }]
        }

    def surgery_survival(input_json):
        filters = ca_create_filter(input_json)
        totals = get_totals(filters)
        surgeries = get_data(filters, 'surgery')

        data = {'> 120 months': 0, '> 60 months': 0, '> 36 months': 0}
        for months in ['>120', '>60', '>36']:
            if months == '>120':
                if totals[months] > 0:
                    data['> 120 months'] = surgeries[months] / totals[months] * 100
                else:
                    data['> 120 months'] = 0
            if months == '>60':
                if totals[months] > 0:
                    data['> 60 months'] = surgeries[months] / totals[months] * 100
                else:
                    data['> 60 months'] = 0
            if months == '>36':
                if totals[months] > 0:
                    data['> 36 months'] = surgeries[months] / totals[months] * 100
                else:
                    data['> 36 months'] = 0

        return {
            "labels": list(map(lambda x: x, data.keys())),
            "datasets": [{
                "data": list(map(lambda x: x, data.values())),
                "label": "Surgery",
                "borderColor": "#48ccf5",
                "fill": False
            }]
        }

    filters = ca_create_filter(input_json)
    if grouping == 'radiation':
        filters['$and'] = [d for d in filters['$and'] if 'radiation' not in d]
        return radiation_survival(input_json)
    elif grouping == 'chemo':
        filters['$and'] = [d for d in filters['$and'] if 'chemo' not in d]
        return chemotherapy_survival(input_json)
    elif grouping == 'surgery':
        filters['$and'] = [d for d in filters['$and'] if 'surgery' not in d]
        return surgery_survival(input_json)


def survival_months(input_json, grouping):
    def get_totals(subfilters, group):
        tot_filter = copy.deepcopy(subfilters)
        tot_filter['$and'].append({"cod-to-site-recode": {"$nin": ['']}})
        # pprint(tot_filter)
        tf120 = copy.deepcopy(tot_filter)
        tf120['$and'].append({"$and": [{"year-of-diagnosis": {"$gte": 2004}},
                                       {"year-of-diagnosis": {"$lte": 2005}}]})
        # pprint(tf120)
        res120 = json.loads(aggregate([
            {"$match": tf120},
            {"$group": {
                "_id": "",
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}]))
        total120 = res120[0]['count'] if len(res120) > 0 else 0

        tf60 = copy.deepcopy(tot_filter)
        tf60['$and'].append({"$and": [{"year-of-diagnosis": {"$gte": 2004}},
                                      {"year-of-diagnosis": {"$lte": 2009}}]})
        res60 = json.loads(aggregate([
            {"$match": tf60},
            {"$group": {
                "_id": "",
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}]))
        total60 = res60[0]['count'] if len(res60) > 0 else 0

        tf36 = copy.deepcopy(tot_filter)
        tf36['$and'].append({"$and": [{"year-of-diagnosis": {"$gte": 2004}},
                                      {"year-of-diagnosis": {"$lte": 2011}}]})
        res36 = json.loads(aggregate([
            {"$match": tf36},
            {"$group": {
                "_id": "",
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}]))
        total36 = res36[0]['count'] if len(res36) > 0 else 0
        return {'>120': total120, '>60': total60, '>36': total36}

    def get_data(subfilters, group):
        dat_filter = copy.deepcopy(subfilters)
        dat_filter['$and'].append({"cod-to-site-recode": "Alive"})
        # pprint(dat_filter)
        df120 = copy.deepcopy(dat_filter)
        df120['$and'].append({"$and": [{"year-of-diagnosis": {"$gte": 2004}},
                                       {"year-of-diagnosis": {"$lte": 2005}}]})
        # pprint(df120)
        res120 = json.loads(aggregate([
            {"$match": df120},
            {"$group": {
                "_id": "",
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}]))
        total120 = res120[0]['count'] if len(res120) > 0 else 0

        df60 = copy.deepcopy(dat_filter)
        df60['$and'].append({"$and": [{"year-of-diagnosis": {"$gte": 2004}},
                                      {"year-of-diagnosis": {"$lte": 2009}}]})
        res60 = json.loads(aggregate([
            {"$match": df60},
            {"$group": {
                "_id": "",
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}]))
        total60 = res60[0]['count'] if len(res60) > 0 else 0

        df36 = copy.deepcopy(dat_filter)
        df36['$and'].append({"$and": [{"year-of-diagnosis": {"$gte": 2004}},
                                      {"year-of-diagnosis": {"$lte": 2011}}]})
        res36 = json.loads(aggregate([
            {"$match": df36},
            {"$group": {
                "_id": "",
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}]))
        total36 = res36[0]['count'] if len(res36) > 0 else 0
        return {'>120': total120, '>60': total60, '>36': total36}

    def survival(sfilter, label):
        totals = get_totals(sfilter, grouping)
        # pprint(totals)
        surgeries = get_data(sfilter, grouping)
        # pprint(surgeries)

        data = {'> 120 months': 0, '> 60 months': 0, '> 36 months': 0}
        for months in ['>120', '>60', '>36']:
            if months == '>120':
                if totals[months] > 0:
                    data['> 120 months'] = surgeries[months] / totals[months] * 100
                else:
                    data['> 120 months'] = 0
            if months == '>60':
                if totals[months] > 0:
                    data['> 60 months'] = surgeries[months] / totals[months] * 100
                else:
                    data['> 60 months'] = 0
            if months == '>36':
                if totals[months] > 0:
                    data['> 36 months'] = surgeries[months] / totals[months] * 100
                else:
                    data['> 36 months'] = 0

        return {
            "labels": list(map(lambda x: x, data.keys())),
            "datasets": [{
                "data": list(map(lambda x: x, data.values())),
                "label": label,
                "borderColor": "#48ccf5",
                "fill": False
            }]
        }

    filters = ca_create_filter(input_json)
    if grouping == 'radiation':
        rad_yes_filter = {"$and": [d for d in filters['$and'] if 'radiation' not in d]}
        rad_yes_filter["$and"].append({"radiation": "Yes"})
        rad_no_filter = {"$and": [d for d in filters['$and'] if 'radiation' not in d]}
        rad_no_filter["$and"].append({"radiation": "No"})
        return survival(rad_yes_filter, 'yes'), survival(rad_no_filter, 'no')
    elif grouping == 'chemo':
        chemo_yes_filter = {"$and": [d for d in filters['$and'] if 'chemo' not in d]}
        chemo_yes_filter["$and"].append({"chemo": "Yes"})
        chemo_no_filter = {"$and": [d for d in filters['$and'] if 'chemo' not in d]}
        chemo_no_filter["$and"].append({"chemo": "No"})
        return survival(chemo_yes_filter, 'yes'), survival(chemo_no_filter, 'no')
    elif grouping in ['Bi-Lateral Mastectomy', 'Lumpectomy', 'Mastectomy']:
        surgery_yes_filter = {"$and": [d for d in filters['$and'] if 'chemo' not in d]}
        if grouping == 'Lumpectomy':
            surgery_yes_filter['$and'].append({'surgery': {"$in": ['Lumpectomy', 'Partial Mastectomy']}})
        elif grouping == 'Mastectomy':
            surgery_yes_filter['$and'].append({"$or": [{'surgery': 'Single Mastectomy'},
                                                       {'surgery': 'Mastectomy '},
                                                       {'surgery': 'Simple Mastectomy'}, ]})
        elif grouping == 'Bi-Lateral Mastectomy':
            surgery_yes_filter['$and'].append({'surgery': {"$in": ['Bi-Lateral Mastectomy']}})
        surgery_no_filter = {"$and": [d for d in filters['$and'] if 'chemo' not in d]}
        surgery_no_filter['$and'].append({'surgery': {"$in": ['None']}})
        return survival(surgery_yes_filter, 'yes'), survival(surgery_no_filter, 'no')


def survival_months2(input_json):
    def get_totals(subfilters):
        tot_filter = copy.deepcopy(subfilters)
        tot_filter['$and'].append({"cod-to-site-recode": {"$nin": ['']}})
        # pprint(tot_filter)
        tf120 = copy.deepcopy(tot_filter)
        tf120['$and'].append({"$and": [{"year-of-diagnosis": {"$gte": 2004}},
                                       {"year-of-diagnosis": {"$lte": 2005}}]})
        # pprint(tf120)
        res120 = json.loads(aggregate([
            {"$match": tf120},
            {"$group": {
                "_id": "",
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}]))
        total120 = res120[0]['count'] if len(res120) > 0 else 0

        tf60 = copy.deepcopy(tot_filter)
        tf60['$and'].append({"$and": [{"year-of-diagnosis": {"$gte": 2009}},
                                      {"year-of-diagnosis": {"$lte": 2010}}]})
        res60 = json.loads(aggregate([
            {"$match": tf60},
            {"$group": {
                "_id": "",
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}]))
        total60 = res60[0]['count'] if len(res60) > 0 else 0

        tf36 = copy.deepcopy(tot_filter)
        tf36['$and'].append({"$and": [{"year-of-diagnosis": {"$gte": 2011}},
                                      {"year-of-diagnosis": {"$lte": 2012}}]})
        res36 = json.loads(aggregate([
            {"$match": tf36},
            {"$group": {
                "_id": "",
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}]))
        total36 = res36[0]['count'] if len(res36) > 0 else 0
        return {'>120': total120, '>60': total60, '>36': total36}

    def get_data(subfilters):
        dat_filter = copy.deepcopy(subfilters)
        dat_filter['$and'].append({"cod-to-site-recode": "Alive"})
        # pprint(dat_filter)
        df120 = copy.deepcopy(dat_filter)
        df120['$and'].append({"$and": [{"year-of-diagnosis": {"$gte": 2004}},
                                       {"year-of-diagnosis": {"$lte": 2005}}]})
        # pprint(df120)
        res120 = json.loads(aggregate([
            {"$match": df120},
            {"$group": {
                "_id": "",
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}]))
        total120 = res120[0]['count'] if len(res120) > 0 else 0

        df60 = copy.deepcopy(dat_filter)
        df60['$and'].append({"$and": [{"year-of-diagnosis": {"$gte": 2009}},
                                      {"year-of-diagnosis": {"$lte": 2010}}]})
        res60 = json.loads(aggregate([
            {"$match": df60},
            {"$group": {
                "_id": "",
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}]))
        total60 = res60[0]['count'] if len(res60) > 0 else 0

        df36 = copy.deepcopy(dat_filter)
        df36['$and'].append({"$and": [{"year-of-diagnosis": {"$gte": 2011}},
                                      {"year-of-diagnosis": {"$lte": 2012}}]})
        res36 = json.loads(aggregate([
            {"$match": df36},
            {"$group": {
                "_id": "",
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}]))
        total36 = res36[0]['count'] if len(res36) > 0 else 0
        return {'>120': total120, '>60': total60, '>36': total36}

    def survival(sfilter, label):
        totals = get_totals(sfilter)
        pprint(totals)
        treatment = get_data(sfilter)
        pprint(treatment)

        data = {'> 120 months': 0, '> 60 months': 0, '> 36 months': 0}
        for months in ['>120', '>60', '>36']:
            if months == '>120':
                if totals[months] > 0:
                    data['> 120 months'] = treatment[months] / totals[months] * 100
                else:
                    data['> 120 months'] = 0
            if months == '>60':
                if totals[months] > 0:
                    data['> 60 months'] = treatment[months] / totals[months] * 100
                else:
                    data['> 60 months'] = 0
            if months == '>36':
                if totals[months] > 0:
                    data['> 36 months'] = treatment[months] / totals[months] * 100
                else:
                    data['> 36 months'] = 0

        return {
            "labels": list(map(lambda x: x, data.keys())),
            "datasets": [{
                "data": list(map(lambda x: x, data.values())),
                "label": label,
                "borderColor": "#48ccf5",
                "fill": False
            }]
        }

    filters = ca_create_filter(input_json)
    wot = {"$and": []}
    for f in filters['$and']:
        for k, v in f.items():
            if k not in ['chemo', 'radiation', 'surgery']:
                wot['$and'].append(f)
    wot['$and'].append({"chemo": "No"})
    # wot['$and'].append({"radiation": "No"})
    # wot['$and'].append({"surgery": "None"})

    return survival(filters, 'treatment'), survival(wot, 'w/o treatment')


if __name__ == '__main__':
    ca_diag_request = '{"1age": 35, ' \
                      '"1sex": "Female", ' \
                      '"1tumor_grade": 1, ' \
                      '"1er_status": "+", ' \
                      '"1pr_status": "+", ' \
                      '"1tumor_size": "2-5cm", ' \
                      '"1num_pos_nodes": "4-8", ' \
                      '"1her2_status": "+", ' \
                      '"1tumor_number": 1, ' \
                      '"stage": "IIA", ' \
                      '"chemo": "Yes", ' \
                      '"radiation": "Yes", ' \
                      '"surgery": "Lumpectomy", ' \
                      '"1ethnicity": "Japanese"}'

    # pprint(display_group('surgery'))

    # pprint(survival_months(ca_diag_request, 'chemo'))
    # pprint(survival_months(ca_diag_request, 'radiation'))
    # pprint(survival_months(ca_diag_request, 'Mastectomy'))
    pprint(survival_months2(ca_diag_request))

    exit()
    find_request = '{"1age": 35, ' \
                   '"1sex": "Female", ' \
                   '"1tumor_grade": 1, ' \
                   '"1er_status": "+", ' \
                   '"1pr_status": "+", ' \
                   '"1tumor_size": "2-5cm", ' \
                   '"1num_pos_nodes": "4-8", ' \
                   '"1her2_status": "+", ' \
                   '"1tumor_number": "1", ' \
                   '"stage": "IIA", ' \
                   '"1ethnicity": "Japanese"}'
    filter = ca_create_filter(find_request)
    filter['$and'].append({"cod-to-site-recode": {"$nin": ['']}})
    # filter['$and'].append({"cod-to-site-recode": "Alive"})
    filter['$and'].append({"chemo": "Yes"})
    filter['$and'].append({"$and": [{"year-of-diagnosis": {"$gte": 2004}},
                                    {"year-of-diagnosis": {"$lte": 2005}}]})
    pprint(filter)
    count = json.loads(aggregate([
        {"$match": filter},
        {"$group": {
            "_id": "",
            "count": {"$sum": 1}}},
        {"$sort": SON([("_id", 1)])}]))
    pprint(count)

    # ca_find_request = '{"ethnicity": "Chinese"}'
    # filters = ca_create_filter(ca_diag_request)
    # print(len(find(filters, limit=100)))
    # pprint(custom_analytics(ca_diag_request, 'size'))
    # pprint(custom_analytics(ca_diag_request, 'grade'))
