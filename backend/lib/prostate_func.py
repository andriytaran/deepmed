import json, time
from collections import OrderedDict
from pymongo import MongoClient
from bson.son import SON
from pprint import pprint

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'prostate'
COLLECTION_NAME = 'dataset2'


def aggregate(request, collection=None):
    response = []
    if collection:
        data = collection.aggregate(request)
    else:
        mongo_client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        collection = mongo_client[DBS_NAME][COLLECTION_NAME]
        data = collection.aggregate(request)
    for row in data:
        response.append(row)
    return json.dumps(response)


def find(request, collection=None, **kwargs):
    response = []
    if collection:
        data = collection.find(request, **kwargs)
    else:
        mongo_client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        collection = mongo_client[DBS_NAME][COLLECTION_NAME]
        data = collection.find(request, **kwargs)
    for row in data:
        response.append(row)
    return response


def display_group(group, collection=None):
    if group:
        group = '$' + str(group)
        result = json.loads(aggregate([
            {"$group": {
                "_id": group,
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}], collection))
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
        age_group = ["00 years", "00-04 years", "05-09 years"]
    return age_group


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


def get_race(race):
    if race == "White":
        return "Caucasian"
    elif race == "Black":
        return "African American"
    elif race == "Asian or Pacific Islander":
        return "Asian"
    elif race in ['Unknown', 'American Indian/Alaska Native']:
        return "Other"
    else:
        return race


def get_t_size_cm(mm):
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
    elif race == 'Asian':
        race_group = ['Pacific Islander, NOS (1991+)', 'Samoan (1991+)', 'Tongan (1991+)', 'Fiji Islander (1991+)',
                      'Guamanian, NOS (1991+)', 'Micronesian, NOS (1991+)', 'Melanesian, NOS (1991+)',
                      'Polynesian, NOS (1991+)', 'New Guinean (1991+)', 'Chamorran (1991+)', 'Tahitian (1991+)',
                      'Filipino', 'Chinese', 'Hmong (1988+)', 'Japanese', 'Other Asian (1991+)', 'Kampuchean (1988+)',
                      'Laotian (1988+)', 'Korean (1988+)', 'Vietnamese (1988+)', 'Asian Indian (2010+)',
                      'Asian Indian or Pakistani, NOS (1988+)', 'Pakistani (2010+)', 'Thai (1994+)']
    elif race == 'Other':
        race_group = ['Unknown', 'NOS (1988+)', 'Other', 'NOS (1991+)']

    return race_group


def create_filter(input_data, operator='$and'):
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
                   '"tumor_size_in_mm": int, ' \
                   '"num_pos_nodes": int, ' \
                   '"her2_status": "+" or "-", ' \
                   '"ethnicity": string}'
    :param operator: {"$and"} or {"or"} as filtering operators
    :return: list of dicts
    """
    input_data = json.loads(input_data)
    filter_list = [{"sex": "Male"}]
    if 'age' in input_data.keys():
        age = get_age_group(input_data['age'])
        filter_list.append({"age-range": {"$in": age}})
    if 'chemo' in input_data.keys():
        if input_data['chemo'] == 'No':
            input_data['chemo'] = 'No/Unknown'
        filter_list.append({"chemo": input_data["chemo"]})
    if 'ethnicity' in input_data.keys():
        filter_list.append({"race": input_data["ethnicity"]})
    if 'gleason-pri' in input_data.keys() and 'gleason-sec' in input_data.keys():
        glpri = int(input_data['gleason-pri'])
        glsec = int(input_data['gleason-sec'])
        if glpri == 1:
            gleason = 10 + glsec
        elif glpri == 2:
            gleason = 20 + glsec
        elif glpri == 3:
            gleason = 30 + glsec
        elif glpri == 4:
            gleason = 40 + glsec
        elif glpri == 5:
            gleason = 50 + glsec
        filter_list.append({"gleason": gleason})
    if 'pas' in input_data.keys():
        filter_list.append({"psa-value": input_data["psa"]})
    if 'radiation' in input_data.keys():
        filter_list.append({"radiation": input_data["radiation"]})
    if 'surgery' in input_data.keys():
        filter_list.append({"surgery": input_data["surgery"]})
    if 'tumor_size_mm' in input_data.keys():
        t_size_cm = get_t_size_cm(input_data['tumor_size_mm'])
        filter_list.append({"t-size-cm": t_size_cm})

    return {operator: filter_list}


def diagnosis(input_json, limit=20, collection=None):
    """
    Returned values are grouped by these groups:
    "ethnicity": "White" -> "Caucasian", "Black" -> "African American", "Asian or Pacific Islander" -> "Asian",
        ['Unknown', 'American Indian/Alaska Native'] -> "Other"
    "cod": "Alive" -> "Alive", "Breast" -> "Breast", any_other_value -> "Other"
    Other values are returned as in database
    :param input_json: json
    :param limit: int
    :return: list
    """

    def get_race(race):
        if race == "White":
            return "Caucasian"
        elif race == "Black":
            return "African American"
        elif race == "Asian or Pacific Islander":
            return "Asian"
        elif race in ['Unknown', 'American Indian/Alaska Native']:
            return "Other"
        else:
            return race

    def get_cod(cod):
        if cod not in ['Alive', 'Breast']:
            return "Other"
        else:
            return cod

    def build_dict(item):
        return {'age': item['age-recode-with-single-ages-and-85'],
                'ethnicity': get_race(item['race-recode-w-b-ai-api']),
                'size': item['t-size-cm'],
                'grade': item['grade'],
                'er': item['er-status-recode-breast-cancer-1990'],
                'pr': item['pr-status-recode-breast-cancer-1990'],
                'her2': item['derived-her2-recode-2010'],
                'lat': item['laterality'],
                'site': item['primary-site-labeled'],
                'type': item['type'],
                'stage': item['breast-adjusted-ajcc-6th-stage-1988'],
                '+nodes': item['regional-nodes-positive-1988'],
                'surgery': item['surgery'],
                'chemo': item['chemo'],
                'radiation': item['radiation'],
                'year dx': item['year-of-diagnosis'],
                'survival mos.': item['survival-months'],
                'cod': get_cod(item['cod-to-site-recode'])}

    filters = create_filter(input_json)
    dataset = find(filters, limit=limit)
    results = []
    for item in dataset:
        d = build_dict(item)
        results.append(d)

    if len(results) < 20:
        # print(len(results))
        filters['$and'] = [d for d in filters['$and'] if 't-size-cm' not in d]
        # ts_mm = json.loads(input_json)['tumor_size_in_mm']
        # ts_min = round(ts_mm * 0.8)
        # ts_max = round(ts_mm *1.2)
        # filters['$and'].append({"$and": [{"tumor_size_in_mm": {"$gte": ts_min}},
        #                                  {"tumor_size_in_mm": {"$lte": ts_max}}]})
        dataset = find(filters, limit=limit, collection=collection)
        results = []
        for item in dataset:
            d = build_dict(item)
            results.append(d)
        if len(results) < 20:
            filters['$and'] = [d for d in filters['$and'] if 'race-recode-w-b-ai-api' not in d]
            dataset = find(filters, limit=limit, collection=collection)
            results = []
            for item in dataset:
                d = build_dict(item)
                results.append(d)
            if len(results) < 20:
                filters['$and'] = [d for d in filters['$and'] if 'age-recode-with-single-ages-and-85' not in d]
                dataset = find(filters, limit=limit, collection=collection)
                results = []
                for item in dataset:
                    d = build_dict(item)
                    results.append(d)
                return results
            return results
        return results
    return results


def percent_men_annualy_diagnosed(input_json, collection=None):
    """
    men age xx-xx as a % of total prostate diagnoses
    :param input_json:
    :param collection:
    :return:
    """

    def get_total(year):
        ff = {"$and": [{"year-of-diagnosis": {"$gte": year}},
                       {"year-of-diagnosis": {"$lt": year + 5}}]}
        total = json.loads(aggregate([
            {"$match": ff},
            {"$group": {
                "_id": "",
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}], collection))
        return total[0]['count']

    def get_by_age(only_age, year):
        ff = create_filter(json.dumps(only_age))
        ff['$and'].append({"$and": [{"year-of-diagnosis": {"$gte": year}},
                                    {"year-of-diagnosis": {"$lt": year + 5}}]})
        by_age = json.loads(aggregate([
            {"$match": ff},
            {"$group": {
                "_id": "",
                "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])}], collection))
        return by_age[0]['count']

    def get_percent(only_age, year):
        return get_by_age(only_age, year) / get_total(year) * 100

    only_age = {"age": json.loads(input_json)['age']}

    data = {"1975-1979": 0, "1980-1984": 0, "1985-1989": 0, "1990-1994": 0, "1995-1999": 0,
            "2000-2004": 0, "2005-2009": 0, "2010-2014": 0}
    for year in [1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010]:
        if year == 1975:
            data['1975-1979'] = get_percent(only_age, year)
        if year == 1980:
            data['1980-1984'] = get_percent(only_age, year)
        if year == 1985:
            data['1985-1989'] = get_percent(only_age, year)
        if year == 1990:
            data['1990-1994'] = get_percent(only_age, year)
        if year == 1995:
            data['1995-1999'] = get_percent(only_age, year)
        if year == 2000:
            data['2000-2004'] = get_percent(only_age, year)
        if year == 2005:
            data['2005-2009'] = get_percent(only_age, year)
        if year == 2010:
            data['2010-2014'] = get_percent(only_age, year)

    return {
        'labels': list(map(lambda x: x, data.keys())),
        'datasets': [{
            'data': list(map(lambda x: x, data.values())),
            'label': "Diagnosed",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def percent_race_by_age(input_json, collection=None):
    """
    percent of men with prostate by ethnicity for overall and this age group
    :param input_json:
    :param collection:
    :return:
    """
    filters = create_filter(input_json)
    filters['and'] = [d for d in filters['$and'] if 'race' not in d]
    result = json.loads(aggregate([
        {"$match": filters},
        {"$group": {
            "_id": "",
            "total": {"$sum": 1},
            "race_set": {"$push": "$race"}
        }},
        {"$unwind": "$race_set"},
        {"$group": {
            "_id": {"race": "$race_set", "total": "$total"},
            "count": {"$sum": 1}
        }},
        {"$project": {
            "count": 1,
            "percentage": {"$multiply": [{"$divide": [100, "$_id.total"]}, "$count"], }
        }},
        {"$sort": SON([("percentage", -1)])}], collection))

    data = OrderedDict()
    data['Other'] = 0
    data['Caucasian'] = 0
    data['African American'] = 0
    data['Asian'] = 0
    data['Hispanic'] = 0
    for i, label in enumerate(list(map(lambda x: x['_id']['race'], result))):
        if label == 'White':
            data['Caucasian'] += result[i]['percentage']
        elif label == 'Black':
            data['African American'] += result[i]['percentage']
        elif label == 'Hispanic':
            data['Hispanic'] += result[i]['percentage']
        elif label == 'Asian or Pacific Islander':
            data['Asian'] += result[i]['percentage']
        elif label in ['Unknown', 'American Indian/Alaska Native'] or label is None:
            data['Other'] += result[i]['percentage']
    data.move_to_end("Other")

    return {
        'labels': list(map(lambda x: x, data.keys())),
        'datasets': [{
            'data': list(map(lambda x: x, data.values())),
            'label': "Diagnosed",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def distribution_by_stage(input_json, collection=None):
    """
    percent of men with prostate cancer by stage for overall and this ethnic group
    :param input_json:
    :param collection:
    :return:
    """
    filters = create_filter(input_json)
    filters['$and'] = [d for d in filters['$and'] if 'stage' not in d]
    filters['$and'].append({"stage": {"$nin": [None]}})
    result = json.loads(aggregate([
        {"$match": filters},
        {"$group": {
            "_id": "",
            "total": {"$sum": 1},
            "subset": {"$push": "$stage"}
        }},
        {"$unwind": "$subset"},
        {"$group": {
            "_id": {"stage": "$subset", "total": "$total"},
            "count": {"$sum": 1}
        }},
        {"$project": {
            "count": 1,
            "percentage": {"$multiply": [{"$divide": [100, "$_id.total"]}, "$count"], }
        }},
        {"$sort": SON([("percentage", -1)])}], collection))

    data = {"I": 0, "II": 0, "III": 0, "IV": 0}
    for i, label in enumerate(list(map(lambda x: x['_id']['stage'], result))):
        if label == 'I':
            data['I'] = result[i]['percentage']
        elif label in ['II', 'IIA', 'IIB']:
            data['II'] += result[i]['percentage']
        elif label in ['III']:
            data['III'] += result[i]['percentage']
        elif label == 'IV':
            data['IV'] = result[i]['percentage']

    return {
        'labels': list(map(lambda x: x, data.keys())),
        'datasets': [{
            'data': list(map(lambda x: x, data.values())),
            'label': "Stage",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def surgery_decisions(input_json, collection=None):
    """
    surgery decision for men by overall and this age group
    :param input_json:
    :param collection:
    :return:
    """
    filters = create_filter(input_json)
    filters['$and'] = [d for d in filters['$and'] if 'surgery' not in d]
    filters['$and'].append({"surgery": {"$nin": [None]}})
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
        {"$sort": SON([("percentage", -1)])}], collection))

    return {
        'labels': list(map(lambda x: x['_id']['surgery'], result)),
        'datasets': [{
            'data': list(map(lambda x: x['percentage'], result)),
            'label': "Surgeries",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def chemo_decisions(input_json, collection=None):
    """
    surgery decision for men by overall and this age group
    :param input_json:
    :param collection:
    :return:
    """
    filters = create_filter(input_json)
    filters['$and'] = [d for d in filters['$and'] if 'surgery' not in d]
    filters['$and'].append({"chemo": {"$nin": [None]}})
    result = json.loads(aggregate([
        {"$match": filters},
        {"$group": {
            "_id": "",
            "total": {"$sum": 1},
            "surgery_set": {"$push": "$chemo"}
        }},
        {"$unwind": "$surgery_set"},
        {"$group": {
            "_id": {"chemo": "$surgery_set", "total": "$total"},
            "count": {"$sum": 1}
        }},
        {"$project": {
            "count": 1,
            "percentage": {"$multiply": [{"$divide": [100, "$_id.total"]}, "$count"], }
        }},
        {"$sort": SON([("percentage", -1)])}], collection))

    return {
        'labels': list(map(lambda x: x['_id']['chemo'], result)),
        'datasets': [{
            'data': list(map(lambda x: x['percentage'], result)),
            'label': "Chemotherapy",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def radiation_decisions(input_json, collection=None):
    """
    surgery decision for men by overall and this age group
    :param input_json:
    :param collection:
    :return:
    """
    filters = create_filter(input_json)
    filters['$and'] = [d for d in filters['$and'] if 'radiation' not in d]
    filters['$and'].append({"radiation": {"$nin": [None]}})
    result = json.loads(aggregate([
        {"$match": filters},
        {"$group": {
            "_id": "",
            "total": {"$sum": 1},
            "surgery_set": {"$push": "$radiation"}
        }},
        {"$unwind": "$surgery_set"},
        {"$group": {
            "_id": {"radiation": "$surgery_set", "total": "$total"},
            "count": {"$sum": 1}
        }},
        {"$project": {
            "count": 1,
            "percentage": {"$multiply": [{"$divide": [100, "$_id.total"]}, "$count"], }
        }},
        {"$sort": SON([("percentage", -1)])}], collection))

    return {
        'labels': list(map(lambda x: x['_id']['radiation'], result)),
        'datasets': [{
            'data': list(map(lambda x: x['percentage'], result)),
            'label': "Radiation",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def breakout_by_gleason(input_json, collection=None):
    """
    prostate cancer breakout by gleason score for this age group - two digit Gleason and single digit Gleason
    :param input_json:
    :param collection:
    :return:
    """
    filters = create_filter(input_json)
    filters['$and'] = [d for d in filters['$and'] if 'gleason' not in d]
    filters['$and'].append({"gleason": {"$nin": [None, 19, 29, 39, 49, 59]}})
    result = json.loads(aggregate([
        {"$match": filters},
        {"$group": {
            "_id": "$gleason",
            "count": {"$sum": 1}}},
        {"$sort": SON([("_id", 1)])}], collection))

    return {
        'labels': list(map(lambda x: x['_id'], result)),
        'datasets': [{
            'data': list(map(lambda x: x['count'], result)),
            'label': "Diagnosed",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def breakout_by_gleason_comb(input_json, collection=None):
    """
    prostate cancer breakout by gleason score for this age group - two digit Gleason and single digit Gleason
    :param input_json:
    :param collection:
    :return:
    """
    filters = create_filter(input_json)
    filters['$and'] = [d for d in filters['$and'] if 'gleason-comb-recode' not in d]
    filters['$and'].append({"gleason-comb-recode": {"$nin": [None]}})
    result = json.loads(aggregate([
        {"$match": filters},
        {"$group": {
            "_id": "$gleason-comb-recode",
            "count": {"$sum": 1}}},
        {"$sort": SON([("_id", 1)])}], collection))

    return {
        'labels': list(map(lambda x: x['_id'], result)),
        'datasets': [{
            'data': list(map(lambda x: x['count'], result)),
            'label': "Diagnosed",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def prostate_cancer_by_size(input_json, collection=None):
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

    if 'age' in json.loads(input_json):
        only_age = {"age": json.loads(input_json)['age']}
        filters = create_filter(json.dumps(only_age))
    else:
        filters = create_filter(input_json)
    filters['$and'] = [d for d in filters['$and'] if 't-size-mm' not in d]
    filters['$and'] = [d for d in filters['$and'] if 't-size-cm' not in d]
    sizes = ['< 1cm', '< 2cm', '< 3cm', '< 5cm', '> 5cm', 'Micro']
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
        {"$sort": SON([("percentage", -1)])}], collection))

    data = {'< 2cm': 0, '< 5cm': 0, '> 5cm': 0}
    for i, label in enumerate(list(map(lambda x: x['_id']['t-size-cm'], result))):
        if label == '< 1cm':
            data['< 1cm'] += result[i]['percentage']
        elif label == '< 2cm':
            data['< 2cm'] += result[i]['percentage']
        elif label == '< 3cm':
            data['< 5cm'] += result[i]['percentage']
        elif label == '< 5cm':
            data['< 5cm'] += result[i]['percentage']
        elif label == '> 5cm':
            data['> 5cm'] += result[i]['percentage']
        elif label == 'Micro':
            data['< 1cm'] += result[i]['percentage']

    return {
        'labels': list(map(lambda x: x, data.keys())),
        'datasets': [{
            'data': list(map(lambda x: x, data.values())),
            'label': "Diagnosed",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def distribution_by_psa(input_json, collection=None):
    """
    prostate cancer breakout by gleason score for this age group - two digit Gleason and single digit Gleason
    :param input_json:
    :param collection:
    :return:
    """
    filters = create_filter(input_json)
    filters['$and'] = [d for d in filters['$and'] if 'psa-value' not in d]
    filters['$and'].append({"psa-value": {"$nin": [None]}})
    result = json.loads(aggregate([
        {"$match": filters},
        {"$group": {
            "_id": "",
            "total": {"$sum": 1},
            "subset": {"$push": "$psa-value"}
        }},
        {"$unwind": "$subset"},
        {"$group": {
            "_id": {"psa-value": "$subset", "total": "$total"},
            "count": {"$sum": 1}
        }},
        {"$project": {
            "count": 1,
            "percentage": {"$multiply": [{"$divide": [100, "$_id.total"]}, "$count"], }
        }},
        {"$sort": SON([("percentage", -1)])}], collection))

    data = {"0-20ML": 0, "20-40ML": 0, "40-60ML": 0, "60-80ML": 0, ">80ML": 0}
    for i, label in enumerate(list(map(lambda x: x['_id']['psa-value'], result))):
        if label < 200:
            data['0-20ML'] += result[i]['percentage']
        elif label < 400:
            data['20-40ML'] += result[i]['percentage']
        elif label < 600:
            data['40-60ML'] += result[i]['percentage']
        elif label < 800:
            data['60-80ML'] += result[i]['percentage']
        elif label <= 980:
            data['>80ML'] += result[i]['percentage']

    return {
        'labels': list(map(lambda x: x, data.keys())),
        'datasets': [{
            'data': list(map(lambda x: x, data.values())),
            'label': "Stage",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def distribution_by_gleason_pri(input_json, collection=None):
    """
    prostate cancer breakout by gleason score for this age group - two digit Gleason and single digit Gleason
    :param input_json:
    :param collection:
    :return:
    """
    filters = create_filter(input_json)
    filters['$and'] = [d for d in filters['$and'] if 'gleason' not in d]
    filters['$and'].append({"gleason": {"$nin": [None, 19, 29, 39, 49, 59]}})
    result = json.loads(aggregate([
        {"$match": filters},
        {"$group": {
            "_id": "",
            "total": {"$sum": 1},
            "subset": {"$push": "$gleason"}
        }},
        {"$unwind": "$subset"},
        {"$group": {
            "_id": {"gleason": "$subset", "total": "$total"},
            "count": {"$sum": 1}
        }},
        {"$project": {
            "count": 1,
            "percentage": {"$multiply": [{"$divide": [100, "$_id.total"]}, "$count"], }
        }},
        {"$sort": SON([("percentage", -1)])}], collection))

    data = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
    for i, label in enumerate(list(map(lambda x: x['_id']['gleason'], result))):
        if label in [11, 12, 13, 14, 15]:
            data['1'] += result[i]['percentage']
        elif label in [21, 22, 23, 24, 25]:
            data['2'] += result[i]['percentage']
        elif label in [31, 32, 33, 34, 35]:
            data['3'] += result[i]['percentage']
        elif label in [41, 42, 43, 44, 45]:
            data['4'] += result[i]['percentage']
        elif label in [51, 52, 53, 54, 55]:
            data['5'] += result[i]['percentage']

    return {
        'labels': list(map(lambda x: x, data.keys())),
        'datasets': [{
            'data': list(map(lambda x: x, data.values())),
            'label': "Gleason primary",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def distribution_by_gleason_sec(input_json, collection=None):
    """
    prostate cancer breakout by gleason score for this age group - two digit Gleason and single digit Gleason
    :param input_json:
    :param collection:
    :return:
    """
    filters = create_filter(input_json)
    filters['$and'] = [d for d in filters['$and'] if 'gleason' not in d]
    filters['$and'].append({"gleason": {"$nin": [None, 19, 29, 39, 49, 59]}})
    result = json.loads(aggregate([
        {"$match": filters},
        {"$group": {
            "_id": "",
            "total": {"$sum": 1},
            "subset": {"$push": "$gleason"}
        }},
        {"$unwind": "$subset"},
        {"$group": {
            "_id": {"gleason": "$subset", "total": "$total"},
            "count": {"$sum": 1}
        }},
        {"$project": {
            "count": 1,
            "percentage": {"$multiply": [{"$divide": [100, "$_id.total"]}, "$count"], }
        }},
        {"$sort": SON([("percentage", -1)])}], collection))

    data = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
    for i, label in enumerate(list(map(lambda x: x['_id']['gleason'], result))):
        if label in [11, 21, 31, 41, 51]:
            data['1'] += result[i]['percentage']
        elif label in [12, 22, 32, 42, 52]:
            data['2'] += result[i]['percentage']
        elif label in [13, 23, 33, 43, 53]:
            data['3'] += result[i]['percentage']
        elif label in [14, 24, 34, 44, 54]:
            data['4'] += result[i]['percentage']
        elif label in [15, 25, 35, 45, 55]:
            data['5'] += result[i]['percentage']

    return {
        'labels': list(map(lambda x: x, data.keys())),
        'datasets': [{
            'data': list(map(lambda x: x, data.values())),
            'label': "Gleason secondary",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


def distribution_by_gleason_comb(input_json, collection=None):
    """
    prostate cancer breakout by gleason score for this age group - two digit Gleason and single digit Gleason
    :param input_json:
    :param collection:
    :return:
    """
    filters = create_filter(input_json)
    filters['$and'] = [d for d in filters['$and'] if 'gleason' not in d]
    filters['$and'].append({"gleason": {"$nin": [None, 19, 29, 39, 49, 59]}})
    filters['$and'].append({"gleason-comb-recode": {"$nin": [None]}})
    result = json.loads(aggregate([
        {"$match": filters},
        {"$group": {
            "_id": "",
            "total": {"$sum": 1},
            "subset": {"$push": "$gleason-comb-recode"}
        }},
        {"$unwind": "$subset"},
        {"$group": {
            "_id": {"gleason-comb-recode": "$subset", "total": "$total"},
            "count": {"$sum": 1}
        }},
        {"$project": {
            "count": 1,
            "percentage": {"$multiply": [{"$divide": [100, "$_id.total"]}, "$count"], }
        }},
        {"$sort": SON([("percentage", -1)])}], collection))

    return {
        'labels': list(map(lambda x: x['_id']['gleason-comb-recode'], result)),
        'datasets': [{
            'data': list(map(lambda x: x['percentage'], result)),
            'label': "Gleason combined",
            'borderColor': '#48ccf5',
            'fill': False
        }]
    }


if __name__ == '__main__':
    """
    Database groups:
    "sex": {'Male': 1212874}
    "age-1": 0-110
    "race": {'American Indian/Alaska Native': 4069, 'Asian or Pacific Islander': 53415, 'Black': 160951, 'Unknown': 26150, 'White': 968289}
    "race-detail": {'American Indian/Alaska Native': 4069, 'Asian Indian (2010+)': 1907, 'Asian Indian or Pakistani, 
    NOS (1988+)': 1869, 'Black': 160951, 'Chamorran (1991+)': 19, 'Chinese': 10491, 'Fiji Islander (1991+)': 68, 'Filipino': 14437
    "year-of-diagnosis": 1973 - 2014
    "summ-stage": {'Blank(s)': 320533, 'Distant': 41310, 'In situ': 181, 'Localized': 703385, 'Regional': 104445, 'Unknown/unstaged': 43020}
    "of-malignant-tumors": 1-56
    "tumor-size-2004": 0 - 999
    """
    mongo_client = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = mongo_client[DBS_NAME][COLLECTION_NAME]

    # pprint(display_group("gleason-comb-recode"))

    # exit()
    """
    Age, tumor size, Gleason score, ethnicity, PSA, nodes,
    Sorry Gleason primRy score, Gleason secondary score
    Not just one
    We will likely do a three separate charts
    One for Gleason score number 1
    One for Gleason score #2
    And finally a combined Gleason score chart
    So 34 would be 3 in chart 1, 4 in chart 2, and 7 in chart 3
    So on Gleason
    11-55
    Means the values we be separated
    Into songpenintegers
    Single integers
    So 11 becomes 1 and 1
    33 would be 3 and 3
    And then since 11 is 1+1=2
    Last chart would be 2
    55 would be 10
    Etc etc
    """

    diag_request = '{"1age": 62, ' \
                   '"1ethnicity": "Hispanic", ' \
                   '"1gleason-pri": 1, ' \
                   '"1gleason-sec": 1, ' \
                   '"1psa": 1, ' \
                   '"1tumor_size_mm": 1 ' \
                   '}'

    filters = create_filter(diag_request)
    # pprint(filters)
    # count = json.loads(aggregate([
    #     {"$match": filters},
    #     {"$group": {
    #         "_id": "",
    #         "count": {"$sum": 1}}},
    #     {"$sort": SON([("_id", 1)])}]))
    # pprint(count)

    # pprint(display_group("gleason"))
    # pprint(display_group("gleason-comb-recode"))
    # pprint(display_group("chemo"))

    pprint(distribution_by_gleason_comb(diag_request, collection))
