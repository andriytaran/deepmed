from oauth2_provider.models import AccessToken

from accounts.models import User


class oAuth2AuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner

    def __call__(self, scope):
        try:
            token = \
                AccessToken.objects.select_related('user').get(
                    token=scope["query_string"].decode("utf-8").rsplit(
                        'token=')[1])
            if not token.is_expired():
                scope["user"] = token.user
            else:
                scope["user"] = None
        except AccessToken.DoesNotExist:
            scope["user"] = None
        return self.inner(scope)
