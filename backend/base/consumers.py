from channels.generic.websocket import JsonWebsocketConsumer
from django.conf import settings

from base.serializers import DiagnosisDataSerializer


class DiagnosisConsumer(JsonWebsocketConsumer):
    serializer_class = DiagnosisDataSerializer

    def connect(self):
        # Called on connection. Either call
        if self.scope['user']:
            self.accept()
        else:
            self.close()

    def receive_json(self, content, **kwargs):
        serializer = self.serializer_class(data=content)

        if not serializer.is_valid():
            self.send_json({'error': 'Data not valid.',
                            'extra': serializer.errors})
            self.close()

        dd = serializer.validated_data

        # Recommended Treatment Plans

        response = {'overall_plans': None,
                    'hormonal_therapy': None,
                    'radiation_therapy': None,
                    'chemo_therapy': None}

        self.send_json(response)

        try:
            import subprocess
            import ast
            import re
            regex = r"\((.*?)\)"

            # START SURGERY
            surgery_args = ','.join([dd.get('sex'),
                                     str(dd.get('age')),
                                     dd.get('ethnicity'),
                                     str(float(dd.get('tumor_grade', 'unk'))),
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
                self.close()

            surgery_response = ast.literal_eval(
                re.search(regex,
                          str(surgery_output.decode('utf8'))).group())
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
                self.close()

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

            if not sm_radiation_output:
                self.send_json(
                    {'error': 'Radiation "Mastectomy" command failed'})
                self.close()

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

            if not sl_radiation_output:
                self.send_json(
                    {'error': 'Radiation "Lumpectomy" command failed'})
                self.close()

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

            response['overall_plans'] = overall_plans
            self.send_json(response)

            # Hormonal Therapy
            hormonal_therapy = []
            if dd.get('her2_status') == '+' or dd.get('er_status') == '+':
                hormonal_therapy.append({'name': 'Tamoxifen',
                                         'number_of_treatments': 120,
                                         'administration': 'Monthly'})

            response['hormonal_therapy'] = hormonal_therapy
            self.send_json(response)

            # Radiation Therapy

            radiation_therapy = []
            if is_radiation_therapy == 'Yes':
                radiation_therapy.append({'name': 'Beam Radiation',
                                          'number_of_treatments': 30,
                                          'administration': 'Daily'})

            response['radiation_therapy'] = radiation_therapy
            self.send_json(response)

            # Chemo Therapy

            chemo_therapy = []
            if chemo_response[0] == 'Yes' and \
                    dd.get('tumor_size_in_mm') in ['>5cm', '>3cm',
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
                    dd.get('tumor_size_in_mm') not in ['>5cm', '>3cm',
                                                       '<3cm'] and \
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
                    dd.get('tumor_size_in_mm') in ['>5cm', '>3cm',
                                                   '<3cm'] and \
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
                    dd.get('tumor_size_in_mm') not in ['>5cm', '>3cm',
                                                       '<3cm'] and \
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

            response['chemo_therapy'] = chemo_therapy
            self.send_json(response)

        except Exception as e:
            self.send_json({'error': 'Failed to run command.',
                            'extra': e.__dict__})

        self.close()


class IndividualStatisticsConsumer(JsonWebsocketConsumer):

    def connect(self):
        # Called on connection. Either call
        if self.scope['user']:
            self.accept()
        else:
            self.close()

    def receive_json(self, content, **kwargs):
        pass


class SimilarDiagnosisConsumer(JsonWebsocketConsumer):

    def connect(self):
        # Called on connection. Either call
        if self.scope['user']:
            self.accept()
        else:
            self.close()

    def receive_json(self, content, **kwargs):
        pass
