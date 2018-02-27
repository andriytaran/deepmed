import json, os
# import pandas as pd
# from slugify import slugify
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
    elif 10 <= mm < 20:
        return '< 2cm'
    elif 20 <= mm < 30:
        return '< 3cm'
    elif 30 <= mm < 50:
        return '< 5cm'
    elif 50 <= mm < 989:
        return '> 5cm'
    else:
        return None


def recode_t_size(document):
    if isinstance(document['t-size-mm-2004'], int):
        if document['t-size-mm-2004'] not in [888, 990, 991, 992, 993, 994, 995, 996, 997, 998, 999]:
            t_size_mm = document['t-size-mm-2004']
            return t_size_mm, mm_to_cm(t_size_mm)
        elif document['t-size-mm-2004'] in [990, 991, 992, 993, 994, 995]:
            return t_size_2004[document['t-size-mm-2004']]
    tlist = document['t-size-mm-1988'].split()
    try:
        t_size_mm = int(tlist[0])
        return t_size_mm, mm_to_cm(t_size_mm)
    except:
        pass
    if tlist[0] in t_size_1988 and t_size_1988[tlist[0]] == "Micro":
        return "Micro", "< 1cm"
    return None, None


def recode_chemotherapy(document):
    if document['chemotherapy-recode-yes-no-unk'] == 'Yes':
        return 'Yes'
    return 'No'


def recode_radiation(document):
    if document['radiation-1'] != 'None/Unknown':
        return 'Yes'
    if document['radiation-sequence-with-surgery'] != 'No radiation and/or cancer-directed surgery':
        return 'Yes'
    return 'No'


def recode_age(document):
    alist = document['age-recode-with-single-ages-and-85'].split()
    try:
        return int(alist[0])
    except:
        if alist[0] == '85+':
            return 85
    return None


def recode_surgery(document):
    if document['surgery-pre-1997'] != 'Blank(s)':
        if document['surgery-pre-1997'] in (10, 20):
            return "Lumpectomy"
        elif document['surgery-pre-1997'] in (30, 40, 50, 60, 70, 80, 90):
            return "Single Mastectomy"
    if document['surgery'] != 'Blank(s)':
        if document['surgery'] in (
                30, 40, 41, 43, 44, 45, 46, 50, 51, 53, 54, 55, 56, 60, 61, 64, 65, 66, 67, 70, 71, 80):
            return "Single Mastectomy"
        elif document['surgery'] in (42, 47, 48, 49, 52, 57, 58, 59, 62, 63, 68, 69, 72, 73, 74, 75, 76):
            return "Bi-Lateral Mastectomy"
        elif document['surgery'] in (20, 21, 23, 24):
            return "Partial Mastectomy"
        elif document['surgery'] in (19, 90, 99):
            return "Partial Mastectomy"
    return None


def recode_site(document):
    if document['primary-site-labeled'] == 'C50.4-Upper-outer quadrant of breast':
        return "Upper-Outer"
    if document['primary-site-labeled'] == 'C50.2-Upper-inner quadrant of breast':
        return "Lower-Outer"
    if document['primary-site-labeled'] == 'C50.8-Overlapping lesion of breast':
        return "Overlapping"
    if document['primary-site-labeled'] == 'C50.9-Breast, NOS':
        return "NoS"
    if document['primary-site-labeled'] == 'C50.1-Central portion of breast':
        return "Center"
    if document['primary-site-labeled'] == 'C50.3-Lower-inner quadrant of breast':
        return "Lower-Inner"
    if document['primary-site-labeled'] == 'C50.5-Lower-outer quadrant of breast':
        return "Lower-Outer"
    if document['primary-site-labeled'] == 'C50.0-Nipple':
        return "Nipple"
    if document['primary-site-labeled'] == 'C50.6-Axillary tail of breast':
        return "Axillary"
    return None


