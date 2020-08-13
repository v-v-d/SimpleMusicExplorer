from django.apps import AppConfig


class musicappConfig(AppConfig):
    name = 'musicapp'

    def ready(self):
        import musicapp.signals
