from django.shortcuts import get_object_or_404
from rest_framework import status, mixins, permissions
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

import accounts.models
import accounts.serializers
from common.drf.mixins import ActionPermissionClassesMixin
from common.drf.permissions import NotAuthenticated


class UsersViewSet(ActionPermissionClassesMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   GenericViewSet):
    model = accounts.models.User
    serializer_class = accounts.serializers.UserSerializer
    action_permission_classes = {
        'create': [NotAuthenticated],
        'retrieve': [permissions.IsAuthenticated],
        'update': [permissions.IsAuthenticated],
        'partial_update': [permissions.IsAuthenticated],
        'confirm_email': [permissions.AllowAny],
        'email_status': [permissions.AllowAny],
    }

    def get_queryset(self):
        return self.model.objects.all()

    def get_serializer_class(self):
        return super(UsersViewSet, self).get_serializer_class()

    @list_route(methods='GET', url_path='confirm-email')
    def confirm_email(self, request, *args, **kwargs):
        """
        View for confirm email.

        Receive an activation key as parameter and confirm email.
        """
        user = get_object_or_404(accounts.models.User,
                                 activation_key=str(request.query_params
                                                    .get('activation_key')))
        if user.confirm_email():
            return Response(status=status.HTTP_200_OK)

        log.warning(message='Email confirmation key not found.',
                    details={'http_status_code': status.HTTP_404_NOT_FOUND})
        return Response(status=status.HTTP_404_NOT_FOUND)

    @list_route(methods='GET', url_path='email-status')
    def email_status(self, request, *args, **kwargs):
        """Retrieve user current confirmed_email status."""
        user = self.request.user
        return Response({'status': user.confirmed_email},
                        status=status.HTTP_200_OK)
