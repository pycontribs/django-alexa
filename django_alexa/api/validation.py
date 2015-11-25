import logging
import json
from rest_framework import serializers
from django.conf import settings

log = logging.getLogger(__name__)


def validate_reponse_limit(value):
    """
    value - a django response object
    """
    if len(value.content.encode('utf-8')) > 24:
        msg = "Alexa response content is bigger then 24 kilobytes"
        raise serializers.ValidationError(detail=msg)


def validate_app_ids(value):
    """
    value - an alexa app id
    """
    if value not in settings.ALEXA_APP_IDS:
        msg = "{0} is not a valid alexa skills application id"
        raise serializers.ValidationError(detail=msg.format(value))


def validate_current_timestamp(value):
    """
    value - a timestamp formatted in ISO 8601 (for example, 2015-05-13T12:34:56Z).
    """
    # TODO: flesh out current timestamp validation
    pass


def validate_char_limit(value):
    """
    value - a serializer to check to make sure the character limit is not excceed
    """
    # TODO: remove this logging once we validate the validator works
    log.info("CHAR VALIDATE: {0}".format(value))
    if len(json.dumps(value.data)) > 8000:
        msg = "{0} has exceeded the total character limit of 8000"
        raise serializers.ValidationError(detail=msg.format(value.__class__.__name__))


def validate_alexa_request(value):
    """
    value - a django request object
    """
    # TODO: validate alexa request headers
    # see https://github.com/anjishnu/ask-alexa-pykit/blob/master/lib/validation_utils.py
    log.info(value.META.items())
