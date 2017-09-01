from django.apps import AppConfig


class SevchefsApiConfig(AppConfig):
    name = 'sevchefs_api'

    def ready(self):
        import sevchefs_api.signals
