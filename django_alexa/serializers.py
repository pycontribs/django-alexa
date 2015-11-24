from __future__ import absolute_import
import logging
from rest_framework import serializers
from django.conf import settings
from .api import validation, IntentsSchema

log = logging.getLogger(__name__)


class Obj(object):
    def __init__(self, data):
        self.__dict__.update(data)


class BaseASKSerializer(serializers.Serializer):
    
    def create(self, validated_data):
        return Obj(data=validated_data)


class ASKApplicationSerializer(BaseASKSerializer):
    applicationId = serializers.CharField(validators=[validation.validate_app_ids])


class ASKUserSerializer(BaseASKSerializer):
    userId = serializers.CharField()


class ASKSessionSerializer(BaseASKSerializer):
    sessionId = serializers.CharField()
    application = ASKApplicationSerializer()
    attributes = serializers.DictField(required=False)
    user = ASKUserSerializer()
    new = serializers.BooleanField()


class ASKIntentSerializer(BaseASKSerializer):
    name = serializers.CharField()
    slots = serializers.DictField()


class ASKRequestSerializer(BaseASKSerializer):
    type = serializers.CharField()
    requestId = serializers.CharField()
    timestamp = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    intent = ASKIntentSerializer(required=False)
    reason = serializers.CharField(required=False)


class ASKOutputSpeechSerializer(BaseASKSerializer):
    type = serializers.ChoiceField(choices=("PlainText", "SSML"))
    text = serializers.CharField() # TODO Choice validation to check if text or ssml is filed
    ssml = serializers.CharField()


class ASKCardSerializer(BaseASKSerializer):
    type = serializers.ChoiceField(choices=("Simple", "LinkAccount"))
    title = serializers.CharField(required=False)
    content = serializers.CharField(required=False)


class ASKRempromptSerializer(BaseASKSerializer):
    outputSpeech = ASKOutputSpeechSerializer(required=False)


class ASKResponseSerializer(BaseASKSerializer):
    outputSpeech = ASKOutputSpeechSerializer(required=False, validators=[validation.validate_char_limit])
    card = ASKCardSerializer(required=False, validators=[validation.validate_char_limit])
    reprompt = ASKRempromptSerializer(required=False)
    shouldEndSession = serializers.BooleanField()


class ASKSerializer(BaseASKSerializer):
    version = serializers.FloatField(required=True)
    
    session = ASKSessionSerializer(write_only=True)
    request = ASKRequestSerializer(write_only=True)
    
    sessionAttributes = serializers.DictField(required=False, read_only=True)
    response = ASKResponseSerializer(read_only=True)
    
    def create(self, validated_data):
        intent_name = validated_data["request"]["intent"]["name"]
        intent_kwargs = {}
        for slot, slot_data in validated_data["request"]["intent"]["slots"].items():
            intent_kwargs[slot_data["name"]] = slot_data['value']
        log.info("Routing: {0} - {1}".format(intent, intent_kwargs))
        response = IntentsSchema.route(intent_name, intent_kwargs)
        if isinstance(response, ASKResponseSerializer) is not True:
            msg = "Intent '{0}' does not return an ASKResponseSerializer"
            raise serializers.ValidationError(detail=msg.format(intent_name))
        validated_data['response'] = response
        # TODO: handle session attributes somehow
        return Obj(data=validated_data)


