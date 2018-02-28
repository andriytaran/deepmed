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
        age = int(alist[0])
        if age < 5:
            return "00-04 years"
        if age < 10:
            return "05-09 years"
        if age < 15:
            return "10-14 years"
        if age < 20:
            return "15-19 years"
        if age < 25:
            return "20-24 years"
        if age < 30:
            return "25-29 years"
        if age < 35:
            return "30-34 years"
        if age < 40:
            return "35-39 years"
        if age < 45:
            return "40-44 years"
        if age < 50:
            return "45-49 years"
        if age < 55:
            return "50-54 years"
        if age < 60:
            return "55-59 years"
        if age < 65:
            return "60-64 years"
        if age < 70:
            return "65-69 years"
        if age < 75:
            return "70-74 years"
        if age < 80:
            return "75-79 years"
        if age < 85:
            return "80-84 years"
        return int(alist[0])
    except:
        if alist[0] == '85+':
            return '85+ years'
    return None


def recode_surgery(document):
    if document['surgery-pre-1997'] != 'Blank(s)':
        if document['surgery-pre-1997'] in (10, 18, 20, 28):
            return "Lumpectomy"
        elif document['surgery-pre-1997'] in (30, 38, 40, 48, 50, 58, 60, 68, 70, 78, 80, 88, 90, 98):
            return "Single Mastectomy"
    if document['surgery-1'] != 'Blank(s)':
        if document['surgery-1'] in (
                30, 40, 41, 43, 44, 45, 46, 50, 51, 53, 54, 55, 56, 60, 61, 64, 65, 66, 67, 70, 71, 80):
            return "Single Mastectomy"
        elif document['surgery-1'] in (42, 47, 48, 49, 52, 57, 58, 59, 62, 63, 68, 69, 72, 73, 74, 75, 76):
            return "Bi-Lateral Mastectomy"
        elif document['surgery-1'] in (20, 21, 22, 23, 24):
            return "Lumpectomy"
        elif document['surgery-1'] in (19, 90, 99):
            return "Other"
    return None


def recode_site(document):
    # new document['primary-site-labeled']
    if document['primary-site-labeled-1'] == 'C50.4-Upper-outer quadrant of breast':
        return "Upper-Outer"
    if document['primary-site-labeled-1'] == 'C50.2-Upper-inner quadrant of breast':
        return "Lower-Outer"
    if document['primary-site-labeled-1'] == 'C50.8-Overlapping lesion of breast':
        return "Overlapping"
    if document['primary-site-labeled-1'] == 'C50.9-Breast, NOS':
        return "NoS"
    if document['primary-site-labeled-1'] == 'C50.1-Central portion of breast':
        return "Center"
    if document['primary-site-labeled-1'] == 'C50.3-Lower-inner quadrant of breast':
        return "Lower-Inner"
    if document['primary-site-labeled-1'] == 'C50.5-Lower-outer quadrant of breast':
        return "Lower-Outer"
    if document['primary-site-labeled-1'] == 'C50.0-Nipple':
        return "Nipple"
    if document['primary-site-labeled-1'] == 'C50.6-Axillary tail of breast':
        return "Axillary"
    return None


