from django.urls import path, include
from rest_framework.routers import DefaultRouter

import accounts.views

user_router = DefaultRouter(trailing_slash=True)
user_router.register('user', accounts.views.UsersViewSet,
                     base_name='users')

urlpatterns = [
    path('', include(user_router.urls)),
]