def recode_type(document):
    if document['type'] in [
        "8530/3: Inflammatory carcinoma",
        "8540/3: Paget disease, mammary",
        "8541/3: Paget disease and infiltrating ductal carcinoma of breast",
        "8543/3: Paget disease and intraductal carcinoma"
    ]:
        return "IBC"
    if document['type'] in [
        "8012/3: Large cell carcinoma, NOS",
        "8015/3: Glassy cell carcinoma",
        "8020/3: Carcinoma, undifferentiated, NOS",
        "8021/3: Carcinoma, anaplastic, NOS",
        "8022/3: Pleomorphic carcinoma",
        "8031/3: Giant cell carcinoma",
        "8032/3: Spindle cell carcinoma, NOS",
        "8033/3: Pseudosarcomatous carcinoma",
        "8041/3: Small cell carcinoma, NOS",
        "8042/3: Oat cell carcinoma",
        "8045/3: Combined small cell carcinoma",
        "8046/3: Non-small cell carcinoma",
        "8050/3: Papillary carcinoma, NOS",
        "8052/3: Papillary squamous cell carcinoma",
        "8070/3: Squamous cell carcinoma, NOS",
        "8071/3: Squamous cell carcinoma, keratinizing, NOS",
        "8072/3: Squamous cell carcinoma, large cell, nonkeratinizing, NOS",
        "8074/3: Squamous cell carcinoma, spindle cell",
        "8076/3: Squamous cell carcinoma, micro-invasive",
        "8082/3: Lymphoepithelial carcinoma",
        "8083/3: Basaloid squamous cell carcinoma",
        "8090/3: Basal cell carcinoma, NOS",
        "8123/3: Basaloid carcinoma",
        "8140/3: Adenocarcinoma, NOS",
        "8141/3: Scirrhous adenocarcinoma",
        "8200/3: Adenoid cystic carcinoma",
        "8201/3: Cribriform carcinoma, NOS",
        "8211/3: Tubular adenocarcinoma",
        "8230/3: Solid carcinoma, NOS",
        "8240/3: Carcinoid tumor, NOS",
        "8243/3: Goblet cell carcinoid",
        "8246/3: Neuroendocrine carcinoma, NOS",
        "8247/3: Merkel cell carcinoma",
        "8260/3: Papillary adenocarcinoma, NOS",
        "8290/3: Oxyphilic adenocarcinoma",
        "8310/3: Clear cell adenocarcinoma, NOS",
        "8314/3: Lipid-rich carcinoma",
        "8315/3: Glycogen-rich carcinoma",
        "8323/3: Mixed cell adenocarcinoma",
        "8341/3: Papillary microcarcinoma",
        "8343/3: Papillary carcinoma, encapsulated",
        "8344/3: Papillary carcinoma, columnar cell",
        "8350/3: Nonencapsulated sclerosing carcinoma",
        "8401/3: Apocrine adenocarcinoma",
        "8407/3: Sclerosing sweat duct carcinoma",
        "8413/3: Eccrine adenocarcinoma",
        "8430/3: Mucoepidermoid carcinoma",
        "8440/3: Cystadenocarcinoma, NOS",
        "8450/3: Papillary cystadenocarcinoma, NOS",
        "8452/3: Solid pseudopapillary carcinoma",
        "8453/3: Intraductal papillary-mucinous carcinoma, invasive",
        "8460/3: Papillary serous cystadenocarcinoma",
        "8470/3: Mucinous cystadenocarcinoma, NOS",
        "8471/3: Papillary mucinous cystadenocarcinoma",
        "8480/3: Mucinous adenocarcinoma",
        "8481/3: Mucin-producing adenocarcinoma",
        "8490/3: Signet ring cell carcinoma",
        "8500/2: Intraductal carcinoma, noninfiltrating, NOS",
        "8500/3: Infiltrating duct carcinoma, NOS",
        "8501/2: Comedocarcinoma, noninfiltrating",
        "8501/3: Comedocarcinoma, NOS",
        "8502/3: Secretory carcinoma of breast",
        "8503/2: Noninfiltrating intraductal papillary adenocarcinoma",
        "8503/3: Intraductal papillary adenocarcinoma with invasion",
        "8504/2: Noninfiltrating intracystic carcinoma",
        "8504/3: Intracystic carcinoma, NOS",
        "8507/2: Intraductal micropapillary carcinoma",
        "8507/3: Ductal carcinoma, micropapillary",
        "8510/3: Medullary carcinoma, NOS",
        "8512/3: Medullary carcinoma with lymphoid stroma",
        "8513/3: Atypical medullary carcinoma",
        "8514/3: Duct carcinoma, desmoplastic type",
        "8550/3: Acinar cell carcinoma",
        "8560/3: Adenosquamous carcinoma",
        "8562/3: Epithelial-myoepithelial carcinoma",
        "8575/3: Metaplastic carcinoma, NOS"
    ]:
        return "IDC"
    if document['type'] in [
        "8520/3: Lobular carcinoma, NOS",
        "8521/3: Infiltrating ductular carcinoma"
    ]:
        return "ILC"
    if document['type'] in [
        "8010/2: Carcinoma in situ, NOS",
        "8022/2: Pleomorphic carcinoma in situ",
        "8050/2: Papillary carcinoma in situ",
        "8070/2: Squamous cell carcinoma in situ, NOS",
        "8140/2: Adenocarcinoma in situ, NOS",
        "8200/2: Adenoid cystic carcinoma in situ",
        "8201/2: Cribriform carcinoma in situ",
        "8211/2: Tubular adenocarcinoma in situ",
        "8230/2: Ductal carcinoma in situ, solid type",
        "8255/2: Adenocarcinoma with mixed subtypes, in situ",
        "8260/2: Papillary adenocarcinoma in situ, NOS",
        "8310/2: Clear cell adenocarcinoma in situ",
        "8323/2: Mixed cell adenocarcinoma in situ",
        "8343/2: Papillary carcinoma, encapsulated, in situ",
        "8401/2: Apocrine adenocarcinoma in situ",
        "8453/2: Intraductal papillary-mucinous carcinoma, in situ",
        "8480/2: Mucinous adenocarcinoma in situ",
        "8502/2: Secretory carcinoma of breast, in situ",
        "8508/2: Cystic hypersecretory carcinoma, in situ",
        "8520/2: Lobular carcinoma in situ",
        "8521/2: Ductular carcinoma in situ",
        "8522/2: Intraductal and lobular in situ carcinoma",
        "8523/2: Intraductal with other types of carcinoma in situ",
        "8540/2: Paget disease, mammary, in situ",
        "8550/2: Acinar cell carcinoma in situ",
        "8560/2: Mixed squamous cell and glandular papilloma, in situ",
        "8743/2: Superficial spreading melanoma in situ",
        "8983/2: Adenomyoepithelioma, in situ"
    ]:
        return "In-Situ"
    if document['type'] in [
        "8523/3: Infiltrating duct mixed with other types of carcinoma",
        "8524/3: Infiltrating lobular mixed with other types of carcinoma",
        "8543/2: Paget disease in situ and intraductal carcinoma",
        "8570/3: Adenocarcinoma with squamous metaplasia",
        "8571/3: Adenocarcinoma with cartilaginous and osseous metaplasia",
        "8572/3: Adenocarcinoma with spindle cell metaplasia",
        "8573/3: Adenocarcinoma with apocrine metaplasia",
        "8574/2: Adenocarcinoma in situ with neuroendocrine differentiation",
        "8574/3: Adenocarcinoma with neuroendocrine differentiation"
    ]:
        return "Mixed"
    return "Other"


