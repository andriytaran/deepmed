from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

import accounts.views

user_router = DefaultRouter()
user_router.register('user', accounts.views.UsersViewSet,
                     base_name='users')

urlpatterns = [
    url(r'^', include(user_router.urls)),
]
