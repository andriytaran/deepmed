from django.conf.urls import include, url
from django.contrib import admin

api_urlpatterns = [
    url('^auth/', include('auth.urls')),
    url('^accounts/', include('accounts.urls')),
    url('^diagnosis/', include('base.urls')),
]

urlpatterns = [
    url('^api/v1/', include(api_urlpatterns)),
    url('^admin/', admin.site.urls),
]
