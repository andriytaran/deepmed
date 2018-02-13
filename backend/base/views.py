import json

from django.conf import settings
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from base.serializers import DiagnosisSerializer
from lib.dataset import breast_cancer_by_grade, diagnosis, \
    percent_race_with_cancer_by_age, \
    breakout_by_stage, breast_cancer_by_size, \
    percent_of_women_with_cancer_by_race_overall, \
    distribution_of_stage_of_cancer, surgery_decisions, chemotherapy, \
    radiation, breast_cancer_by_state, \
    breast_cancer_at_a_glance, breast_cancer_by_age, \
    percent_women_annualy_diagnosed, percent_women_by_type, \
    breast_cancer_by_state2, breast_cancer_at_a_glance2


def v_get_t_size_cm(size_mm):
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


class ReportDataView(GenericAPIView):
    serializer_class = DiagnosisSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)

        serializer.is_valid(raise_exception=True)
        dd = dict(serializer.validated_data)

        age = json.dumps({'age': dd.get('age')})

        ethnicity = dd.get('ethnicity')

        if ethnicity == 'Caucasian':
            v_ethnicity = 'White'
        elif ethnicity == 'African American':
            v_ethnicity = 'Black'
        elif ethnicity == 'Asian':
            v_ethnicity = 'Asian or Pacific Islander'
        elif ethnicity == 'Other':
            v_ethnicity = 'Unknown'
        else:
            v_ethnicity = ethnicity

        is_radiation_therapy = 'No'  # Radiation Therapy

        # Recommended Treatment Plans

        ## Overall Plans

        overall_plans = []
        hormonal_therapy = []
        radiation_therapy = []
        chemo_therapy = []

        try:
            import subprocess
            import ast
            import re
            regex = r"\((.*?)\)"

            # START SURGERY
            surgery_args = ','.join([dd.get('sex'),
                                     str(dd.get('age')),
                                     v_ethnicity,
                                     str(float(dd.get('tumor_grade', 'unk'))),
                                     dd.get('site'),
                                     dd.get('type'),
                                     dd.get('stage'),
                                     dd.get('region'),
                                     v_get_t_size_cm(
                                         dd.get('tumor_size_in_mm')),
                                     str(dd.get('number_of_tumors')),
                                     str(dd.get('num_pos_nodes'))])

            surgery_command_str = [settings.ML_PYTHON_PATH,
                                   settings.ML_COMMAND_FILE,
                                   surgery_args, 'Surgery']

            surgery_command = subprocess.Popen(surgery_command_str,
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE,
                                               cwd=settings.ML_COMMAND_DIR)
            surgery_output, err = surgery_command.communicate()

            # To-Do remove try-except
            try:
                surgery_response = ast.literal_eval(
                    re.search(regex,
                              str(surgery_output.decode('utf8'))).group())
            except:
                surgery_response = ()

            # END SURGERY

            # START CHEMO

            chemo_args = ','.join([
                str(dd.get('age')),
                v_ethnicity,
                str(float(dd.get('tumor_grade'))),
                dd.get('type'),
                dd.get('stage'),
                dd.get('region'),
                v_get_t_size_cm(dd.get('tumor_size_in_mm')),
                str(dd.get('number_of_tumors')),
                str(dd.get('num_pos_nodes')),
                str(dd.get('er_status')),
                str(dd.get('pr_status')),
                str(dd.get('her2_status'))])

            chemo_command_str = [settings.ML_PYTHON_PATH,
                                 settings.ML_COMMAND_FILE,
                                 chemo_args, 'Chemo']

            chemo_command = subprocess.Popen(chemo_command_str,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE,
                                             cwd=settings.ML_COMMAND_DIR)
            chemo_output, err = chemo_command.communicate()

            chemo_response = ast.literal_eval(
                re.search(regex, str(chemo_output.decode('utf8'))).group())

            # END CHEMO

            # START RADIATION

            import copy

            radiation_args = [
                str(dd.get('age')),
                v_ethnicity,
                str(float(dd.get('tumor_grade'))),
                dd.get('site'),
                dd.get('type'),
                dd.get('stage'),
                dd.get('region'),
                v_get_t_size_cm(dd.get('tumor_size_in_mm')),
                str(dd.get('number_of_tumors')),
                str(dd.get('num_pos_nodes')),
                str(dd.get('er_status')),
                str(dd.get('pr_status')),
                str(dd.get('her2_status'))]

            sm_radiation_args = copy.deepcopy(
                radiation_args)  # Copy base list of args

            sm_radiation_args.append('Mastectomy')
            sm_radiation_args.append(chemo_response[0])

            sm_radiation_command_str = [settings.ML_PYTHON_PATH,
                                        settings.ML_COMMAND_FILE,
                                        ','.join(sm_radiation_args),
                                        'Radiation']

            sm_radiation_command = subprocess.Popen(sm_radiation_command_str,
                                                    stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE,
                                                    cwd=settings.ML_COMMAND_DIR)

            sm_radiation_output, err = sm_radiation_command.communicate()

            sm_radiation_response = ast.literal_eval(
                re.search(regex,
                          str(sm_radiation_output.decode('utf8'))).group())

            sl_radiation_args = copy.deepcopy(
                radiation_args)  # Copy base list of args

            sl_radiation_args.append('Lumpectomy')
            sl_radiation_args.append(chemo_response[0])

            sl_radiation_command_str = [settings.ML_PYTHON_PATH,
                                        settings.ML_COMMAND_FILE,
                                        ','.join(sm_radiation_args),
                                        'Radiation']

            sl_radiation_command = subprocess.Popen(sl_radiation_command_str,
                                                    stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE,
                                                    cwd=settings.ML_COMMAND_DIR)
            sl_radiation_output, err = sl_radiation_command.communicate()

            sl_radiation_response = ast.literal_eval(
                re.search(regex,
                          str(sl_radiation_output.decode('utf8'))).group())

            # END RADIATION

            overall_plans = []

            surgery_level = round(surgery_response[1] * 100)
            chemo_level = round(chemo_response[1] * 100)
            sm_radiation_level = round(sm_radiation_response[1] * 100)
            sl_radiation_level = round(sl_radiation_response[1] * 100)

            if surgery_response[0] == 'Mastectomy':
                is_radiation_therapy = sm_radiation_response[0]
                overall_plans.append({
                    'name': 'Preferred Outcome A',
                    'type': surgery_response[0],
                    'radiation': 'Y' if sm_radiation_response[
                                            0] == 'Yes' else 'N',
                    'radiation_confidence_level': sm_radiation_level,
                    'chemo': 'Y' if chemo_response[0] == 'Yes' else 'N',
                    'chemo_confidence_level': chemo_level,
                    'surgery': 'Y',
                    'surgery_confidence_level': surgery_level,
                    'level': surgery_level})
                overall_plans.append({
                    'name': 'Preferred Outcome B',
                    'type': 'Lumpectomy',
                    'radiation': 'Y' if sl_radiation_response[
                                            0] == 'Yes' else 'N',
                    'radiation_confidence_level': sl_radiation_level,
                    'chemo': 'Y' if chemo_response[0] == 'Yes' else 'N',
                    'chemo_confidence_level': chemo_level,
                    'surgery': 'Y',
                    'surgery_confidence_level': 100 - surgery_level,
                    'level': 100 - surgery_level})
            else:
                is_radiation_therapy = sl_radiation_response[0]
                overall_plans.append({
                    'name': 'Preferred Outcome A',
                    'type': surgery_response[0],
                    'radiation': 'Y' if sl_radiation_response[
                                            0] == 'Yes' else 'N',
                    'radiation_confidence_level': sl_radiation_level,
                    'chemo': 'Y' if chemo_response[0] == 'Yes' else 'N',
                    'chemo_confidence_level': chemo_level,
                    'surgery_confidence_level': surgery_level,
                    'surgery': 'Y',
                    'level': surgery_level})
                overall_plans.append({
                    'name': 'Preferred Outcome B',
                    'type': 'Mastectomy',
                    'radiation': 'Y' if sm_radiation_response[
                                            0] == 'Yes' else 'N',
                    'radiation_confidence_level': sm_radiation_level,
                    'chemo': 'Y' if chemo_response[0] == 'Yes' else 'N',
                    'chemo_confidence_level': chemo_level,
                    'surgery_confidence_level': 100 - surgery_level,
                    'surgery': 'Y',
                    'level': 100 - surgery_level})

            # Hormonal Therapy

            if dd.get('her2_status') == '+' or dd.get('er_status') == '+':
                hormonal_therapy.append({'name': 'Tamoxifen',
                                         'number_of_treatments': 120,
                                         'administration': 'Monthly'})

            # Radiation Therapy

            if is_radiation_therapy == 'Yes':
                radiation_therapy.append({'name': 'Beam Radiation',
                                          'number_of_treatments': 30,
                                          'administration': 'Daily'})

            # Chemo Therapy

            if chemo_response[0] == 'Yes' and \
                    int(dd.get('tumor_size_in_mm')) > 20 and \
                    dd.get('her2_status') != '+':
                chemo_therapy.append({
                    'plan': 'AC+T',
                    'number_of_treatments': [
                        {'name': 'A)', 'value': '4AC, 4T'},
                        {'name': 'B)', 'value': '4AC, 12T'}],
                    'administration': [
                        {'name': 'A)', 'values': [
                            {'name': 'AC', 'time': 'Every 2 weeks'},
                            {'name': 'T', 'time': 'Every 2 weeks'}
                        ]},
                        {'name': 'B)', 'values': [
                            {'name': 'AC', 'time': 'Every 2 weeks'},
                            {'name': 'T', 'time': 'Every week'}
                        ]}
                    ]
                })
            elif chemo_response[0] == 'Yes' and \
                    int(dd.get('tumor_size_in_mm')) < 20 and \
                    dd.get('her2_status') != '+':
                chemo_therapy.append({
                    'plan': 'C+T',
                    'number_of_treatments': [
                        {'name': 'A)', 'value': '4C, 4T'},
                        {'name': 'B)', 'value': '4C, 12T'}],
                    'administration': [
                        {'name': 'A)', 'values': [
                            {'name': 'C', 'time': 'Every 2 weeks'},
                            {'name': 'T', 'time': 'Every 2 weeks'}
                        ]},
                        {'name': 'B)', 'values': [
                            {'name': 'C', 'time': 'Every 2 weeks'},
                            {'name': 'T', 'time': 'Every week'}
                        ]}
                    ]
                })
            elif chemo_response[0] == 'Yes' and \
                    int(dd.get('tumor_size_in_mm')) > 20 and \
                    dd.get('her2_status') == '+':
                chemo_therapy.append({
                    'plan': 'AC+T+HCP',
                    'number_of_treatments': [
                        {'name': 'A)', 'value': '4AC, 4T, 52HCP'},
                        {'name': 'B)', 'value': '4AC, 12T, 52HCP'}],
                    'administration': [
                        {'name': 'A)', 'values': [
                            {'name': 'AC', 'time': 'Every 2 weeks'},
                            {'name': 'T', 'time': 'Every 2 weeks'},
                            {'name': 'HCP', 'time': 'Every week'}
                        ]},
                        {'name': 'B)', 'values': [
                            {'name': 'AC', 'time': 'Every 2 weeks'},
                            {'name': 'T', 'time': 'Every week'},
                            {'name': 'HCP', 'time': 'Every week'}
                        ]}
                    ]
                })
            elif chemo_response[0] == 'Yes' and \
                    int(dd.get('tumor_size_in_mm')) < 20 and \
                    dd.get('her2_status') == '+':
                chemo_therapy.append({
                    'plan': 'A+T+HCP',
                    'number_of_treatments': [
                        {'name': 'A)', 'value': '4C, 4T, 52HCP'},
                        {'name': 'B)', 'value': '4C, 12T, 52HCP'}],
                    'administration': [
                        {'name': 'A)', 'values': [
                            {'name': 'A', 'time': 'Every 2 weeks'},
                            {'name': 'T', 'time': 'Every 2 weeks'},
                            {'name': 'HCP', 'time': 'Every week'}
                        ]},
                        {'name': 'B)', 'values': [
                            {'name': 'A', 'time': 'Every 2 weeks'},
                            {'name': 'T', 'time': 'Every week'},
                            {'name': 'HCP', 'time': 'Every week'}
                        ]}
                    ]
                })

        except Exception as e:
            overall_plans = []
            hormonal_therapy = []
            radiation_therapy = []
            chemo_therapy = []

        data = {
            'recommended_treatment_plans': {
                'overall_plans': overall_plans,
                'hormonal_therapy': hormonal_therapy,
                'radiation_therapy': radiation_therapy,
                'chemo_therapy': chemo_therapy
            },
            'percent_women_by_type': percent_women_by_type(),
            'breast_cancer_by_grade_and_size': {
                'grade': breast_cancer_by_grade(age),
                'size': breast_cancer_by_size(age)
            },
            'distribution_of_stage_of_cancer': {
                'overall': distribution_of_stage_of_cancer(age),
                'by_race':
                    distribution_of_stage_of_cancer(
                        json.dumps({'age': dd.get('age'),
                                    'ethnicity': v_ethnicity},
                                   ensure_ascii=False)),
            },
            'percent_of_women_with_cancer_by_race': {
                'overall': percent_of_women_with_cancer_by_race_overall()
            },
            'surgery_decisions': surgery_decisions(age),
            'chemotherapy': {
                'overall': chemotherapy(age),
            },
            'radiation': {
                'overall': radiation(age),
            },
            'breast_cancer_by_state': breast_cancer_by_state2(1),
            'breast_cancer_at_a_glance': breast_cancer_at_a_glance2(),
            'breast_cancer_by_age': breast_cancer_by_age(),
        }

        data['chemotherapy']['breakout_by_stage'] = breakout_by_stage(
            json.dumps({
                'age': dd.get('age'),
                'chemo': 'Yes',
                "breast-adjusted-ajcc-6th-stage-1988": {
                    "$in": ["I", "IIA", "IIB", "IIIA",
                            "IIIB", "IIIC", "IIINOS", "IV",
                            0]
                }}, ensure_ascii=False))

        data['radiation']['breakout_by_stage'] = breakout_by_stage(json.dumps({
            'age': dd.get('age'),
            'radiation': 'Yes',
            "breast-adjusted-ajcc-6th-stage-1988": {
                "$in": ["I", "IIA", "IIB", "IIIA",
                        "IIIB", "IIIC", "IIINOS", "IV",
                        0]
            }}, ensure_ascii=False))

        data['percent_of_women_with_cancer_by_race'][
            'by_age'] = percent_race_with_cancer_by_age(json.dumps({
            'age': dd.get('age'),
            'sex': 'Female'
        }, ensure_ascii=False))

        dd.pop('laterality', None)
        dd.pop('site', None)
        dd.pop('type', None)
        dd.pop('stage', None)
        dd.pop('number_of_tumors', None)
        dd.pop('region', None)

        similar_diagnosis = diagnosis(json.dumps(dd, ensure_ascii=False),
                                      limit=20)

        if len(similar_diagnosis) < 20:
            dd.pop('race', None)
            similar_diagnosis = diagnosis(
                json.dumps(dd, ensure_ascii=False), limit=20)

            if len(similar_diagnosis) < 20:
                dd.pop('age', None)
                similar_diagnosis = diagnosis(
                    json.dumps(dd, ensure_ascii=False), limit=20)

        data['similar_diagnosis'] = similar_diagnosis

        return Response(data, status=status.HTTP_200_OK)


