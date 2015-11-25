from django.utils.module_loading import autodiscover_modules


default_app_config = 'django_alexa.apps.AlexaAppConfig'


def autodiscover():
    autodiscover_modules('alexa')
