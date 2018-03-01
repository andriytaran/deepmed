import json

from channels.generic.websocket import JsonWebsocketConsumer
from django.conf import settings
from pymongo import MongoClient

from base.serializers import DiagnosisDataSerializer, CustomAnalyticsSerializer
from lib.bcancer_ca import custom_analytics, chemo_decisions, surgery_decisions
from lib.dataset import surgery_decisions as ind_surgery_decisions
from lib.dataset import percent_women_by_type, breast_cancer_by_grade, \
    breast_cancer_by_size, distribution_of_stage_of_cancer, \
    percent_of_women_with_cancer_by_race_overall, \
    chemotherapy, radiation, percent_race_with_cancer_by_age, \
    breast_cancer_by_state2, \
    breast_cancer_at_a_glance2, breast_cancer_by_age, \
    percent_women_annualy_diagnosed, chemotherapy_filter, radiation_filter, \
    MONGODB_HOST, MONGODB_PORT, COLLECTION_NAME, DBS_NAME
from .ML.predictions import make_pred


class DiagnosisConsumer(JsonWebsocketConsumer):
    serializer_class = DiagnosisDataSerializer

    def connect(self):
        # Called on connection. Either call
        if self.scope['user']:
            self.accept()
        else:
            self.close()

    def receive_json(self, content, **kwargs):
        content['user'] = self.scope['user'].id
        # Remove empty strings
        content = dict((k, v) for k, v in content.items() if v)
        serializer = self.serializer_class(data=content)

        if not serializer.is_valid():
            self.send_json({'error': 'Data not valid.',
                            'extra': serializer.errors})

        dd = serializer.validated_data

        serializer.save()

        dd['user'] = str(self.scope['user'].id)

        # Recommended Treatment Plans

        try:
            import subprocess
            import ast
            import re
            regex = r"\((.*?)\)"

            surgery_response = (None, None)
            sm_radiation_response = (None, None)
            sl_radiation_response = (None, None)
            none_radiation_response = (None, None)
            # START SURGERY
            if dd.get('tumor_size_in_mm_sd') > 0:
                surgery_args = ','.join([dd.get('sex', 'Female'),
                                         str(dd.get('age')),
                                         dd.get('ethnicity'),
                                         str(float(
                                             dd.get('tumor_grade', 'unk'))),
                                         dd.get('site'),
                                         dd.get('type'),
                                         dd.get('stage'),
                                         dd.get('region'),
                                         dd.get('tumor_size_in_mm'),
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

                if not surgery_output:
                    self.send_json({'error': 'Surgery command failed'})

                surgery_response = ast.literal_eval(
                    re.search(regex,
                              str(surgery_output.decode('utf8'))).group())
            else:
                pass
            # END SURGERY

            # START CHEMO

            chemo_args = ','.join([
                str(dd.get('age')),
                dd.get('ethnicity'),
                str(float(dd.get('tumor_grade'))),
                dd.get('type'),
                dd.get('stage'),
                dd.get('region'),
                dd.get('tumor_size_in_mm'),
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

            if not chemo_output:
                self.send_json({'error': 'Chemo command failed'})

            chemo_response = ast.literal_eval(
                re.search(regex, str(chemo_output.decode('utf8'))).group())

            # END CHEMO

            # START RADIATION

            import copy

            radiation_args = [
                str(dd.get('age')),
                dd.get('ethnicity'),
                str(float(dd.get('tumor_grade'))),
                dd.get('site'),
                dd.get('type'),
                dd.get('stage'),
                dd.get('region'),
                dd.get('tumor_size_in_mm'),
                str(dd.get('number_of_tumors')),
                str(dd.get('num_pos_nodes')),
                str(dd.get('er_status')),
                str(dd.get('pr_status')),
                str(dd.get('her2_status'))]

            if dd.get('tumor_size_in_mm_sd') == 0:
                none_radiation_args = copy.deepcopy(
                    radiation_args)  # Copy base list of args

                none_radiation_args.append('None')
                none_radiation_args.append(chemo_response[0])

                none_radiation_command_str = [settings.ML_PYTHON_PATH,
                                              settings.ML_COMMAND_FILE,
                                              ','.join(none_radiation_args),
                                              'Radiation']

                none_radiation_command = subprocess.Popen(
                    none_radiation_command_str,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=settings.ML_COMMAND_DIR)

                none_radiation_output, err = none_radiation_command.communicate()

                if not none_radiation_output:
                    self.send_json(
                        {'error': 'Radiation "None" command failed'})

                none_radiation_response = ast.literal_eval(
                    re.search(regex,
                              str(none_radiation_output.decode(
                                  'utf8'))).group())

            elif dd.get('tumor_size_in_mm_sd') > 0:

                sm_radiation_args = copy.deepcopy(
                    radiation_args)  # Copy base list of args

                sm_radiation_args.append('Mastectomy')
                sm_radiation_args.append(chemo_response[0])

                sm_radiation_command_str = [settings.ML_PYTHON_PATH,
                                            settings.ML_COMMAND_FILE,
                                            ','.join(sm_radiation_args),
                                            'Radiation']

                sm_radiation_command = subprocess.Popen(
                    sm_radiation_command_str,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=settings.ML_COMMAND_DIR)

                sm_radiation_output, err = sm_radiation_command.communicate()

                if not sm_radiation_output:
                    self.send_json(
                        {'error': 'Radiation "Mastectomy" command failed'})

                sm_radiation_response = ast.literal_eval(
                    re.search(regex,
                              str(sm_radiation_output.decode('utf8'))).group())

                sl_radiation_args = copy.deepcopy(
                    radiation_args)  # Copy base list of args

                sl_radiation_args.append('Lumpectomy')
                sl_radiation_args.append(chemo_response[0])

                sl_radiation_command_str = [settings.ML_PYTHON_PATH,
                                            settings.ML_COMMAND_FILE,
                                            ','.join(sl_radiation_args),
                                            'Radiation']

                sl_radiation_command = subprocess.Popen(
                    sl_radiation_command_str,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=settings.ML_COMMAND_DIR)
                sl_radiation_output, err = sl_radiation_command.communicate()

                if not sl_radiation_output:
                    self.send_json(
                        {'error': 'Radiation "Lumpectomy" command failed'})

                sl_radiation_response = ast.literal_eval(
                    re.search(regex,
                              str(sl_radiation_output.decode('utf8'))).group())

            # END RADIATION

            overall_plans = []

            chemo_level = round(chemo_response[1] * 100)
            if dd.get('tumor_size_in_mm_sd') > 0:
                surgery_level = round(surgery_response[1] * 100)
                sm_radiation_level = round(sm_radiation_response[1] * 100)
                sl_radiation_level = round(sl_radiation_response[1] * 100)

                if (surgery_response[0] == 'Lumpectomy' and surgery_level < 50) \
                        or (surgery_response[
                                0] == 'Mastectomy' and surgery_level >= 50):
                    overall_plans.append({
                        'name': 'Preferred Outcome A',
                        'type': 'Mastectomy',
                        'radiation': 'Yes' if sm_radiation_response[
                                                  0] == 'Yes' else 'No',
                        'radiation_confidence_level': sm_radiation_level,
                        'chemo': 'Yes' if chemo_response[0] == 'Yes' else 'No',
                        'chemo_confidence_level': chemo_level,
                        'surgery': 'Yes',
                        'surgery_confidence_level': surgery_level if
                        surgery_response[
                            0] == 'Mastectomy' else 100 - surgery_level
                    })
                    overall_plans.append({
                        'name': 'Preferred Outcome B',
                        'type': 'Lumpectomy',
                        'radiation': 'Yes' if sl_radiation_response[
                                                  0] == 'Yes' else 'No',
                        'radiation_confidence_level': sl_radiation_level,
                        'chemo': 'Yes' if chemo_response[0] == 'Yes' else 'No',
                        'chemo_confidence_level': chemo_level,
                        'surgery': 'Yes',
                        'surgery_confidence_level': 100 - surgery_level if
                        surgery_response[0] == 'Mastectomy' else surgery_level
                    })
                elif (surgery_response[
                          0] == 'Mastectomy' and surgery_level < 50) \
                        or (surgery_response[
                                0] == 'Lumpectomy' and surgery_level >= 50):
                    overall_plans.append({
                        'name': 'Preferred Outcome A',
                        'type': 'Lumpectomy',
                        'radiation': 'Yes' if sl_radiation_response[
                                                  0] == 'Yes' else 'No',
                        'radiation_confidence_level': sl_radiation_level,
                        'chemo': 'Yes' if chemo_response[0] == 'Yes' else 'No',
                        'chemo_confidence_level': chemo_level,
                        'surgery': 'Yes',
                        'surgery_confidence_level': surgery_level if
                        surgery_response[
                            0] == 'Lumpectomy' else 100 - surgery_level
                    })
                    overall_plans.append({
                        'name': 'Preferred Outcome B',
                        'type': 'Mastectomy',
                        'radiation': 'Yes' if sm_radiation_response[
                                                  0] == 'Yes' else 'No',
                        'radiation_confidence_level': sm_radiation_level,
                        'chemo': 'Yes' if chemo_response[0] == 'Yes' else 'No',
                        'chemo_confidence_level': chemo_level,
                        'surgery': 'Yes',
                        'surgery_confidence_level': 100 - surgery_level if
                        surgery_response[0] == 'Lumpectomy' else surgery_level
                    })
            elif dd.get('tumor_size_in_mm_sd') == 0:
                none_radiation_level = round(none_radiation_response[1] * 100)
                overall_plans.append({
                    'name': 'None',
                    'type': 'N/A',
                    'radiation': 'Yes' if none_radiation_response[
                                              0] == 'Yes' else 'No',
                    'radiation_confidence_level': none_radiation_level,
                    'chemo': 'Yes' if chemo_response[0] == 'Yes' else 'No',
                    'chemo_confidence_level': chemo_level,
                    'surgery': 'No',
                    'surgery_confidence_level': 'N/A'
                })

            self.send_json({'overall_plans': overall_plans})

            if dd.get('ethnicity') == 'White':
                dd['ethnicity'] = 'Caucasian'
            elif dd.get('ethnicity') == 'Black':
                dd['ethnicity'] = 'African American'
            elif dd.get('ethnicity') == 'Asian or Pacific Islander':
                dd['ethnicity'] = 'Asian'
            elif dd.get('ethnicity') == 'Unknown':
                dd['ethnicity'] = 'Other'

            estimated_survival_dd = copy.deepcopy(dd)

            tumor_size = dd.get('tumor_size_in_mm')
            dd['tumor_size_in_mm'] = dd.get('tumor_size_in_mm_sd')
            dd['stage'] = dd.get('stage_sd')

            self.send_json({'diagnosis_form': dd})

            # Hormonal Therapy
            hormonal_therapy = []
            if dd.get('her2_status') == '+' or dd.get('er_status') == '+':
                hormonal_therapy.append({'name': 'Tamoxifen',
                                         'number_of_treatments': 120,
                                         'administration': 'Monthly'})

            self.send_json({'hormonal_therapy': hormonal_therapy})

            # Radiation Therapy

            radiation_therapy = []
            if sm_radiation_response[0] == 'Yes' or \
                    sl_radiation_response[0] == 'Yes' or \
                    none_radiation_response[0] == 'Yes':
                radiation_therapy.append({'name': 'Beam Radiation',
                                          'number_of_treatments': 30,
                                          'administration': 'Daily'})

            self.send_json({'radiation_therapy': radiation_therapy})

            # Chemo Therapy

            chemo_therapy = []
            if chemo_response[0] == 'Yes' and \
                    tumor_size in ['>5cm', '>3cm',
                                   '<3cm'] and \
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
                    tumor_size not in ['>5cm', '>3cm', '<3cm'] and \
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
                    tumor_size in ['>5cm', '>3cm', '<3cm'] and \
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
                    tumor_size not in ['>5cm', '>3cm', '<3cm'] and \
                    dd.get('her2_status') == '+':
                chemo_therapy.append({
                    'plan': 'C+T+HCP',
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

            self.send_json({'chemo_therapy': chemo_therapy})

            estimated_survival_dd[
                'tumor_size_in_mm'] = estimated_survival_dd.get(
                'tumor_size_in_mm_sd')

            # Estimated survival
            if estimated_survival_dd.get('tumor_size_in_mm') > 0:
                estimated_survival_data = {
                    'age': estimated_survival_dd.get('age'),
                    'stage': estimated_survival_dd.get('stage_sd'),
                    'tumor_grade': estimated_survival_dd.get('tumor_grade'),
                }
                es_response = {}

                # Preferred treatment
                es_chemo_decision_response = chemo_decisions(
                    json.dumps(estimated_survival_data, ensure_ascii=False))

                if es_chemo_decision_response:
                    for i in es_chemo_decision_response:
                        if i['datasets'][0]['label'] == 'Chemo':
                            i['chart_label'] = 'Chemotherapy'
                        elif i['datasets'][0]['label'] == 'no Chemo':
                            i['chart_label'] = 'No Chemotherapy'
                        i.get('labels', []).reverse()
                        i.get('datasets', [])[0].get('data', []).reverse()

                es_response['chemo_decision'] = {
                    'decision': es_chemo_decision_response[0],
                    'wo_decision': es_chemo_decision_response[1]
                }

                # Alternative treatment
                estimated_survival_data['chemo'] = chemo_response[0]

                es_surgery_decision_response = surgery_decisions(
                    json.dumps(estimated_survival_data, ensure_ascii=False))

                if es_surgery_decision_response:
                    for i in es_surgery_decision_response:
                        if i['datasets'][0]['label'] == 'Mastectomy':
                            i['chart_label'] = 'Mastectomy'
                        elif i['datasets'][0]['label'] == 'Lumpectomy':
                            i['chart_label'] = 'Lumpectomy'
                        i.get('labels', []).reverse()
                        i.get('datasets', [])[0].get('data', []).reverse()

                es_response[
                    'surgery_decision'] = {
                    'decision': es_surgery_decision_response[0],
                    'wo_decision': es_surgery_decision_response[1]
                }

                self.send_json({'estimated_survival': es_response})

        except Exception as e:
            self.send_json({'error': 'Failed to run command.',
                            'extra': e.__dict__})


class IndividualStatisticsConsumer(JsonWebsocketConsumer):
    serializer_class = DiagnosisDataSerializer

    def connect(self):
        # Called on connection. Either call
        if self.scope['user']:
            self.accept()
        else:
            self.close()

    def receive_json(self, content, **kwargs):
        # Remove empty strings
        content = dict((k, v) for k, v in content.items() if v)
        serializer = self.serializer_class(data=content)
        if not serializer.is_valid():
            self.send_json({'error': 'Data not valid.',
                            'extra': serializer.errors})
            self.close()

        dd = serializer.validated_data

        age = json.dumps({'age': dd.get('age')})

        mongo_client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        collection = mongo_client[DBS_NAME][COLLECTION_NAME]

        percent_women_annualy_diagnosed_response = percent_women_annualy_diagnosed(
            age, collection)
        self.send_json(
            {'percent_women_annualy_diagnosed':
                 percent_women_annualy_diagnosed_response})

        percent_women_by_type_response = percent_women_by_type(collection)
        self.send_json(
            {'percent_women_by_type': percent_women_by_type_response})

        breast_cancer_by_grade_and_size_response = {
            'grade': breast_cancer_by_grade(age, collection),
            'size': breast_cancer_by_size(age, collection)
        }
        self.send_json({
            'breast_cancer_by_grade_and_size': breast_cancer_by_grade_and_size_response})

        distribution_of_stage_of_cancer_response = {
            'overall': distribution_of_stage_of_cancer(age, collection),
            'by_race':
                distribution_of_stage_of_cancer(
                    json.dumps({'age': dd.get('age'),
                                'ethnicity': dd.get('ethnicity')},
                               ensure_ascii=False), collection),
        }
        self.send_json({
            'distribution_of_stage_of_cancer': distribution_of_stage_of_cancer_response})

        percent_of_women_with_cancer_by_race_response = {
            'overall': percent_of_women_with_cancer_by_race_overall(
                collection),
            'by_age': percent_race_with_cancer_by_age(json.dumps({
                'age': dd.get('age'),
                'sex': 'Female'
            }, ensure_ascii=False), collection)
        }
        self.send_json({'percent_of_women_with_cancer_by_race': \
                            percent_of_women_with_cancer_by_race_response})

        surgery_decisions_response = {
            'overall': ind_surgery_decisions(json.dumps({}), collection),
            'by_age': ind_surgery_decisions(age, collection)
        }
        self.send_json({'surgery_decisions': surgery_decisions_response})

        chemotherapy_response = {
            'overall': chemotherapy(collection),
            'breakout_by_stage': chemotherapy_filter(age, collection)
        }
        self.send_json({'chemotherapy': chemotherapy_response})

        radiation_response = {
            'overall': radiation(collection),
            'breakout_by_stage': radiation_filter(age, collection)
        }
        self.send_json({'radiation': radiation_response})

        breast_cancer_by_state_response = breast_cancer_by_state2(1)
        self.send_json(
            {'breast_cancer_by_state': breast_cancer_by_state_response})

        breast_cancer_at_a_glance_response = breast_cancer_at_a_glance2()
        self.send_json(
            {'breast_cancer_at_a_glance': breast_cancer_at_a_glance_response})

        breast_cancer_by_age_response = breast_cancer_by_age(collection)
        self.send_json({'breast_cancer_by_age': breast_cancer_by_age_response})


class SimilarDiagnosisConsumer(JsonWebsocketConsumer):
    serializer_class = DiagnosisDataSerializer

    def connect(self):
        # Called on connection. Either call
        if self.scope['user']:
            self.accept()
        else:
            self.close()

    def receive_json(self, content, **kwargs):
        # Remove empty strings
        content = dict((k, v) for k, v in content.items() if v)
        serializer = self.serializer_class(data=content)

        if not serializer.is_valid():
            self.send_json({'error': 'Data not valid.',
                            'extra': serializer.errors})
            self.close()

        dd = dict(serializer.validated_data)
        similar_diagnosis = []

        try:

            # START SURGERY
            simdx_args = [
                str(dd.get('age')),
                str(dd.get('number_of_tumors')),
                str(dd.get('num_pos_nodes')),
                str(float(dd.get('tumor_grade', 'unk'))),
                dd.get('type'),
                dd.get('stage'),
                dd.get('tumor_size_in_mm'),
                dd.get('er_status'),
                dd.get('pr_status'),
                dd.get('her2_status')
            ]

            similar_diagnosis = make_pred(simdx_args, 'simdx')

            for obj in similar_diagnosis:
                if obj.get('Race_group') == 'White':
                    obj['Race_group'] = 'Caucasian'
                elif obj.get('Race_group') == 'Black':
                    obj['Race_group'] = 'African American'
                elif obj.get('Race_group') == 'Asian or Pacific Islander':
                    obj['Race_group'] = 'Asian'
                elif obj.get('Race_group') == 'Unknown':
                    obj['Race_group'] = 'Other'

                if obj.get('Surgery') == 'Partial Mastectomy':
                    obj['Surgery'] = 'Lumpectomy'

                if obj.get('T_size'):
                    obj['T_size'] = '{}cm'.format(
                        round(obj.get('T_size') / 10, 1))

                if obj.get('COD to site recode') not in ['Breast', 'Alive']:
                    obj['COD to site recode'] = 'Other'

        except:
            pass

        self.send_json({'similar_diagnosis': similar_diagnosis})


class CustomAnalyticsConsumer(JsonWebsocketConsumer):
    serializer_class = CustomAnalyticsSerializer

    def connect(self):
        # Called on connection. Either call
        if self.scope['user']:
            self.accept()
        else:
            self.close()

    def receive_json(self, content, **kwargs):
        group = content.get('group', None)

        if group not in ['grade', 'stage', 'type', 'ethnicity', 'cod',
                         'radiation', 'chemo', 'surgery', 'size',
                         'tumor_number']:
            self.send_json({'error': 'Invalid group parameter'})
            self.close()

        if group == 'ethnicity':
            group = 'race'

        serializer = self.serializer_class(data=content.get('filters', {}))

        if not serializer.is_valid():
            self.send_json({'error': 'Data not valid.',
                            'extra': serializer.errors})
            self.close()

        dd = dict(serializer.validated_data)

        custom_analytics_response = custom_analytics(
            json.dumps(dd, ensure_ascii=False), group)

        try:
            data_list = custom_analytics_response.get('datasets')[0].get('data')
            if all(v == 0 for v in data_list):
                custom_analytics_response['is_data'] = False
            else:
                custom_analytics_response['is_data'] = True
        except:
            custom_analytics_response['is_data'] = False

        self.send_json({'custom_analytics': custom_analytics_response})