def recode_grade(document):
    if document['grade'] == 'Moderately differentiated; Grade II':
        return 2
    if document['grade'] == 'Poorly differentiated; Grade III':
        return 3
    if document['grade'] == 'Well differentiated; Grade I':
        return 1
    if document['grade'] == 'Unknown':
        return None
    if document['grade'] == 'Undifferentiated; anaplastic; Grade IV':
        return 4
    return None


def recode_laterality(document):
    if document['laterality'] == 'Right - origin of primary':
        return "Right"
    if document['laterality'] == 'Left - origin of primary':
        return "Left"
    if document['laterality'] == 'Paired site, but no information concerning laterality':
        return None
    if document['laterality'] == 'Bilateral, single primary':
        return "Bilateral"
    return None


def recode_er_status(document):
    if document['er-status-recode-breast-cancer-1990'] in ['Positive', 'Borderline']:
        return "+"
    if document['er-status-recode-breast-cancer-1990'] == 'Negative':
        return "-"
    return None


def recode_pr_status(document):
    if document['pr-status-recode-breast-cancer-1990'] in ['Positive', 'Borderline']:
        return "+"
    if document['pr-status-recode-breast-cancer-1990'] == 'Negative':
        return "-"
    return None


def recode_her2_status(document):
    if document['derived-her2-recode-2010'] in ['Positive', 'Borderline']:
        return "+"
    if document['derived-her2-recode-2010'] == 'Negative':
        return "-"
    return None


def recode_nodes(document):
    pass


if __name__ == '__main__':
    display_group('surgery-pre-1997')
    # display_group('surgery')
    exit()

    # i = 0
    collection.updateMany({}, {"$rename": {"radiation": "radiation-1"}})
    for document in collection.find():
        print(document['_id'])
        document['t-size-mm'] = recode_t_size(document)[0]
        document['t-size-cm'] = recode_t_size(document)[1]
        collection.update_one({'_id': document['_id']}, {"$set": document}, upsert=False)
    # print(i)
