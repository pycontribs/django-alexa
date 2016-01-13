'''These are the only serializer fields support by the Alexa skills kit'''
from rest_framework.serializers import CharField, IntegerField, DateField, TimeField, DurationField, ChoiceField # flake8: noqa


class USCityField(CharField):

    def __init__(self, **kwargs):
        super(USCityField, self).__init__(**kwargs)

class FirstNameField(CharField):

    def __init__(self, **kwargs):
        super(FirstNameField, self).__init__(**kwargs)

class USStateField(CharField):

    def __init__(self, **kwargs):
        super(USStateField, self).__init__(**kwargs)

class FourDigitField(IntegerField):

    def __init__(self, **kwargs):
        super(FourDigitField, self).__init__(**kwargs)