def recode_type(document):
    # new document['type']
    if document['type-1'] in [
        "8530/3: Inflammatory carcinoma",
        "8540/3: Paget disease, mammary",
        "8541/3: Paget disease and infiltrating ductal carcinoma of breast",
        "8543/3: Paget disease and intraductal carcinoma",
        "8542/3: Paget disease, extramammary (except Paget disease of bone)"
    ]:
        return "IBC"
    if document['type-1'] in [
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
        "8575/3: Metaplastic carcinoma, NOS",
        "8345/3: Medullary carcinoma with amyloid stroma"
    ]:
        return "IDC"
    if document['type-1'] in [
        "8520/3: Lobular carcinoma, NOS",
        "8521/3: Infiltrating ductular carcinoma"
    ]:
        return "ILC"
    if document['type-1'] in [
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
        "8983/2: Adenomyoepithelioma, in situ",
        "8052/2: Papillary squamous cell carcinoma, non-invasive",
        "8071/2: Squamous cell carcinoma in situ, keratinizing, NOS",
        "8210/2: Adenocarcinoma in situ in adenomatous polyp",
        "8240/2: Carcinoid tumor, in situ",
        "8246/2: Neuroendocrine carcinoma in situ",
        "8481/2: Mucin-producing adenocarcinoma in situ",
        "8490/2: Signet ring cell carcinoma in situ",
        "8510/2: Medullary carcinoma in situ, NOS",
        "8524/2: Infiltrating lobular mixed with other types of carcinoma, in situ",
        "8541/2: Paget disease in situ and intraductal carcinoma",
        "8542/2: Paget disease (in situ), extramammary (except Paget disease of bone)",
        "8571/2: Adenocarcinoma with cartilaginous and osseous metaplasia, in situ",
        "8573/2: Adenocarcinoma in situ with apocrine metaplasia",
        "8720/2: Melanoma in situ"
    ]:
        return "In-Situ"
    if document['type-1'] in [
        "8523/3: Infiltrating duct mixed with other types of carcinoma",
        "8524/3: Infiltrating lobular mixed with other types of carcinoma",
        "8543/2: Paget disease in situ and intraductal carcinoma",
        "8570/3: Adenocarcinoma with squamous metaplasia",
        "8571/3: Adenocarcinoma with cartilaginous and osseous metaplasia",
        "8572/3: Adenocarcinoma with spindle cell metaplasia",
        "8573/3: Adenocarcinoma with apocrine metaplasia",
        "8574/2: Adenocarcinoma in situ with neuroendocrine differentiation",
        "8574/3: Adenocarcinoma with neuroendocrine differentiation",
        "8522/3: Infiltrating duct and lobular carcinoma"
    ]:
        return "Mixed"
    if document['type-1'] in [
        "8000/3: Neoplasm, malignant",
        "8001/3: Tumor cells, malignant",
        "8002/3: Malignant tumor, small cell type",
        "8003/3: Malignant tumor, giant cell type",
        "8004/3: Malignant tumor, spindle cell type",
        "8005/3: Malignant tumor, clear cell type",
        "8010/3: Carcinoma, NOS",
        "8011/3: Epithelioma, malignant",
        "8012/2: Large cell carcinoma in situ",
        "8013/3: Large cell neuroendocrine carcinoma",
        "8030/3: Giant cell and spindle cell carcinoma",
        "8035/3: Carcinoma with osteoclast-like giant cells",
        "8051/2: Verrucous carcinoma in situ",
        "8051/3: Verrucous carcinoma, NOS",
        "8075/3: Squamous cell carcinoma, adenoid",
        "8081/2: Bowen disease",
        "8110/3: Pilomatrix carcinoma",
        "8130/3: Papillary transitional cell carcinoma",
        "8142/3: Linitis plastica",
        "8143/3: Superficial spreading adenocarcinoma",
        "8145/3: Carcinoma, diffuse type",
        "8147/3: Basal cell adenocarcinoma",
        "8154/3: Mixed pancreatic endocrine and exocrine tumor, malignant",
        "8190/3: Trabecular adenocarcinoma",
        "8210/3: Adenocarcinoma in adenomatous polyp",
        "8231/3: Carcinoma simplex",
        "8241/3: Enterochromaffin cell carcinoid",
        "8249/3: Atypical carcinoid tumor",
        "8250/3: Bronchiolo-alveolar adenocarcinoma, NOS",
        "8251/3: Alveolar adenocarcinoma",
        "8255/3: Adenocarcinoma with mixed subtypes",
        "8320/3: Granular cell carcinoma",
        "8382/3: Endometrioid adenocarcinoma, secretory variant",
        "8400/3: Sweat gland adenocarcinoma",
        "8403/3: Malignant eccrine spiradenoma",
        "8508/3: Cystic hypersecretory carcinoma",
        "8525/3: Polymorphous low grade adenocarcinoma",
        "8720/3: Malignant melanoma, NOS",
        "8743/3: Superficial spreading melanoma",
        "8800/3: Sarcoma, NOS",
        "8801/3: Spindle cell sarcoma",
        "8802/3: Giant cell sarcoma",
        "8803/3: Small cell sarcoma",
        "8804/3: Epithelioid sarcoma",
        "8805/3: Undifferentiated sarcoma",
        "8810/3: Fibrosarcoma, NOS",
        "8811/3: Fibromyxosarcoma",
        "8814/3: Infantile fibrosarcoma",
        "8815/3: Solitary fibrous tumor, malignant",
        "8830/3: Malignant fibrous histiocytoma",
        "8832/3: Dermatofibrosarcoma, NOS",
        "8836/3: Malignant angiomatoid fibrous histiocytoma",
        "8840/3: Myxosarcoma",
        "8850/3: Liposarcoma, NOS",
        "8851/3: Liposarcoma, well differentiated",
        "8852/3: Myxoid liposarcoma",
        "8854/3: Pleomorphic liposarcoma",
        "8855/3: Mixed liposarcoma",
        "8858/3: Dedifferentiated liposarcoma",
        "8890/3: Leiomyosarcoma, NOS",
        "8900/3: Rhabdomyosarcoma, NOS",
        "8912/3: Spindle cell rhabdomyosarcoma",
        "8935/3: Stromal sarcoma, NOS",
        "8940/3: Mixed tumor, malignant, NOS",
        "8950/3: Mullerian mixed tumor",
        "8980/3: Carcinosarcoma, NOS",
        "8982/3: Malignant myoepithelioma",
        "8983/3: Adenomyoepithelioma, malignant",
        "9020/3: Phyllodes tumor, malignant",
        "9040/3: Synovial sarcoma, NOS",
        "9041/3: Synovial sarcoma, spindle cell",
        "9120/3: Hemangiosarcoma",
        "9180/3: Osteosarcoma, NOS",
        "9181/3: Chondroblastic osteosarcoma",
        "9186/3: Central osteosarcoma",
        "9260/3: Ewing sarcoma",
        "9473/3: Primitive neuroectodermal tumor",
        "9540/3: Malignant peripheral nerve sheath tumor",
        "9580/3: Granular cell tumor, malignant",
        "8891/3: Epithelioid leiomyosarcoma",
        "8894/3: Angiomyosarcoma",
        "8895/3: Myosarcoma",
        "8896/3: Myxoid leiomyosarcoma",
        "8901/3: Pleomorphic rhabdomyosarcoma, adult type",
        "8910/3: Embryonal rhabdomyosarcoma, NOS",
        "8920/3: Alveolar rhabdomyosarcoma",
        "8930/3: Endometrial stromal sarcoma, NOS",
        "8933/3: Adenosarcoma",
        "8963/3: Malignant rhabdoid tumor",
        "8990/3: Mesenchymoma, malignant",
        "9044/3: Clear cell sarcoma, NOS (except of kidney M-8964/3)",
        "9071/3: Yolk sac tumor",
        "9100/3: Choriocarcinoma, NOS",
        "9130/3: Hemangioendothelioma, malignant",
        "9133/3: Epithelioid hemangioendothelioma, malignant",
        "9150/3: Hemangiopericytoma, malignant",
        "9170/3: Lymphangiosarcoma",
        "9183/3: Telangiectatic osteosarcoma",
        "9220/3: Chondrosarcoma, NOS",
        "9231/3: Myxoid chondrosarcoma",
        "9364/3: Peripheral neuroectodermal tumor",
        "9400/3: Astrocytoma, NOS",
        "9500/3: Neuroblastoma, NOS",
        "9581/3: Alveolar soft part sarcoma"
    ]:
        return "Other"
    return None


