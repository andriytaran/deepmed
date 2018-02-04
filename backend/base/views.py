import json

from django.conf import settings
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from base.serializers import DiagnosisSerializer
from lib.dataset import breast_cancer_by_grade, diagnosis, \
    growth_by_specific_type, percent_race_with_cancer_by_age, \
    breakout_by_stage, woman_annualy_diagnosed, breast_cancer_by_size, \
    percent_of_women_with_cancer_by_race_overall, \
    distribution_of_stage_of_cancer, surgery_decisions, chemotherapy, \
    radiation, get_t_size_cm


class ReportDataView(GenericAPIView):
    serializer_class = DiagnosisSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)

        serializer.is_valid(raise_exception=True)
        dd = serializer.validated_data
        input_json = json.dumps(dd, ensure_ascii=False)
        age = json.dumps({'age': dd.get('age')})

        overall_plans = [{'type': 'Mastectomy',
                                  'radiation': 'n',
                                  'chemo': 'y',
                                  'surgery': 'y',
                                  'level': 97},
                         {'type': 'Lumpectomy',
                          'radiation': 'y',
                          'chemo': 'y',
                          'surgery': 'y',
                          'level': 3}
                         ]

        data = {
            'recommended_treatment_plans': {
                'overall_plans': overall_plans
            },
            'woman_annualy_diagnosed': woman_annualy_diagnosed(age),
            'growth_by_specific_type': growth_by_specific_type(
                '{"type": "Other", "type": "Mixed",'
                ' "type": "IBC", "type": "Mixed "}',
                operator="$or"),
            'breast_cancer_by_grade_and_size': {
                'grade': breast_cancer_by_grade(age),
                'size': breast_cancer_by_size(age)
            },
            'distribution_of_stage_of_cancer': distribution_of_stage_of_cancer(
                age),
            'distribution_of_stage_of_cancer_by_ethnicity':
                distribution_of_stage_of_cancer(
                    json.dumps({'age': dd.get('age'),
                                'ethnicity': dd.get(
                                    'ethnicity')}, ensure_ascii=False)),
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
            'similar_diagnosis': diagnosis(input_json)
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

        return Response(data, status=status.HTTP_200_OK)


class TestDataView(GenericAPIView):
    serializer_class = DiagnosisSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)

        serializer.is_valid(raise_exception=True)
        dd = serializer.validated_data
        input_json = json.dumps(dd, ensure_ascii=False)
        age = json.dumps({'age': dd.get('age')})

        str_args = ' '.join([dd.get('sex', 'Female'),
                             str(dd.get('age', 43)),
                             dd.get('ethnicity', 'White'),
                             str(float(dd.get('tumor_grade', 1))),
                             dd.get('site', 'Center'), dd.get('type', 'IDC'),
                             dd.get('stage', str('II')),
                             dd.get('n_stage', 'Localized'),
                             get_t_size_cm(dd.get('tumor_size_in_mm', 22)),
                             str(dd.get('Total_insitu_mali_tumors', 12)),
                             str(dd.get('num_pos_nodes', 10))])

        command = [settings.ML_PYTHON_PATH,
                   settings.ML_SURGERY_FILE,
                   str_args, 'Surgery']

        import subprocess
        import ast

        surgery_command = subprocess.Popen(command, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
        output, err = surgery_command.communicate()
        sc_response = ast.literal_eval(str(output.decode('utf8')))

        overall_plans = []
        percent = round(sc_response[1] * 100)
        if sc_response[0] == 'Mastectomy':
            overall_plans.append({'type': sc_response[0],
                                  'radiation': 'n',
                                  'chemo': 'y',
                                  'surgery': 'y',
                                  'level': percent})
            overall_plans.append({'type': 'Lumpectomy',
                                  'radiation': 'y',
                                  'chemo': 'y',
                                  'surgery': 'y',
                                  'level': 100 - percent})
        else:
            overall_plans.append({'type': sc_response[0],
                                  'radiation': 'y',
                                  'chemo': 'y',
                                  'surgery': 'y',
                                  'level': percent})
            overall_plans.append({'type': 'Mastectomy',
                                  'radiation': 'n',
                                  'chemo': 'y',
                                  'surgery': 'y',
                                  'level': 100 - percent})

        data = {
            'recommended_treatment_plans': {
                'overall_plans': overall_plans
            },
            'woman_annualy_diagnosed': woman_annualy_diagnosed(age),
            'growth_by_specific_type': growth_by_specific_type(
                '{"type": "Other", "type": "Mixed",'
                ' "type": "IBC", "type": "Mixed "}',
                operator="$or"),
            'breast_cancer_by_grade_and_size': {
                'grade': breast_cancer_by_grade(age),
                'size': breast_cancer_by_size(age)
            },
            'distribution_of_stage_of_cancer': distribution_of_stage_of_cancer(
                age),
            'distribution_of_stage_of_cancer_by_ethnicity':
                distribution_of_stage_of_cancer(
                    json.dumps({'age': dd.get('age'),
                                'ethnicity': dd.get(
                                    'ethnicity')}, ensure_ascii=False)),
            'percent_of_women_with_cancer_by_race': {
                'overall': percent_of_women_with_cancer_by_race_overall()
            },
            'surgery_decisions': surgery_decisions(age),
            'chemotherapy': {
                'overall': chemotherapy(age),  # ????
            },
            'radiation': {
                'overall': radiation(age),  # ????
            },
            'similar_diagnosis': diagnosis(input_json)
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

        return Response(data, status=status.HTTP_200_OK)
