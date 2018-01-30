from django.conf.urls import url

from auth import views

urlpatterns = [
    url(r'token', views.token, name="token"),
    url(r'revoke_token', views.revoke_token, name="revoke-token"),
]