def recode_grade(document):
    # new document['grade']
    if document['grade-1'] == 'Moderately differentiated; Grade II':
        return 2
    if document['grade-1'] == 'Poorly differentiated; Grade III':
        return 3
    if document['grade-1'] == 'Well differentiated; Grade I':
        return 1
    if document['grade-1'] == 'Unknown':
        return None
    if document['grade-1'] == 'Undifferentiated; anaplastic; Grade IV':
        return 4
    return None


def recode_laterality(document):
    # new document['laterality']
    if document['laterality-1'] == 'Right - origin of primary':
        return "Right"
    if document['laterality-1'] == 'Left - origin of primary':
        return "Left"
    if document['laterality-1'] == 'Paired site, but no information concerning laterality':
        return None
    if document['laterality-1'] == 'Bilateral, single primary':
        return "Bilateral"
    return None


def recode_er_status(document):
    # new document['er-status-recode-breast-cancer-1990']
    if document['er-status-recode-breast-cancer-1990-1'] in ['Positive', 'Borderline']:
        return "+"
    if document['er-status-recode-breast-cancer-1990-1'] == 'Negative':
        return "-"
    return None


def recode_pr_status(document):
    # new document['pr-status-recode-breast-cancer-1990']
    if document['pr-status-recode-breast-cancer-1990-1'] in ['Positive', 'Borderline']:
        return "+"
    if document['pr-status-recode-breast-cancer-1990-1'] == 'Negative':
        return "-"
    return None


