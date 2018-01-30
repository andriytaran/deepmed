from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        pass