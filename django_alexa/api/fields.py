'''These are the only serializer fields support by the Alexa skills kit'''
from rest_framework.serializers import CharField, IntegerField, DateField, TimeField, DurationField, ChoiceField # flake8: noqa

# This maps serializer fields to the amazon intent slot types
INTENT_SLOT_TYPES = {
    "CharField": "AMAZON.LITERAL",
    "IntegerField": "AMAZON.NUMBER",
    "DateField": "AMAZON.DATE",
    "TimeField": "AMAZON.TIME",
    "DurationField": "AMAZON.DURATION",
    "USCityField": "AMAZON.US_CITY",
    "FirstNameField": "AMAZON.US_FIRST_NAME",
    "USStateField": "AMAZON.US_STATE",
    "FourDigitField": "AMAZON.FOUR_DIGIT_NUMBER",
}

# Choicefield does not have a amazon mapping because it represents
# a custom slot type which has but has to have a defined choice set in the
# alexa skills kit interaction model
VALID_SLOT_TYPES = INTENT_SLOT_TYPES.keys() + [
    "ChoiceField"
]


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
