from __future__ import absolute_import
import logging
from string import Formatter
from .exceptions import InternalError
from .fields import AmazonField

log = logging.getLogger(__name__)


class IntentsSchema():
    intents = {}

    @classmethod
    def route(cls, name, session, data):
        """Routes an intent to the proper method"""

        if name not in cls.intents.keys():
            msg = "Unable to find an intent defined for '{0}'".format(name)
            raise InternalError(msg)
        kwargs = {}
        func, slot = cls.intents[name]
        if slot:
            if bool(data) is False:
                msg = "Intent '{0}' requires slots data and none was provided".format(name)
                raise InternalError(msg)
            else:
                slots = slot(data=data)
                slots.is_valid(raise_exception=True)
                kwargs.update(slots.data)
        kwargs['session'] = session.get('attributes', {})
        log.info("Routing: '{0}' with args {1} to '{2}.{3}'".format(name, kwargs, func.__module__, func.__name__))
        return func(**kwargs)

    @classmethod
    def register(cls, func, name, slots=None):
        if slots:
            s = slots()
            for field_name, field in s.get_fields().items():
                if issubclass(field.__class__, AmazonField) is not True:
                    msg = "'{0}' on slot '{1}' is not a valid alexa slot field type"
                    msg = msg.format(field_name, s.__class__.__name__)
                    raise InternalError(msg)
        cls.intents[name] = (func, slots)

    @classmethod
    def generate_schema(cls):
        """Generates the alexa intents schema json"""
        intents = []
        for intent_name in cls.intents.keys():
            intent_data = {"intent": intent_name,
                           "slots": []}
            _, slot = cls.intents[intent_name]
            if slot:
                s = slot()
                for field_name, field in s.get_fields().items():
                    slot_type = field.get_slot_name()
                    if slot_type is None:
                        msg = "Intent '{0}' slot '{1}' does not have a valid slot_type"
                        raise InternalError(msg.format(intent_name, field_name))
                    if slot_type == "AMAZON.LITERAL":
                        msg = "Please upgrade intent '{0}' slot '{1}' to a AmazonCustom field with choices!"
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
        utterances = []
        for intent_name in cls.intents.keys():
            func, slot = cls.intents[intent_name]
            fields = []
            if slot:
                s = slot()
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
                        msg = "Intent '{0}' utterance '{1}' has a missing the key in the slot '{2}'"
                        raise ValueError(msg.format(intent_name,
                                                    line,
                                                    s.__class__.__name__))
                utterances.append(utterance_format.format(intent_name, line.lower()))
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
        slots = kwargs.get('slots', None)
        IntentsSchema.register(func, name, slots)
        return func
    return register if invoked else register(func)
