from __future__ import absolute_import
import logging
import warnings
from string import Formatter
from rest_framework import serializers

log = logging.getLogger(__name__)

# This maps DRF serializer fields to the amazon intent slot types
INTENT_SLOT_TYPES = {
    "CharField": "AMAZON.LITERAL",
    "IntegerField": "AMAZON.NUMBER",
    "DateField": "AMAZON.DATE",
    "TimeField": "AMAZON.TIME",
    "DurationField": "AMAZON.DURATION",
}

# These are the valid intent slot types
# We add choicefield here because it represents custom slot types but has to
# have a custom name mapping for the slot type which based on the field label
VALID_SLOT_TYPES = INTENT_SLOT_TYPES.keys() + [
    "ChoiceField"
]

# These utterances can have utterance overrides but need a prefix of "AMAZON."
UTTERANCES_OVERRIDE_INTENTS = [
    'HelpIntent',
    'CancelIntent',
    'StopIntent'
]

class IntentsSchema():
    intents = {}

    @classmethod
    def route(cls, name, data=None):
        """Routes an intent to the proper method"""
        if name not in cls.intents.keys():
            msg = "Unable to find an intent defined for '{0}'"
            raise serializers.ValidationError(detail=msg.format(name))
        kwargs = {}
        func, serializer = cls.intents[name]
        if serializer:
            if data is None:
                msg = "Intent '{0}' requires slots data and none was provided"
                raise serializers.ValidationError(detail=msg.format(name))
            else:
                slots = serializer(data=data)
                slots.is_valid(raise_exception=True)
                kwargs.update(slots.data)
        return func(**kwargs)

    @classmethod
    def register(cls, func, name, serializer=None):
        if serializer:
            s = serializer()
            for field_name, field in s.get_fields().items():
                if field.__class__.__name__ not in VALID_SLOT_TYPES:
                    msg = "'{0}' on serializer '{1}' is not a valid alexa slot type"
                    raise ValueError(msg.format(field_name,
                                                s.__class__.__name__))
        cls.intents[name] = (func, serializer)

    @classmethod
    def generate_schema(cls):
        """Generates the alexa intents schema json"""
        intents =[]
        for intent_name in cls.intents.keys():
            intent_data = {"intent": intent_name,
                           "slots": []}
            _, serializer = cls.intents[intent_name]
            if serializer:
                s = serializer()
                for field_name, field in s.get_fields().items():
                    slot_type = INTENT_SLOT_TYPES.get(field.__class__.__name__,
                                                 field.label)
                    if slot_type is None:
                        msg = "Intent '{0}' slot '{1}' does not have a valid slot_type"
                        raise ValueError(msg.format(intent_name, field_name))
                    if slot_type == "AMAZON.LITERAL":
                        msg = "Please upgrade intent '{0}' slot '{1}' to a ChoiceField with choices!"
                        log.warning(msg.format(intent_name, field_name))
                    slot_data = {
                        "name": field_name,
                        "type": slot_type
                    }
                    intent_data['slots'].append(slot_data)
            intents.append(intent_data)
        return {"intents": intents}

    @classmethod
    def generate_utterances(cls):
        """Generates the alexa utterances schema for all intents"""
        utterance_format = "{0} {1}"
        utterances =[]
        for intent_name in cls.intents.keys():
            func, serializer = cls.intents[intent_name]
            fields = []
            if serializer:
                s = serializer()
                fields = s.get_fields().keys()
            docstring = """"""
            if func.__doc__:
                if "---\n" in func.__doc__:
                    docstring = func.__doc__.split("---")[-1].strip()
            for line in docstring.splitlines():
                line = line.strip()
                for key in [i[1] for i in Formatter().parse(line) if i[1]]:
                    if "|" in key:
                        key = key.split("|")[-1]
                    if key not in fields:
                        msg = "Intent '{0}' utterance '{1}' has a missing the key in the serializer '{2}'"
                        raise ValueError(msg.format(intent_name,
                                                    line,
                                                    s.__class__.__name__))
                if intent_name in UTTERANCES_OVERRIDE_INTENTS:
                    intent_name = "AMAZON.{0}".format(intent_name)
                utterances.append(utterance_format.format(intent_name, line))
        return utterances


def intent(*args, **kwargs):
    """
    Decorator that registers a function to the IntentsSchema
    """
    invoked = bool(not args or kwargs)
    if not invoked:
        func, args = args[0], ()

    def register(func):
        name = kwargs.get('name', func.__name__)
        serializer = kwargs.get('serializer', None)
        IntentsSchema.register(func, name, serializer)
        return func
    return register if invoked else register(func)
