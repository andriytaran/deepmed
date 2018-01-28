from django.conf.urls import url

from base import views as base_views

urlpatterns = [
    url(r'^$',
        base_views.ProtectedDataView.as_view(),
        name='protected_data'),
    url(r'^reports/$',
        base_views.ReportDataView.as_view(),
        name='reports'),
]
