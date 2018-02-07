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
    radiation, get_t_size_cm, breast_cancer_by_state, \
    breast_cancer_at_a_glance, breast_cancer_by_age, \
    percent_women_annualy_diagnosed, percent_women_by_type


class ReportDataView(GenericAPIView):
    serializer_class = DiagnosisSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)

        serializer.is_valid(raise_exception=True)
        dd = dict(serializer.validated_data)

        age = json.dumps({'age': dd.get('age')})

        try:
            import subprocess
            import ast
            import re
            regex = r"\((.*?)\)"

            if dd.get('ethnicity') == 'Caucasian':
                v_ethnicity = 'White'
            elif dd.get('ethnicity') == 'Other':
                v_ethnicity = 'Unknown'
            else:
                v_ethnicity = dd.get('ethnicity')

            # START SURGERY
            surgery_args = ','.join([dd.get('sex'),
                                     str(dd.get('age')),
                                     v_ethnicity,
                                     str(float(dd.get('tumor_grade', 'unk'))),
                                     dd.get('site'),
                                     dd.get('type'),
                                     dd.get('stage'),
                                     dd.get('region'),
                                     get_t_size_cm(
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
                get_t_size_cm(dd.get('tumor_size_in_mm')),
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
                get_t_size_cm(dd.get('tumor_size_in_mm')),
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

            percent = round(surgery_response[1] * 100)
            if surgery_response[0] == 'Mastectomy':
                overall_plans.append({
                    'name': 'Preferred Outcome A',
                    'type': surgery_response[0],
                    'radiation': 'Y' if sm_radiation_response[
                                            0] == 'Yes' else 'N',
                    'chemo': 'Y' if chemo_response[0] == 'Yes' else 'N',
                    'surgery': 'Y',
                    'level': percent})
                overall_plans.append({
                    'name': 'Preferred Outcome B',
                    'type': 'Lumpectomy',
                    'radiation': 'Y' if sl_radiation_response[
                                            0] == 'Yes' else 'N',
                    'chemo': 'Y' if chemo_response[0] == 'Yes' else 'N',
                    'surgery': 'Y',
                    'level': 100 - percent})
            else:
                overall_plans.append({
                    'name': 'Preferred Outcome A',
                    'type': 'Lumpectomy',
                    'radiation': 'Y' if sl_radiation_response[
                                            0] == 'Yes' else 'N',
                    'chemo': 'Y' if chemo_response[0] == 'Yes' else 'N',
                    'surgery': 'Y',
                    'level': percent})
                overall_plans.append({
                    'name': 'Preferred Outcome B',
                    'type': surgery_response[0],
                    'radiation': 'Y' if sm_radiation_response[
                                            0] == 'Yes' else 'N',
                    'chemo': 'Y' if chemo_response[0] == 'Yes' else 'N',
                    'surgery': 'Y',
                    'level': 100 - percent})
        except Exception as e:
            overall_plans = []

        data = {
            'recommended_treatment_plans': {
                'overall_plans': overall_plans
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
                                    'ethnicity': dd.get(
                                        'ethnicity')}, ensure_ascii=False)),
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


class TestDataView(GenericAPIView):
    serializer_class = DiagnosisSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)

        serializer.is_valid(raise_exception=True)
        dd = dict(serializer.validated_data)

        age = json.dumps({'age': dd.get('age')})

        try:
            import subprocess
            import ast
            import re
            regex = r"\((.*?)\)"

            if dd.get('ethnicity') == 'Caucasian':
                v_ethnicity = 'White'
            elif dd.get('ethnicity') == 'Other':
                v_ethnicity = 'Unknown'
            else:
                v_ethnicity = dd.get('ethnicity')

            # START SURGERY
            surgery_args = ','.join([dd.get('sex'),
                                     str(dd.get('age')),
                                     v_ethnicity,
                                     str(float(dd.get('tumor_grade'))),
                                     dd.get('site'),
                                     dd.get('type'),
                                     dd.get('stage'),
                                     dd.get('region'),
                                     get_t_size_cm(
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

            chemo_args = ' '.join([
                str(dd.get('age')),
                v_ethnicity,
                str(float(dd.get('tumor_grade'))),
                dd.get('type'),
                dd.get('stage'),
                dd.get('region'),
                get_t_size_cm(dd.get('tumor_size_in_mm')),
                str(dd.get('num_pos_nodes')),
                str(dd.get('num_pos_nodes')),
                str(dd.get('er_status')),
                str(dd.get('pr_status')),
                str(dd.get('her2_status')),
                str('unk')])  # AJCC_2010p

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
                get_t_size_cm(dd.get('tumor_size_in_mm')),
                str(dd.get('number_of_tumors')),
                str(dd.get('num_pos_nodes')),
                str(dd.get('num_pos_nodes')),  # cs_lymphnodes
                str(dd.get('er_status')),
                str(dd.get('pr_status')),
                str(dd.get('her2_status'))]

            sm_radiation_args = copy.deepcopy(
                radiation_args)  # Copy base list of args

            sm_radiation_args.append('Mastectomy')
            sm_radiation_args.append(chemo_response[0])
            sm_radiation_args.append(str('unk'))  # AJCC_2010p

            sm_radiation_command_str = [settings.ML_PYTHON_PATH,
                                        settings.ML_COMMAND_FILE,
                                        ' '.join(sm_radiation_args),
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
            sl_radiation_args.append(str('unk'))  # AJCC_2010p

            sl_radiation_command_str = [settings.ML_PYTHON_PATH,
                                        settings.ML_COMMAND_FILE,
                                        ' '.join(sm_radiation_args),
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

            percent = round(surgery_response[1] * 100)
            if surgery_response[0] == 'Mastectomy':
                overall_plans.append({
                    'name': 'Preferred Outcome A',
                    'type': surgery_response[0],
                    'radiation': 'Y' if sm_radiation_response[
                                            0] == 'Yes' else 'N',
                    'chemo': 'Y' if chemo_response[0] == 'Yes' else 'N',
                    'surgery': 'Y',
                    'level': percent})
                overall_plans.append({
                    'name': 'Preferred Outcome B',
                    'type': 'Lumpectomy',
                    'radiation': 'Y' if sl_radiation_response[
                                            0] == 'Yes' else 'N',
                    'chemo': 'Y' if chemo_response[0] == 'Yes' else 'N',
                    'surgery': 'Y',
                    'level': 100 - percent})
            else:
                overall_plans.append({
                    'name': 'Preferred Outcome A',
                    'type': 'Lumpectomy',
                    'radiation': 'Y' if sl_radiation_response[
                                            0] == 'Yes' else 'N',
                    'chemo': 'Y' if chemo_response[0] == 'Yes' else 'N',
                    'surgery': 'Y',
                    'level': percent})
                overall_plans.append({
                    'name': 'Preferred Outcome B',
                    'type': surgery_response[0],
                    'radiation': 'Y' if sm_radiation_response[
                                            0] == 'Yes' else 'N',
                    'chemo': 'Y' if chemo_response[0] == 'Yes' else 'N',
                    'surgery': 'Y',
                    'level': 100 - percent})
        except Exception as e:
            overall_plans = []

        data = {
            'recommended_treatment_plans': {
                'overall_plans': overall_plans
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
                                    'ethnicity': dd.get(
                                        'ethnicity')}, ensure_ascii=False)),
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
