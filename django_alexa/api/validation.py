from __future__ import absolute_import
import os
import logging
import json
import requests
import base64
import pytz
from datetime import datetime
from urlparse import urlparse
from OpenSSL import crypto
from rest_framework.exceptions import ValidationError
from django.conf import settings

log = logging.getLogger(__name__)


def validate_reponse_limit(value):
    """
    value - response content
    """
    log.debug("RESPONSE LIMIT VALIDATE: {0}".format(value))
    if len(value.encode('utf-8')) > 1000 * 1000 * 24:
        msg = "Alexa response content is bigger then 24 kilobytes"
        raise ValidationError(detail=msg)


def validate_app_ids(value):
    """
    value - an alexa app id
    """
    if value not in settings.ALEXA_APP_IDS:
        msg = "{0} is not a valid alexa skills application id"
        raise ValidationError(detail=msg.format(value))


def validate_current_timestamp(value):
    """
    value - a timestamp formatted in ISO 8601 (for example, 2015-05-13T12:34:56Z).
    """
    # TODO: flesh out current timestamp validation
    timestamp = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    utc_timestamp = pytz.utc.localize(timestamp)
    utc_timestamp_now = pytz.utc.localize(datetime.utcnow())
    delta = utc_timestamp_now - utc_timestamp
    log.info("Time drift is: {0}".format(delta.seconds))
    return False if delta.seconds > 150 else True


def validate_char_limit(value):
    """
    value - a serializer to check to make sure the character limit is not excceed
    """
    data = json.dumps(value)
    log.debug("CHAR LIMIT VALIDATING: {0}".format(data))
    if len(data) > 8000:
        msg = "{0} has exceeded the total character limit of 8000"
        raise ValidationError(detail=msg.format(value.__class__.__name__))


def verify_cert_url(cert_url):
    """
    Verify the URL location of the certificate
    """
    if cert_url is None:
        return False
    parsed_url = urlparse(cert_url)
    if parsed_url.scheme == 'https':
        if parsed_url.hostname == "s3.amazonaws.com":
            if os.path.normpath(parsed_url.path).startswith("/echo.api/"):
                return True
    return False


def verify_signature(request_body, signature, cert_url):
    """
    Verify the request signature is valid.
    """
    if signature is None or cert_url is None:
        return False
    cert_str = requests.get(cert_url)
    certificate = crypto.load_certificate(crypto.FILETYPE_PEM, str(cert_str.text))
    if certificate.has_expired() is True:
        return False
    if certificate.get_subject().CN != "echo-api.amazon.com":
        return False
    decoded_signature = base64.b64decode(signature)
    try:
        if crypto.verify(certificate, decoded_signature, request_body, 'sha1') is None:
            return True
    except:
        log.exception("Error occured during signature validation")
    return False


def validate_alexa_request(request_headers, request_body):
    """
    Validates this is a valid alexa request
    value - a django request object
    """
    # see https://github.com/anjishnu/ask-alexa-pykit/blob/388fb947009bc28671a09d258061529b494d09ad/lib/validation_utils.py
    log.debug(request_headers)
    log.debug(request_body)
    if settings.ALEXA_ENABLE_REQUEST_VERIFICATON is True:
        if verify_cert_url(request_headers.get('HTTP_SIGNATURECERTCHAINURL')) is False:
            raise ValidationError("Invalid Certificate Chain URL")
        if verify_signature(request_body, request_headers.get('HTTP_SIGNATURE'), request_headers.get('HTTP_SIGNATURECERTCHAINURL')) is False:
            raise ValidationError("Invalid Request Signature")
        #timestamp = json.loads(request_body)['request']['timestamp']
        #if validate_current_timestamp(timestamp) is False:
        #    raise ValidationError("Invalid Request Timestamp")
    
