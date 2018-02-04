import json

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from base.serializers import DiagnosisSerializer
from lib.dataset import breast_cancer_by_grade, diagnosis, \
    growth_by_specific_type, percent_race_with_cancer_by_age, \
    breakout_by_stage, woman_annualy_diagnosed, breast_cancer_by_size, \
    percent_of_women_with_cancer_by_race_overall, \
    distribution_of_stage_of_cancer, surgery_decisions, chemotherapy, radiation


class ReportDataView(GenericAPIView):
    serializer_class = DiagnosisSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)

        serializer.is_valid(raise_exception=True)
        diagnosis_data = serializer.validated_data
        input_json = json.dumps(diagnosis_data, ensure_ascii=False)
        age = json.dumps({'age': diagnosis_data.get('age')})

        data = {
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
            # 'survival_months': survival_months(input_json),
            # 'cause_of_death': {
            #     'cause_of_death_overall': cause_of_death_overall(),
            #     'by_ages': cause_of_death(input_json)
            # },
            'similar_diagnosis': diagnosis(input_json)
        }

        [o.pop('_id') for o in data['similar_diagnosis']]

        data['chemotherapy']['breakout_by_stage'] = breakout_by_stage(
            json.dumps({
                'age': diagnosis_data.get('age'),
                'chemo': 'Yes',
                "breast-adjusted-ajcc-6th-stage-1988": {
                    "$in": ["I", "IIA", "IIB", "IIIA",
                            "IIIB", "IIIC", "IIINOS", "IV",
                            0]
                }}, ensure_ascii=False))

        data['radiation']['breakout_by_stage'] = breakout_by_stage(json.dumps({
            'age': diagnosis_data.get('age'),
            'radiation': 'Yes',
            "breast-adjusted-ajcc-6th-stage-1988": {
                "$in": ["I", "IIA", "IIB", "IIIA",
                        "IIIB", "IIIC", "IIINOS", "IV",
                        0]
            }}, ensure_ascii=False))

        data['percent_of_women_with_cancer_by_race'][
            'by_age'] = percent_race_with_cancer_by_age(json.dumps({
            'age': diagnosis_data.get('age'),
            'sex': 'Female'
        }, ensure_ascii=False))

        return Response(data, status=status.HTTP_200_OK)
