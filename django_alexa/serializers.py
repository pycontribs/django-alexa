from __future__ import absolute_import
import logging
from rest_framework import serializers
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
    attributes = serializers.DictField(required=False, allow_null=True)
    user = ASKUserSerializer()
    new = serializers.BooleanField()


class ASKIntentSerializer(BaseASKSerializer):
    name = serializers.CharField()
    slots = serializers.DictField(required=False, allow_null=True)


class ASKRequestSerializer(BaseASKSerializer):
    type = serializers.CharField()
    requestId = serializers.CharField()
    timestamp = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    intent = ASKIntentSerializer(required=False)
    reason = serializers.CharField(required=False)


class ASKOutputSpeechSerializer(BaseASKSerializer):
    # TODO: Choice validation to check if text or ssml is filed
    type = serializers.ChoiceField(choices=("PlainText", "SSML"))
    text = serializers.CharField(required=False)
    ssml = serializers.CharField(required=False)


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
        # TODO: handle session attributes somehow
        intent_kwargs = {}
        if validated_data["request"]["type"] == "IntentRequest":
            intent_name = validated_data["request"]["intent"]["name"]
            for slot, slot_data in validated_data["request"]["intent"].get("slots", {}).items():
                intent_kwargs[slot_data["name"]] = slot_data['value']
        else:
            intent_name = validated_data["request"]["type"]
        response = IntentsSchema.route(intent_name, intent_kwargs)
        if isinstance(response, ASKResponseSerializer) is not True:
            msg = "Intent '{0}' does not return an ASKResponseSerializer"
            raise serializers.ValidationError(detail=msg.format(intent_name))
        validated_data['response'] = response.validated_data
        return Obj(data=validated_data)