class ChartOneView(GenericAPIView):
    serializer_class = DiagnosisSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)

        serializer.is_valid(raise_exception=True)
        dd = dict(serializer.validated_data)

        age = json.dumps({'age': dd.get('age')})
        data = {
            'percent_women_annualy_diagnosed': percent_women_annualy_diagnosed(
                age),
        }
        return Response(data, status=status.HTTP_200_OK)


class ResourcesView(GenericAPIView):
    serializer_class = DiagnosisSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)

        serializer.is_valid(raise_exception=True)
        dd = dict(serializer.validated_data)

        if dd.get('er_status') == '+' and dd.get('pr_status') == '+' \
                and dd.get('her2_status') == '+':
            data = {
                'google_links': [
                    'https://www.sciencedirect.com/science/article/pii/S0305737214002102',
                    'https://www.cbcn.ca/en/blog/our-stories/trishamourot',
                    'http://www.onclive.com/peer-exchange/questions-and-controversies-in-breast-cancer/triplepositive-metastatic-breast-cancer',
                    'https://www.curetoday.com/publications/cure/2017/breast-2017/piling-on-drugs-to-treat-her2positive-breast-cancer',
                    'https://www.medicalnewstoday.com/articles/316789.php',
                    'http://www.practiceupdate.com/content/increased-survival-in-patients-with-triple-positive-metastatic-breast-cancer-treated-with-trastuzumab/54715',
                    'https://www.verywell.com/triple-positive-breast-cancer-4151805',
                    'https://www.webmd.boots.com/breast-cancer/guide/types-er-positive-her2-positive',
                    'https://www.futuremedicine.com/doi/full/10.2217/bmt-2017-0012',
                    'https://rethinkbreastcancer.com/tag/triple-positive/'
                ],
                'blogs_and_posts': [
                    'https://community.breastcancer.org/forum/80/topics/852383',
                    'https://community.macmillan.org.uk/cancer_types/breast-cancer/f/38/t/92558',
                    'https://www.youcaring.com/help-a-neighbor/life-as-a-24-year-old-battling-triple-positive-breast-cancer/146284',
                    'https://every-little-thingblog.com/tag/triple-positive-breast-cancer/',
                    'http://her2support.org/vbulletin/showthread.php?t=23495',
                    'https://www.cbcn.ca/en/blog/our-stories/trishamourot',
                    'https://www.sharecancersupport.org/2008/04/megan-her2-positive-breast-cancer/',
                    'http://stageivnowwhat.blogspot.com/p/blogs-i-follow.html',
                    'http://aftercancernowwhat.blogspot.com.',
                    'http://blog.dana-farber.org/insight/2017/03/eric-winer-breast-cancer-treatment-yesterday-and-tomorrow-a-long-and-winding-road/'
                ],
                'pubmed': [
                    'https://www.ncbi.nlm.nih.gov/pubmed/28523293',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4951261/',
                    'https://www.ncbi.nlm.nih.gov/pubmed/25554445',
                    'https://www.ncbi.nlm.nih.gov/pubmed/27644638',
                    'https://www.ncbi.nlm.nih.gov/pubmed/23278394',
                    'https://www.ncbi.nlm.nih.gov/pubmed/26910921',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4742168/',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4961053/',
                    'https://www.ncbi.nlm.nih.gov/pubmed/29182983',
                    'https://www.ncbi.nlm.nih.gov/pubmed/29019331'
                ],
                'news_articles': [
                    'https://my.clevelandclinic.org/patient-stories/20-mother-overcomes-triple-positive-breast-cancer-diagnosis',
                    'https://www.cancertherapyadvisor.com/breast-cancer/breast-cancer-triple-blockade-her2-treatment-effective/article/735936/',
                    'https://www.nytimes.com/interactive/projects/well/breast-cancer-stories/stories/487',
                    'https://breastcancer-news.com/2017/01/18/tucatinib-ont-380-seen-to-benefit-women-with-heavily-treated-breast-cancer/',
                    'https://www.washingtonpost.com/news/to-your-health/wp/2018/02/01/breast-cancer-treatments-can-raise-risk-of-heart-disease-american-heart-association-warns/',
                    'https://medicalxpress.com/news/2018-02-insight-chromatin-therapies-breast-cancer.html',
                    'https://www.medicalnewstoday.com/articles/320762.php',
                    'https://www.healio.com/hematology-oncology/breast-cancer/news/print/hemonc-today/%7Ba433cfe0-6270-4a3d-bac2-f86edfa7aad5%7D/best-treatment-for-small-her-2positive-node-negative-breast-cancers-unknown',
                    'https://www.themednet.org/what-is-your-preferred-regimen-for-triple-positive-breast-cancer-with-bone-only-recurrence',
                    'https://www.bcm.edu/healthcare/care-centers/breast-care-center/news-events/newsletters/new-treatment-options-horizon-her2-positive'
                ]
            }
        elif dd.get('er_status') == '-' and dd.get('pr_status') == '-' \
                and dd.get('her2_status') == '-':
            data = {
                'google_links': [
                    'http://www.nationalbreastcancer.org/triple-negative-breast-cancer',
                    'https://en.wikipedia.org/wiki/Triple-negative_breast_cancer',
                    'https://ww5.komen.org/uploadedFiles/_Komen/Content/About_Breast_Cancer/Tools_and_Resources/Fact_Sheets_and_Breast_Self_Awareness_Cards/Triple%20Negative%20Breast%20Cancer.pdf',
                    'https://www.medicalnewstoday.com/articles/319240.php',
                    'https://www.webmd.com/breast-cancer/triple-negative-breast-cancer',
                    'https://tnbcfoundation.org/understanding-triple-negative-breast-cancer/',
                    'https://www.mdanderson.org/publications/cancerwise/2015/04/triple-negative-breast-cancer-5-things-you-should-know.html',
                    'https://www.healthline.com/health/triple-negative-breast-cancer-outlook-survival-rates-stage',
                    'https://www.hopkinsmedicine.org/breast_center/breast_cancers_other_conditions/triple_negative_breast_cancer.html',
                    'https://www.sciencedaily.com/releases/2018/02/180208084816.htm',
                ],
                'blogs_and_posts': [
                    'http://www.breastcancer.org/community/acknowledging/triple-negative',
                    'http://www.lbbc.org/diagnosed-triple-negative-breast-cancer',
                    'https://www.sharecancersupport.org/2008/08/how-i-survived-triple-negative-breast-cancer/',
                    'http://www.annpietrangelo.com/cancer_series.php',
                    'https://www.youngsurvival.org/blog/survivor-stories/survivor/jennifer',
                    'https://forum.breastcancercare.org.uk/t5/Triple-negative/Any-triple-negative-survivors-out-there/td-p/685856',
                    'https://netflixandchemo.com/',
                    'http://katydidcancer.blogspot.com/2014/03/day-1358-triple-negative-breast-cancer.html',
                    'http://www.joanlunden.com/category/35-breast-cancer/item/579-what-is-triple-negative-breast-cancer',
                    'https://www.triplenegative.co.uk/blog/',
                ],
                'pubmed': [
                    'https://www.ncbi.nlm.nih.gov/pubmed/21278435',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4881925/',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4181680/',
                    'https://www.ncbi.nlm.nih.gov/pubmed/27249684',
                    'https://www.ncbi.nlm.nih.gov/pubmed/25285241',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2868264/',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5008562/',
                    'https://www.ncbi.nlm.nih.gov/pubmed/21067385',
                    'https://www.ncbi.nlm.nih.gov/pubmed/27221827',
                    'https://www.ncbi.nlm.nih.gov/pubmed/24619745',
                ],
                'news_articles': [
                    'https://www.medicalnewstoday.com/articles/320871.php',
                    'https://medicalxpress.com/news/2018-02-uncovers-therapeutic-aggressive-triple-negative-breast.html',
                    'https://www.dovepress.com/neoadjuvant-treatments-in-triple-negative-breast-cancer-patients-where-peer-reviewed-article-CMAR',
                    'http://www.precisionvaccinations.com/cancer-vaccine-candidate-tpiv200-treating-triple-negative-breast-cancer-launches-phase-2-clinical',
                    'http://www.onclive.com/onclive-tv/dr-bardia-on-sacituzumab-govitecan-in-triplenegative-breast-cancer',
                    'https://www.newsday.com/news/health/breast-cancer-genetic-1.16262137',
                    'https://www.news-medical.net/?tag=/Triple-Negative-Breast-Cancer',
                    'https://www.curetoday.com/articles/big-change-is-coming-for-the-treatment-of-triple-negative-breast-cancer',
                    'https://www.prnewswire.com/news-releases/oncosec-provides-encouraging-clinical-observations-related-to-triple-negative-breast-cancer-study-300584586.html',
                    'http://www.ascopost.com/issues/august-10-2017/advances-in-the-treatment-of-triple-negative-breast-cancer/',
                ]
            }
        elif dd.get('ethnicity') == 'Asian':
            data = {
                'google_links': [
                    'http://ww5.komen.org/BreastCancer/RaceampEthnicity.html',
                    'https://www.curetoday.com/articles/breast-cancer-incidences-increasing-in-asianamerican-women',
                    'https://dceg.cancer.gov/research/cancer-types/breast-cancer/breast-asian-women',
                    'https://www.nbcnews.com/news/asian-america/breast-cancer-rates-rise-among-asian-american-women-others-stay-n749366',
                    'https://www.huffingtonpost.com/entry/asian-american-women-breast-cancer_us_596d181be4b0e983c0584166',
                    'https://www.maurerfoundation.org/breast-cancer-rates-increasing-among-asian-americans/',
                    'http://cancerpreventionresearch.aacrjournals.org/content/early/2017/12/08/1940-6207.CAPR-17-0283',
                    'http://www.breastcancer.org/research-news/20070928',
                    'https://www.cdc.gov/cancer/breast/statistics/race.htm',
                    'https://www.sciencedirect.com/science/article/pii/S0960076009003100'
                ],
                'blogs_and_posts': [
                    'http://www.lbbc.org/node/5882',
                    'https://themighty.com/2018/01/cultural-chasm-challenges-asian-american-breast-cancer-survivor/',
                    'http://www.thermographyclinic.com/blog/entry/the-secret-of-asian-women',
                    'http://www.plumblossoms.me/introduction.html',
                    'http://www.ocbreastwellness.com/question-soy-effect-breast-cancer/',
                    'http://blog.marykayfoundation.org/corporate/archive/2017/05/17/cancer-news-and-how-it-affects-you.aspx',
                    'https://community.breastcancer.org/forum/83/topics/862382?page=1#post_5146038',
                    'http://yourhealthblog.net/more-young-asian-women-are-diagnosed-with-breast-cancer/',
                    'http://blog.angryasianman.com/2016/10/why-asian-breast-cancer.html',
                    'https://www.sbi-online.org/endtheconfusion/Blog/TabId/546/ArtMID/1586/ArticleID/407/Racial-Disparities-in-Breast-Cancer-Screening.aspx',
                ],
                'pubmed': [
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2837454/',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2853623/',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5160133/',
                    'https://www.ncbi.nlm.nih.gov/pubmed/20147696',
                    'https://www.ncbi.nlm.nih.gov/pubmed/22638769',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4929251/',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4069805/',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4607827/',
                    'https://www.ncbi.nlm.nih.gov/pubmed/17387549',
                    'https://www.ncbi.nlm.nih.gov/pubmed/25374197',
                ],
                'news_articles': [
                    'http://www.abc.net.au/news/health/2018-02-03/how-cultural-barriers-can-hamper-breast-cancer-screening/9391388',
                    'http://sampan.org/2018/02/duke-university-seeking-chinese-japanese-and-korean-breast-cancer-survivors-for-study/',
                    'http://gulftoday.ae/portal/79f8e21e-70bc-4175-9fbf-ffb8a0374eb8.aspx',
                    'http://www.asianage.com/life/health/080218/breast-cancer-survivors-may-die-of-heart-disease-doctors-warn.html',
                    'https://www.medicalnewstoday.com/articles/320683.php',
                    'https://www.bustle.com/p/what-the-age-you-got-your-first-period-at-says-about-your-health-according-to-science-8064600',
                    'http://www.businesstimes.com.sg/brunch/out-of-the-loop',
                    'https://www.curetoday.com/articles/breast-cancer-incidences-increasing-in-asianamerican-women',
                    'http://managedhealthcareexecutive.modernmedicine.com/managed-healthcare-executive/news/asian-american-women-need-better-targeted-breast-cancer-therapy',
                    'http://www.scmp.com/lifestyle/health-beauty/article/2116762/two-big-myths-about-breast-cancer-and-what-hong-kong-women',
                ]
            }
        elif dd.get('ethnicity') == 'African American':
            data = {
                'google_links': [
                    'http://www.sistersnetworkinc.org/breastcancerfacts.html',
                    'http://theoncologist.alphamedpress.org/content/10/1/1.full',
                    'https://www.bwhi.org/2017/07/20/black-women-breast-cancer-diagnosis-care/',
                    'https://www.cancer.org/latest-news/report-breast-cancer-rates-rising-among-african-american-women.html',
                    'https://www.cdc.gov/healthcommunication/toolstemplates/entertainmented/tips/BreastCancerAfricanAmerican.html',
                    'https://aabcainc.org/facts-to-know/',
                    'https://www.bcrf.org/blog/why-black-women-are-more-likely-die-breast-cancer',
                    'https://blackdoctor.org/515014/breaking-black-woman-developed-alternative-to-breast-cancer-treatment/',
                    'https://www.webmd.com/breast-cancer/news/20161003/breast-cancer-deaths-black-women',
                    'https://www.cancer.gov/about-nci/organization/crchd/cancer-health-disparities-fact-sheet',
                ],
                'blogs_and_posts': [
                    'http://www.lbbc.org/african-american',
                    'https://community.breastcancer.org/forum/98',
                    'http://nautil.us/blog/why-are-black-women-more-likely-to-die-from-breast-cancer',
                    'https://www.onemedical.com/blog/live-well/black-women-breast-cancer/',
                    'https://publichealthmatters.blog.gov.uk/2016/12/08/improving-understanding-of-breast-cancer-survival-in-black-women/',
                    'http://blog.thebreastcancersite.com/exercise-reduces-breast-cancer-risk-in-african-american-women/',
                    'http://www.criteriuminc.com/wordpress/index.php/2017/10/',
                    'https://www.cityofhope.org/blog/black-women-breast-cancer',
                ],
                'pubmed': [
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3955723/',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1447112/',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2568204/',
                    'https://www.ncbi.nlm.nih.gov/pubmed/16951137',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4730397/',
                    'https://www.ncbi.nlm.nih.gov/pubmed/27995352',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3603001/',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4879045/',
                    'https://www.ncbi.nlm.nih.gov/pubmed/23539135',
                    'https://www.ncbi.nlm.nih.gov/pubmed/25673085',
                ],
                'news_articles': [
                    'http://www.nydailynews.com/life-style/breast-cancer-kills-black-women-higher-rate-white-women-article-1.3553618',
                    'https://www.hsph.harvard.edu/news/features/jim-crow-breast-cancer-black-women/',
                    'http://www.13wmaz.com/news/local/alarming-statistic-shows-african-american-women-more-likely-to-die-from-breast-cancer/512621965',
                    'http://www.radiologybusiness.com/topics/care-delivery/obstacle-or-death-sentence-how-women%E2%80%99s-experiences-shape-their-views-breast-cancer',
                    'https://www.oncologynurseadvisor.com/breast-cancer/cardiotoxicity-risk-greater-in-blacks-with-breast-cancer-receiving-her2-therapies/article/741433/',
                    'https://www.alcoholproblemsandsolutions.org/risk-of-breast-cancer-in-african-american-women/',
                    'https://www.reuters.com/article/us-health-breastcancer-insurance-mortali/insurance-a-major-factor-in-blacks-higher-breast-cancer-mortality-idUSKBN1CO21Q',
                    'https://www.blackwomenshealth.org/issues-and-resources/black-women-and-breast-cancer.html',
                    'https://health.usnews.com/health-care/articles/2017-11-15/diabetes-may-be-driving-high-rates-of-breast-cancer-in-black-women',
                    'https://uknowledge.uky.edu/comm_etds/63/',
                ]
            }
        elif dd.get('age') < 40:
            data = {
                'google_links': [
                    'https://ww5.komen.org/BreastCancer/YoungWomenandBreastCancer.html',
                    'https://www.webmd.com/breast-cancer/breast-cancer-young-women',
                    'http://www.lbbc.org/young-woman-breast-cancer',
                    'https://www.healthline.com/health/breast-cancer/breast-cancer-in-young-women',
                    'https://www.breastcancercare.org.uk/sites/default/files/publications/pdf/bcc66_younger_women_with_breast_cancer_web.pdf',
                    'https://www.usatoday.com/story/news/nation/2013/02/26/breast-cancers-young-women/1949157/',
                    'https://breast-cancer-research.biomedcentral.com/articles/10.1186/bcr2647',
                    'https://www.medicinenet.com/breast_cancer_in_young_women/article.htm',
                    'http://www.ascopost.com/issues/may-25-2017/unique-challenges-facing-young-women-with-breast-cancer/',
                    'http://www.dana-farber.org/young-and-strong-program-for-young-women-with-breast-cancer/',
                ],
                'blogs_and_posts': [
                    'http://www.flare.com/health/young-women-with-breast-cancer/',
                    'https://www.youngsurvival.org/blog/survivor-stories/survivor/jennifer',
                    'http://youngwomensbreastcancerblog.blogspot.com/',
                    'http://www.butdoctorihatepink.com/',
                    'http://www.letlifehappen.com/',
                    'http://carolinemfr.blogspot.com/',
                    'http://nancyspoint.com/',
                    'http://www.tamiboehmer.com/',
                    'https://perksofcancer.com/',
                    'http://www.beautythroughthebeast.com/blog',
                ],
                'pubmed': [
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4303229/',
                    'https://www.ncbi.nlm.nih.gov/pubmed/24074783',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3695538/',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4694614/',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2894028/',
                    'https://www.ncbi.nlm.nih.gov/pubmed/28260181',
                    'https://www.ncbi.nlm.nih.gov/pubmed/17059343',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2770847/',
                    'https://www.ncbi.nlm.nih.gov/pubmed/18501818',
                    'https://www.ncbi.nlm.nih.gov/pubmed/27479041',
                ],
                'news_articles': [
                    'http://www.sacbee.com/news/local/health-and-medicine/article108330857.html',
                    'https://www.statnews.com/2017/08/29/double-mastectomy-breast-cancer/',
                    'https://economictimes.indiatimes.com/magazines/panache/breast-cancer-rates-are-on-the-rise-among-young-women-and-heres-how-you-can-prevent-it/articleshow/62803645.cms',
                    'http://www.columbian.com/news/2018/jan/22/breast-cancer-surgeon-diagnosed-with-breast-cancer-advocates-oncoplastic-surgery/',
                    'https://www.thesun.ie/fabulous/2044496/young-irish-mum-urges-women-to-be-aware-of-breast-cancer-after-being-diagnosed-with-condition-at-32-and-seven-months-after-giving-birth/',
                    'http://www.jamaicaobserver.com/your-health-your-wealth/breast-cancer_122442?profile=1373',
                    'https://www.medicalnewstoday.com/articles/320387.php',
                    'https://www.forbes.com/sites/elaineschattner/2017/12/07/in-young-women-kisqali-slows-metastatic-breast-cancer-and-relieves-symptoms/',
                    'http://people.com/human-interest/young-women-breast-cancer/',
                    'http://www.healthimaging.com/topics/womens-health/breast-imaging/bi-annual-mris-more-effective-mammograms-high-risk-young-women',
                ]
            }
        elif dd.get('age') > 70:
            data = {
                'google_links': [
                    'http://www.breastcancer.org/research-news/20120207',
                    'http://theoncologist.alphamedpress.org/content/15/suppl_5/57.full',
                    'http://ascopubs.org/doi/full/10.1200/jop.2015.010207',
                    'https://www.everydayhealth.com/news/letting-go-radiation-older-women-with-breast-cancer/',
                    'https://www.medscape.com/viewarticle/817435',
                    'https://www.health.harvard.edu/cancer/good-news-about-early-stage-breast-cancer-for-older-women',
                    'https://www.omicsonline.org/open-access/treatment-of-breast-cancer-in-women-aged-80-and-older-a-systematic-review-.php?aid=82098',
                    'https://www.aafp.org/afp/1998/1001/p1163.html',
                    'https://www.sciencedirect.com/science/article/pii/S1507136712000831',
                    'https://www.griswoldhomecare.com/blog/treatment-to-prognosis-breast-cancer-care-for-elderly-women/',
                ],
                'blogs_and_posts': [
                    'http://blog.dana-farber.org/insight/2015/08/what-older-women-should-know-about-breast-cancer/',
                    'https://community.breastcancer.org/forum/104',
                    'http://www.joanlunden.com/category/49-breast-cancer-home/item/122-i-have-breast-cancer',
                    'https://medschool.duke.edu/about-us/news-and-communications/med-school-blog/older-breast-cancer-patients-defy-survival-models',
                    'https://www.vitae-care.com/blog/breast-cancer-in-older-age',
                    'https://www.aplaceformom.com/senior-care-resources/articles/breast-cancer-in-seniors',
                    'http://www.lbbc.org/blog',
                    'https://cancer.osu.edu/blog/personalized-breast-cancer-treatment-for-older-women',
                    'https://www.bcrf.org/blog/breast-cancer-elderly-how-bcrf-researchers-are-treating-growing-patient-population',
                    'http://blog.thebreastcancersite.com/',
                ],
                'pubmed': [
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3874410/',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4500607/',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4577665/',
                    'https://www.ncbi.nlm.nih.gov/pubmed/25993142',
                    'https://www.ncbi.nlm.nih.gov/pubmed/1430878',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3745823/',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC222918/',
                    'https://www.ncbi.nlm.nih.gov/pubmed/14581426',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4745843/',
                    'https://www.ncbi.nlm.nih.gov/pubmed/17050874',
                ],
                'news_articles': [
                    'https://www.reuters.com/article/us-breast-cancer/breast-cancer-may-not-change-lifespan-for-older-women-idUSTRE72D7XU20110315',
                    'https://medicalxpress.com/news/2018-02-family-history-breast-cancer-older.html',
                    'https://www.healio.com/internal-medicine/oncology/news/online/%7B04c3ab00-a29b-4f86-af55-9b6b906aa9db%7D/family-history-increases-breast-cancer-risk-regardless-of-age',
                    'http://www.dailymail.co.uk/news/article-5374323/Patients-breast-cancer-live-longer-soft-chemo.html',
                    'https://www.deccanchronicle.com/lifestyle/health-and-wellbeing/270118/older-women-with-high-body-fat-at-increased-risk-of-breast-cancer-stu.html',
                    'https://www.eurekalert.org/pub_releases/2018-01/wkh-dbr013018.php',
                    'https://medicalxpress.com/news/2018-02-soft-chemotherapy-effective-older-patients.html',
                    'http://www.pharmacytimes.com/publications/health-system-edition/2018/january2018/breast-cancer-the-clinicians-involvement',
                    'https://www.irishtimes.com/life-and-style/health-family/after-cancer-relapse-is-the-biggest-fear-but-not-the-only-risk-1.3381974',
                    'https://scroll.in/pulse/868165/while-fighting-breast-cancer-one-woman-also-fought-to-keep-her-breast',
                ]
            }
        else:
            data = {
                'google_links': [
                    'http://www.breastcancer.org/',
                    'https://www.mayoclinic.org/diseases-conditions/breast-cancer/symptoms-causes/syc-20352470',
                    'https://www.medicalnewstoday.com/articles/37136.php',
                    'https://www.cancer.org/cancer/breast-cancer.html',
                    'https://en.wikipedia.org/wiki/Breast_cancer',
                    'https://medlineplus.gov/breastcancer.html',
                    'http://www.health.com/breast-cancer',
                    'https://www.cancer.gov/types/breast',
                    'http://www.nationalbreastcancer.org/breast-cancer-facts',
                    'http://www.nationalbreastcancer.org/',
                ],
                'blogs_and_posts': [
                    'http://hormonenegative.blogspot.com/',
                    'http://www.lbbc.org/blog',
                    'https://breastcancer-news.com/blog/2016/07/13/dealing-with-breast-cancer-diagnosis/',
                    'http://mywifesfightwithbreastcancer.com/blog/',
                    'http://carolinemfr.blogspot.com/',
                    'https://www.blogforacure.com/members.php?type=breast+cancer',
                    'http://liz.oriordan.co.uk/',
                    'https://michelle-giannino.squarespace.com/',
                    'https://www.breastcancercare.org.uk/information-support/vita-magazine/blog',
                    'http://www.nalie.ca/',
                ],
                'pubmed': [
                    'https://www.ncbi.nlm.nih.gov/pubmedhealth/PMH0001911/',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3255438/',
                    'https://www.ncbi.nlm.nih.gov/pubmedhealth/PMH0072606/',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4135458/',
                    'https://www.ncbi.nlm.nih.gov/pubmed/15894099',
                    'https://www.ncbi.nlm.nih.gov/pubmed/11902563',
                    'https://www.ncbi.nlm.nih.gov/pubmed/16045991',
                    'https://www.ncbi.nlm.nih.gov/pubmed/22990110',
                    'https://www.ncbi.nlm.nih.gov/pubmed/17975657',
                    'https://www.ncbi.nlm.nih.gov/pubmed/21310842',
                ],
                'news_articles': [
                    'http://www.nytimes.com/2013/04/28/magazine/our-feel-good-war-on-breast-cancer.html?pagewanted=all',
                    'https://www.usatoday.com/story/news/2017/09/28/julia-louis-dreyfus-breast-cancer-announcement-just-latest-show-evolution-stigma-spotlight/707775001/',
                    'http://time.com/4057310/breast-cancer-overtreatment/',
                    'https://www.healio.com/hematology-oncology/breast-cancer/news/in-the-journals/%7B2534af47-24ab-4366-bce9-f71f851ee40a%7D/residence-in-ethnic-enclaves-associated-with-reduced-breast-colorectal-cancer-risk-among-asians-hispanics',
                    'http://scienceblog.cancerresearchuk.org/2017/10/12/5-persistent-myths-about-the-causes-of-breast-cancer/',
                    'https://www.statnews.com/2017/07/10/breast-cancer-chemotherapy/',
                    'https://www.nature.com/articles/d41586-017-08309-y',
                    'https://www.statnews.com/2017/10/23/breast-cancer-radiation/',
                    'https://www.statnews.com/2017/08/29/double-mastectomy-breast-cancer/',
                    'https://www.dovepress.com/toxic-elements-as-biomarkers-for-breast-cancer-a-meta-analysis-study-peer-reviewed-article-CMAR',
                    'http://www.citywatchla.com/index.php/neighborhood-politics-hidden/370-420-file-news/14594-is-cannabis-a-treatment-for-cancer',
                    'http://www.nature.com/articles/nrclinonc.2017.143',
                ]
            }

        return Response(data, status=status.HTTP_200_OK)


