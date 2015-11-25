from django.apps import AppConfig


class AlexaAppConfig(AppConfig):
    name = "django_alexa"

    def ready(self):
        super(AlexaAppConfig, self).ready()
        self.module.autodiscover()
