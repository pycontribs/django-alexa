'''This maps DRF serializer fields to ASK fields'''
import six
from rest_framework import serializers
from django_alexa.internal import fields


class AmazonSlots(fields.AmazonSlots, serializers.Serializer):
    pass


class AmazonCustom(fields.AmazonCustom, serializers.ChoiceField):

    def get_slot_name(self):
        return self.label

    def get_choices(self):
        return [six.text_type(key) for key in self.choices.keys()]


class AmazonLiteral(fields.AmazonLiteral, serializers.CharField):
    pass


class AmazonNumber(fields.AmazonNumber, serializers.IntegerField):
    pass


class AmazonDate(fields.AmazonDate, serializers.DateField):
    pass


class AmazonTime(fields.AmazonTime, serializers.TimeField):
    pass


class AmazonDuration(fields.AmazonDuration, serializers.DurationField):
    pass


class AmazonUSCity(fields.AmazonUSCity, serializers.CharField):
    pass


class AmazonFirstName(fields.AmazonFirstName, serializers.CharField):
    pass


class AmazonUSState(fields.AmazonUSState, serializers.CharField):
    pass


class AmazonFourDigitNumber(fields.AmazonFourDigitNumber, serializers.IntegerField):
    pass