class TestDataView(GenericAPIView):
    serializer_class = DiagnosisSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)

        serializer.is_valid(raise_exception=True)
        dd = dict(serializer.validated_data)

        age = json.dumps({'age': dd.get('age')})

        ethnicity = dd.get('ethnicity')

        if ethnicity == 'Caucasian':
            v_ethnicity = 'White'
        elif ethnicity == 'African American':
            v_ethnicity = 'Black'
        elif ethnicity == 'Asian':
            v_ethnicity = 'Asian or Pacific Islander'
        elif ethnicity == 'Other':
            v_ethnicity = 'Unknown'
        else:
            v_ethnicity = ethnicity

        is_radiation_therapy = 'No'  # Radiation Therapy

        # Recommended Treatment Plans

        ## Overall Plans

        try:
            import subprocess
            import ast
            import re
            regex = r"\((.*?)\)"

            # START SURGERY
            surgery_args = ','.join([dd.get('sex'),
                                     str(dd.get('age')),
                                     v_ethnicity,
                                     str(float(dd.get('tumor_grade', 'unk'))),
                                     dd.get('site'),
                                     dd.get('type'),
                                     dd.get('stage'),
                                     dd.get('region'),
                                     v_get_t_size_cm(
                                         dd.get('tumor_size_in_mm')),
                                     str(dd.get('number_of_tumors')),
                                     str(dd.get('num_pos_nodes'))])

            surgery_command_str = [settings.ML_PYTHON_PATH,
                                   settings.ML_COMMAND_FILE,
                                   surgery_args, 'Surgery']

            surgery_command = subprocess.Popen(surgery_command_str,
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE,
                                               cwd=settings.ML_COMMAND_DIR)
            surgery_output, err = surgery_command.communicate()

            # To-Do remove try-except
            try:
                surgery_response = ast.literal_eval(
                    re.search(regex,
                              str(surgery_output.decode('utf8'))).group())
            except:
                surgery_response = ()

            # END SURGERY

            # START CHEMO

            chemo_args = ','.join([
                str(dd.get('age')),
                v_ethnicity,
                str(float(dd.get('tumor_grade'))),
                dd.get('type'),
                dd.get('stage'),
                dd.get('region'),
                v_get_t_size_cm(dd.get('tumor_size_in_mm')),
                str(dd.get('number_of_tumors')),
                str(dd.get('num_pos_nodes')),
                str(dd.get('er_status')),
                str(dd.get('pr_status')),
                str(dd.get('her2_status'))])

            chemo_command_str = [settings.ML_PYTHON_PATH,
                                 settings.ML_COMMAND_FILE,
                                 chemo_args, 'Chemo']

            chemo_command = subprocess.Popen(chemo_command_str,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE,
                                             cwd=settings.ML_COMMAND_DIR)
            chemo_output, err = chemo_command.communicate()

            chemo_response = ast.literal_eval(
                re.search(regex, str(chemo_output.decode('utf8'))).group())

            # END CHEMO

            # START RADIATION

            import copy

            radiation_args = [
                str(dd.get('age')),
                v_ethnicity,
                str(float(dd.get('tumor_grade'))),
                dd.get('site'),
                dd.get('type'),
                dd.get('stage'),
                dd.get('region'),
                v_get_t_size_cm(dd.get('tumor_size_in_mm')),
                str(dd.get('number_of_tumors')),
                str(dd.get('num_pos_nodes')),
                str(dd.get('er_status')),
                str(dd.get('pr_status')),
                str(dd.get('her2_status'))]

            sm_radiation_args = copy.deepcopy(
                radiation_args)  # Copy base list of args

            sm_radiation_args.append('Mastectomy')
            sm_radiation_args.append(chemo_response[0])

            sm_radiation_command_str = [settings.ML_PYTHON_PATH,
                                        settings.ML_COMMAND_FILE,
                                        ','.join(sm_radiation_args),
                                        'Radiation']

            sm_radiation_command = subprocess.Popen(sm_radiation_command_str,
                                                    stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE,
                                                    cwd=settings.ML_COMMAND_DIR)

            sm_radiation_output, err = sm_radiation_command.communicate()

            sm_radiation_response = ast.literal_eval(
                re.search(regex,
                          str(sm_radiation_output.decode('utf8'))).group())

            sl_radiation_args = copy.deepcopy(
                radiation_args)  # Copy base list of args

            sl_radiation_args.append('Lumpectomy')
            sl_radiation_args.append(chemo_response[0])

            sl_radiation_command_str = [settings.ML_PYTHON_PATH,
                                        settings.ML_COMMAND_FILE,
                                        ','.join(sm_radiation_args),
                                        'Radiation']

            sl_radiation_command = subprocess.Popen(sl_radiation_command_str,
                                                    stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE,
                                                    cwd=settings.ML_COMMAND_DIR)
            sl_radiation_output, err = sl_radiation_command.communicate()

            sl_radiation_response = ast.literal_eval(
                re.search(regex,
                          str(sl_radiation_output.decode('utf8'))).group())

            # END RADIATION

            overall_plans = []

            surgery_level = round(surgery_response[1] * 100)
            chemo_level = round(chemo_response[1] * 100)
            sm_radiation_level = round(sm_radiation_response[1] * 100)
            sl_radiation_level = round(sl_radiation_response[1] * 100)

            if surgery_response[0] == 'Mastectomy':
                is_radiation_therapy = sm_radiation_response[0]
                overall_plans.append({
                    'name': 'Preferred Outcome A',
                    'type': surgery_response[0],
                    'radiation': 'Y' if sm_radiation_response[
                                            0] == 'Yes' else 'N',
                    'radiation_confidence_level': sm_radiation_level,
                    'chemo': 'Y' if chemo_response[0] == 'Yes' else 'N',
                    'chemo_confidence_level': chemo_level,
                    'surgery': 'Y',
                    'surgery_confidence_level': surgery_level,
                    'level': surgery_level})
                overall_plans.append({
                    'name': 'Preferred Outcome B',
                    'type': 'Lumpectomy',
                    'radiation': 'Y' if sl_radiation_response[
                                            0] == 'Yes' else 'N',
                    'radiation_confidence_level': sl_radiation_level,
                    'chemo': 'Y' if chemo_response[0] == 'Yes' else 'N',
                    'chemo_confidence_level': chemo_level,
                    'surgery': 'Y',
                    'surgery_confidence_level': 100 - surgery_level,
                    'level': 100 - surgery_level})
            else:
                is_radiation_therapy = sl_radiation_response[0]
                overall_plans.append({
                    'name': 'Preferred Outcome A',
                    'type': surgery_response[0],
                    'radiation': 'Y' if sl_radiation_response[
                                            0] == 'Yes' else 'N',
                    'radiation_confidence_level': sl_radiation_level,
                    'chemo': 'Y' if chemo_response[0] == 'Yes' else 'N',
                    'chemo_confidence_level': chemo_level,
                    'surgery_confidence_level': surgery_level,
                    'surgery': 'Y',
                    'level': surgery_level})
                overall_plans.append({
                    'name': 'Preferred Outcome B',
                    'type': 'Mastectomy',
                    'radiation': 'Y' if sm_radiation_response[
                                            0] == 'Yes' else 'N',
                    'radiation_confidence_level': sm_radiation_level,
                    'chemo': 'Y' if chemo_response[0] == 'Yes' else 'N',
                    'chemo_confidence_level': chemo_level,
                    'surgery_confidence_level': 100 - surgery_level,
                    'surgery': 'Y',
                    'level': 100 - surgery_level})
        except Exception as e:
            overall_plans = []

        # Hormonal Therapy

        hormonal_therapy = []
        if dd.get('pr_status') == '+' or dd.get('er_status') == '+':
            hormonal_therapy.append({'name': 'Tamoxifen',
                                     'number_of_treatments': 120,
                                     'administration': 'Monthly'})

        # Radiation Therapy

        radiation_therapy = []
        if is_radiation_therapy == 'Yes':
            radiation_therapy.append({'name': 'Beam Radiation',
                                      'number_of_treatments': 30,
                                      'administration': 'Daily'})

        # Chemo Therapy

        data = {
            'recommended_treatment_plans': {
                'overall_plans': overall_plans,
                'hormonal_therapy': hormonal_therapy,
                'radiation_therapy': radiation_therapy,
            },
            'percent_women_annualy_diagnosed': percent_women_annualy_diagnosed(
                age),
            'percent_women_by_type': percent_women_by_type(),
            'breast_cancer_by_grade_and_size': {
                'grade': breast_cancer_by_grade(age),
                'size': breast_cancer_by_size(age)
            },
            'distribution_of_stage_of_cancer': {
                'overall': distribution_of_stage_of_cancer(age),
                'by_race':
                    distribution_of_stage_of_cancer(
                        json.dumps({'age': dd.get('age'),
                                    'ethnicity': ethnicity},
                                   ensure_ascii=False)),
            },
            'percent_of_women_with_cancer_by_race': {
                'overall': percent_of_women_with_cancer_by_race_overall()
            },
            'surgery_decisions': surgery_decisions(age),
            'chemotherapy': {
                'overall': chemotherapy(age),
            },
            'radiation': {
                'overall': radiation(age),
            },
            'breast_cancer_by_state': breast_cancer_by_state(),
            'breast_cancer_at_a_glance': breast_cancer_at_a_glance(),
            'breast_cancer_by_age': breast_cancer_by_age(),
        }

        data['chemotherapy']['breakout_by_stage'] = breakout_by_stage(
            json.dumps({
                'age': dd.get('age'),
                'chemo': 'Yes',
                "breast-adjusted-ajcc-6th-stage-1988": {
                    "$in": ["I", "IIA", "IIB", "IIIA",
                            "IIIB", "IIIC", "IIINOS", "IV",
                            0]
                }}, ensure_ascii=False))

        data['radiation']['breakout_by_stage'] = breakout_by_stage(json.dumps({
            'age': dd.get('age'),
            'radiation': 'Yes',
            "breast-adjusted-ajcc-6th-stage-1988": {
                "$in": ["I", "IIA", "IIB", "IIIA",
                        "IIIB", "IIIC", "IIINOS", "IV",
                        0]
            }}, ensure_ascii=False))

        data['percent_of_women_with_cancer_by_race'][
            'by_age'] = percent_race_with_cancer_by_age(json.dumps({
            'age': dd.get('age'),
            'sex': 'Female'
        }, ensure_ascii=False))

        dd.pop('laterality', None)
        dd.pop('site', None)
        dd.pop('type', None)
        dd.pop('stage', None)
        dd.pop('number_of_tumors', None)
        dd.pop('region', None)

        similar_diagnosis = diagnosis(json.dumps(dd, ensure_ascii=False),
                                      limit=20)

        if len(similar_diagnosis) < 20:
            dd.pop('tumor_size_in_mm', None)
            similar_diagnosis = diagnosis(json.dumps(dd, ensure_ascii=False),
                                          limit=20)

            if len(similar_diagnosis) < 20:
                dd.pop('race', None)
                similar_diagnosis = diagnosis(
                    json.dumps(dd, ensure_ascii=False), limit=20)

                if len(similar_diagnosis) < 20:
                    dd.pop('age', None)
                    similar_diagnosis = diagnosis(
                        json.dumps(dd, ensure_ascii=False), limit=20)

        data['similar_diagnosis'] = similar_diagnosis

        return Response(data, status=status.HTTP_200_OK)
