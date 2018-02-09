from django.urls import path

from auth import views

urlpatterns = [
    path(r'token/', views.token, name="token"),
    path(r'revoke_token/', views.revoke_token, name="revoke-token"),
]
