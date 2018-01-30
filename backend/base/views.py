from pprint import pprint

from django.conf import settings
from pymongo import MongoClient
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from base.serializers import DiagnosisSerializer
from lib.dataset import breast_cancer_at_a_glance, breast_cancer_by_age, \
    breast_cancer_by_grade


class ProtectedDataView(GenericAPIView):
    serializer_class = DiagnosisSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            diagnosis = serializer.validated_data

            mongo_client = MongoClient(settings.MONGODB_HOST,
                                       settings.MONGODB_PORT)
            collection = mongo_client[settings.DBS_NAME][
                settings.COLLECTION_NAME]

            collection.insert_one(diagnosis)

            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ReportDataView(GenericAPIView):
    serializer_class = DiagnosisSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            diagnosis = serializer.validated_data
            pprint(diagnosis)

            data = {
                # 'breast_cancer_by_state': breast_cancer_by_state(),
                'breast_cancer_at_a_glance': breast_cancer_at_a_glance(),
                'breast_cancer_by_age': breast_cancer_by_age(),
                'breast_cancer_by_grade': breast_cancer_by_grade(
                    diagnosis['age'])
            }

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_200_OK)
