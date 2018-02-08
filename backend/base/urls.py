from django.conf.urls import url

from base import views as base_views

urlpatterns = [
    url(r'^reports/$',
        base_views.ReportDataView.as_view(),
        name='reports'),
    url(r'^chart/$',
        base_views.ChartOneView.as_view(),
        name='chart'),
    url(r'^test/$',
        base_views.TestDataView.as_view(),
        name='tests'),
]
