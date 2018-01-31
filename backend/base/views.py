import json

from django.conf import settings
from pymongo import MongoClient
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from base.serializers import DiagnosisSerializer
from dataset import woman_age_30_40_annualy_diagnosed, \
    er_pos_pr_neg_her2_neg_annual_diagnoses, breast_cancer_by_size_age_30_40, \
    distribution_of_stage_of_cancer_for_ages_30_40, \
    percent_of_women_with_cancer_by_race, surgery_decisions_within_ages_30_40, \
    chemotherapy_for_ages_30_40, radiation_for_ages_30_40, \
    survival_months_within_ages_30_40, cause_of_death_overall, \
    cause_of_death_within_ages_30_40

from lib.dataset import breast_cancer_by_grade, diagnosis, surgery_decisions


class ReportDataView(GenericAPIView):
    serializer_class = DiagnosisSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            diagnosis_data = serializer.validated_data

            data = {
                'woman_age_30_40_annualy_diagnosed': woman_age_30_40_annualy_diagnosed(),
                'er_pos_pr_neg_her2_neg_annual_diagnoses': er_pos_pr_neg_her2_neg_annual_diagnoses(),
                'breast_cancer_by_grade_and_size_age_30_40': {
                    'grade': breast_cancer_by_grade(diagnosis_data.get('age')),
                    'size': breast_cancer_by_size_age_30_40()
                },
                'distribution_of_stage_of_cancer_for_ages_30_40': distribution_of_stage_of_cancer_for_ages_30_40(),
                'percent_of_women_with_cancer_by_race': percent_of_women_with_cancer_by_race(),
                'surgery_decisions_within_ages_30_40': surgery_decisions_within_ages_30_40(),
                'chemotherapy_for_ages_30_40': chemotherapy_for_ages_30_40(),
                'radiation_for_ages_30_40': radiation_for_ages_30_40(),
                'survival_months_within_ages_30_40': survival_months_within_ages_30_40(),
                'cause_of_death': {
                    'cause_of_death_overall': cause_of_death_overall(),
                    'cause_of_death_within_ages_30_40': cause_of_death_within_ages_30_40()
                },
                'surgery_decisions': surgery_decisions(
                    json.dumps({'age': diagnosis_data.get('age')},
                               ensure_ascii=False)),
                'diagnosis': diagnosis(
                    json.dumps(diagnosis_data.validated_data,
                               ensure_ascii=False))
            }
            [o.pop('_id') for o in data['similar_diagnosis']]

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_200_OK)
