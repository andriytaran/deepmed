from django.urls import path

from base import views as base_views

urlpatterns = [
    path('us-statistics/',
         base_views.USStatisticsView.as_view(),
         name='us-statistics'),
    path('resources/',
         base_views.ResourcesView.as_view(),
         name='resources'),
]
