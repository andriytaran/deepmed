from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from base.consumers import DiagnosisConsumer, IndividualStatisticsConsumer, \
    SimilarDiagnosisConsumer
from common.drf.channels_auth_middleware import oAuth2AuthMiddleware

application = ProtocolTypeRouter({

    "websocket": oAuth2AuthMiddleware(URLRouter([
        path("api/diagnosis", DiagnosisConsumer),
        path("api/individual-stats", IndividualStatisticsConsumer),
        path("api/similar-diagnosis", SimilarDiagnosisConsumer),
    ])),

})