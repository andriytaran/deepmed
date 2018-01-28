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

from lib.dataset import breast_cancer_at_a_glance, breast_cancer_by_age


class IndexView(View):
    """Render main page."""

    def get(self, request):
        """Return html for main application page."""

        abspath = open(os.path.join(settings.BASE_DIR, 'static_dist/index.html'), 'r')
        return HttpResponse(content=abspath.read())


class ProtectedDataView(GenericAPIView):
    """Return protected data main page."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Process GET request and return protected data."""

        data = {
            'data': 'THIS IS THE PROTECTED STRING FROM SERVER',
        }
        sleep(10)

        return Response(data, status=status.HTTP_200_OK)


class ReportDataView(GenericAPIView):
    """Return protected data main page."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Process GET request and return protected data."""

        data = {
            'breast_cancer_by_state': {
                'regions': [{
                    'scale': ['#47cfd1', '#48ccf5', '#88d0d1', '#b8e8f5'],
                    'attribute': 'fill',
                    'values': {
                        "US-AL": 0,
                        "US-AK": 1,
                        "US-AZ": 3,
                        "US-AR": 3,
                        "US-CA": 0,
                        "US-CO": 0,
                        "US-CT": 0,
                        "US-DE": 0,
                        "US-DC": 0,
                        "US-FL": 3,
                        "US-GA": 0,
                        "US-HI": 2,
                        "US-ID": 0,
                        "US-IL": 2,
                        "US-IN": 0,
                        "US-IA": 1,
                        "US-KS": 0,
                        "US-KY": 1,
                        "US-LA": 0,
                        "US-ME": 1,
                        "US-MD": 0,
                        "US-MA": 2,
                        "US-MI": 3,
                        "US-MN": 1,
                        "US-MS": 3,
                        "US-MO": 1,
                        "US-MT": 1,
                        "US-NE": 0,
                        "US-NV": 3,
                        "US-NH": 0,
                        "US-NJ": 0,
                        "US-NM": 3,
                        "US-NY": 2,
                        "US-NC": 1,
                        "US-ND": 3,
                        "US-OH": 1,
                        "US-OK": 0,
                        "US-OR": 3,
                        "US-PA": 1,
                        "US-RI": 0,
                        "US-SC": 0,
                        "US-SD": 0,
                        "US-TN": 3,
                        "US-TX": 3,
                        "US-UT": 3,
                        "US-VT": 0,
                        "US-VA": 1,
                        "US-WA": 2,
                        "US-WV": 0,
                        "US-WI": 1,
                        "US-WY": 0
                    }
                }]
            },
            'breast_cancer_at_a_glance': breast_cancer_at_a_glance(),
            'breast_cancer_by_age': breast_cancer_by_age()
        }

        return Response(data, status=status.HTTP_200_OK)