def recode_her2_status(document):
    # new document['derived-her2-recode-2010']
    if document['derived-her2-recode-2010-1'] in ['Positive', 'Borderline']:
        return "+"
    if document['derived-her2-recode-2010-1'] == 'Negative':
        return "-"
    return None


def recode_icc_site_icd(document):
    # new document['iccc-site-recode-icd-o-3-who-2008']
    if document['iccc-site-recode-icd-o-3-who-2008-1'] == 'Not classified by ICCC or in situ':
        return "Non-Malignant"
    return "Malignant"


def recode_aya_site(document):
    # new document['aya-site-recode-who-2008']
    if document['aya-site-recode-who-2008-1'] == 'Unclassified and Non-Malignant':
        return "Non-Malignant"
    return "Malignant"


def recode_survmnts(document):
    # new document['survival-months']
    try:
        return int(document['survival-months-1'].lstrip('0'))
    except:
        return None


def recode_nodes(document):
    if document['regional-nodes-positive-1988-1'] != 'Blank(s)':
        if document['regional-nodes-positive-1988-1'] < 90:
            return document['regional-nodes-positive-1988-1']
        elif document['regional-nodes-positive-1988-1'] == 90:
            return ">9"
        elif document['regional-nodes-positive-1988-1'] in (95, 97):
            return ">1"
    return None


if __name__ == '__main__':
    pprint(display_group('regional-nodes-positive-1988-1'))
    exit()
    for k, v in display_group('surgery-1').items():
        document = {'surgery-pre-1997': k, 'surgery-1': k}
        new_type = recode_surgery(document)
        if new_type is None:
            print(k)
        # print(k)

    # display_group('surgery')
    exit()

    # i = 0
    i = 0
    for document in collection.find():
        # print(document['_id'])
        document['regional-nodes-positive-1988'] = recode_nodes(document)
        document['chemo'] = recode_chemotherapy(document)
        # print(document['chemotherapy-recode-yes-no-unk'], recode_chemotherapy(document))
        document['radiation'] = recode_radiation(document)
        # print(document['radiation-1'], document['radiation-sequence-with-surgery'],
        #       recode_radiation(document))
        document['age-recode-with-1-year-olds'] = recode_age(document)
        # print(document['age-recode-with-single-ages-and-85'], recode_age(document))
        document['surgery'] = recode_surgery(document)
        # print(document['surgery-pre-1997'], document['surgery-1'], recode_surgery(document))
        document['primary-site-labeled'] = recode_site(document)
        # print(document['primary-site-labeled-1'], recode_site(document))
        document['type'] = recode_type(document)
        # print(document['type-1'], recode_type(document))
        document['grade'] = recode_grade(document)
        # print(document['grade-1'], recode_grade(document))
        document['laterality'] = recode_laterality(document)
        # print(document['laterality-1'], recode_laterality(document))
        document['er-status-recode-breast-cancer-1990'] = recode_er_status(document)
        # print(document['er-status-recode-breast-cancer-1990-1'], recode_er_status(document))
        document['pr-status-recode-breast-cancer-1990'] = recode_pr_status(document)
        # print(document['pr-status-recode-breast-cancer-1990-1'], recode_pr_status(document))
        document['derived-her2-recode-2010'] = recode_her2_status(document)
        # print(document['derived-her2-recode-2010-1'], recode_her2_status(document))
        document['iccc-site-recode-icd-o-3-who-2008'] = recode_icc_site_icd(document)
        # print(document['iccc-site-recode-icd-o-3-who-2008-1'], recode_icc_site_icd(document))
        document['aya-site-recode-who-2008'] = recode_aya_site(document)
        # print(document['aya-site-recode-who-2008-1'], recode_aya_site(document))
        document['survival-months'] = recode_survmnts(document)
        # print(document['survival-months-1'], recode_survmnts(document))
        document['t-size-mm'] = recode_t_size(document)[0]
        document['t-size-cm'] = recode_t_size(document)[1]
        i += 1
        # collection.update_one({'_id': document['_id']}, {"$set": document}, upsert=False)
        print(i, '/ 1546698 ')
    print('ALL DONE.')

    for document in collection.find():
        print(document['_id'])
        document['t-size-mm'] = recode_t_size(document)[0]
        document['t-size-cm'] = recode_t_size(document)[1]
        collection.update_one({'_id': document['_id']}, {"$set": document}, upsert=False)
