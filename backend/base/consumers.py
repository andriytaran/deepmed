from channels.generic.websocket import JsonWebsocketConsumer


class DiagnosisConsumer(JsonWebsocketConsumer):

    def connect(self):
        # Called on connection. Either call
        if self.scope['user']:
            self.accept()
        else:
            self.close()

    def receive_json(self, content, **kwargs):
        """
        Called with decoded JSON content.
        """
        pass

