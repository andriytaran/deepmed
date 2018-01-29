import os
from time import sleep

from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View
from knox.auth import TokenAuthentication
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from serializers import DiagnosisSerializer

from lib.dataset import breast_cancer_at_a_glance, breast_cancer_by_age, breast_cancer_by_state, breast_cancer_by_grade


class IndexView(View):
    """Render main page."""

    def get(self, request):
        """Return html for main application page."""

        abspath = open(os.path.join(settings.BASE_DIR, 'static/index.html'), 'r')
        return HttpResponse(content=abspath.read())


class ProtectedDataView(GenericAPIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        data = {
            'data': 'THIS IS THE PROTECTED STRING FROM SERVER',
        }
        sleep(10)

        return Response(data, status=status.HTTP_200_OK)


class ReportDataView(GenericAPIView):

    serializer_class = DiagnosisSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            age = serializer.validated_data['age']
            race = serializer.validated_data['race']

            data = {
                # 'breast_cancer_by_state': breast_cancer_by_state(),
                'breast_cancer_at_a_glance': breast_cancer_at_a_glance(),
                'breast_cancer_by_age': breast_cancer_by_age(),
                'breast_cancer_by_grade': breast_cancer_by_grade(age)
            }

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_200_OK)
