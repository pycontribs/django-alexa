from __future__ import absolute_import
import logging
from string import Formatter
from .exceptions import InternalError
from .fields import AmazonSlots, AmazonField, AmazonCustom

log = logging.getLogger(__name__)


class IntentsSchema():
    apps = {}
    intents = {}

    @classmethod
    def get_intent(cls, intent):
        if intent not in cls.intents.keys():
            msg = "Unable to find an intent defined for '{0}'".format(intent)
            raise InternalError(msg)
        return cls.intents[intent]

    @classmethod
    def route(cls, session, intent, intent_kwargs):
        """Routes an intent to the proper method"""
        func, slot = cls.get_intent(intent)
        if slot and bool(intent_kwargs) is False:
            msg = "Intent '{0}' requires slots data and none was provided".format(intent)
            raise InternalError(msg)
        intent_kwargs['session'] = session.get('attributes', {})
        msg = "Routing: '{0}' with args {1} to '{2}.{3}'".format(intent,
                                                                 intent_kwargs,
                                                                 func.__module__,
                                                                 func.__name__)
        log.info(msg)
        return func(**intent_kwargs)

    @classmethod
    def register(cls, func, intent, slots=None, app="base"):
        if slots:
            if not issubclass(slots, AmazonSlots):
                msg = "'{0}' slot is not a valid alexa slot".format(slots.__name__)
                logging.warn(msg)
                slots = None
            else:
                s = slots()
                for field_name, field in s.get_fields().items():
                    if issubclass(field.__class__, AmazonField) is not True:
                        msg = "'{0}' on slot '{1}' is not a valid alexa slot field type"
                        msg = msg.format(field_name, s.__class__.__name__)
                        raise InternalError(msg)
        cls.intents[intent] = (func, slots)
        if app not in cls.apps:
            cls.apps[app] = []
        cls.apps[app] += [intent]

    @classmethod
    def generate_schema(cls, app="base"):
        """Generates the alexa intents schema json for an app"""
        intents = []
        for intent_name in cls.apps[app]:
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
    def generate_utterances(cls, app="base"):
        """Generates the alexa utterances schema for all intents for an app"""
        utterance_format = "{0} {1}"
        utterances = []
        for intent_name in cls.apps[app]:
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

    @classmethod
    def generate_custom_slots(cls, app="base"):
        slots = []
        for intent_name in cls.apps[app]:
            func, slot = cls.intents[intent_name]
            if slot:
                s = slot()
                for field_name, field in s.get_fields().items():
                    if issubclass(field.__class__, AmazonCustom):
                        msg = field.get_slot_name() + ":\n"
                        for choice in field.get_choices():
                            msg += "  " + choice + "\n"
                        msg += "\n"
                        slots.append(msg)
        return slots


def intent(*args, **kwargs):
    """
    Decorator that registers a function to the IntentsSchema
    app - The specific app grouping you'd like to register this intent to - Default: base
    intent - The intent you'd like to give this intent - Default: <The function name>
    slots - A slot object with a set of fields to determine the argument needs of the intent
    """
    invoked = bool(not args or kwargs)
    if not invoked:
        func, args = args[0], ()

    def register(func):
        app = kwargs.get('app', "base")
        intent = kwargs.get('intent', func.__name__)
        slots = kwargs.get('slots', None)
        IntentsSchema.register(func, intent, slots, app)
        return func
    return register if invoked else register(func)
