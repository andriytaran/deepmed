from django.conf.urls import include, url
from django.contrib import admin

api_urlpatterns = [
    url('auth/', include('auth.urls')),
    url('accounts/', include('accounts.urls', namespace='accounts')),
    url('diagnosis/', include('base.urls', namespace='base')),
]

urlpatterns = [
    url('api/v1/', include(api_urlpatterns)),
    url('admin/', admin.site.urls),
]
