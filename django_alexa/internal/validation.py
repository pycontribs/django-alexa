from __future__ import absolute_import
import os
import sys
import ast
import logging
import json
import requests
import base64
import pytz
from datetime import datetime, timedelta
from OpenSSL import crypto
from .exceptions import InternalError
# Test for python 3
try:
    from urllib.parse import urlparse
except:
    from urlparse import urlparse

log = logging.getLogger(__name__)


ALEXA_APP_IDS = dict([(str(os.environ[envvar]), envvar.replace("ALEXA_APP_ID_", "")) for envvar in os.environ.keys() if envvar.startswith('ALEXA_APP_ID_')])
ALEXA_REQUEST_VERIFICATON = ast.literal_eval(os.environ.get('ALEXA_REQUEST_VERIFICATON', 'True'))


def validate_response_limit(value):
    """
    value - response content
    """
    if sys.getsizeof(value) >= 1000 * 1000 * 24 + sys.getsizeof('a'):
        msg = "Alexa response content is bigger then 24 kilobytes: {0}".format(value)
        raise InternalError(msg)


def validate_app_ids(value):
    """
    value - an alexa app id
    """
    if value not in ALEXA_APP_IDS.keys():
        msg = "{0} is not one of the valid alexa skills application ids for this service".format(value)
        raise InternalError(msg)


def validate_current_timestamp(value):
    """
    value - a timestamp formatted in ISO 8601 (for example, 2015-05-13T12:34:56Z).
    """
    timestamp = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    utc_timestamp = pytz.utc.localize(timestamp)
    utc_timestamp_now = pytz.utc.localize(datetime.utcnow())
    delta = utc_timestamp - utc_timestamp_now
    log.debug("DATE TIME CHECK!")
    log.debug("Alexa: {0}".format(utc_timestamp))
    log.debug("Server: {0}".format(utc_timestamp_now))
    log.debug("Delta: {0}".format(delta))
    if abs(delta) > timedelta(minutes=2, seconds=30):
        return False
    else:
        return True


def validate_char_limit(value):
    """
    value - a serializer to check to make sure the character limit is not excceed
    """
    data = json.dumps(value)
    if len(data) > 8000:
        msg = "exceeded the total character limit of 8000: {}".format(data)
        raise InternalError(msg)


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
                if parsed_url.port is None:
                    return True
                elif parsed_url.port == 443:
                    return True
    return False


def verify_signature(request_body, signature, cert_url):
    """
    Verify the request signature is valid.
    """
    if signature is None or cert_url is None:
        return False
    if len(signature) == 0:
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
        raise InternalError("Error occured during signature validation", {"error": 400})
    return False


def validate_alexa_request(request_headers, request_body):
    """
    Validates this is a valid alexa request
    value - a django request object
    """
    if ALEXA_REQUEST_VERIFICATON is True:
        timestamp = json.loads(request_body)['request']['timestamp']
        # For each of the following errors, the alexa service expects an HTTP error code. This isn't well documented.
        # I'm going to return 403 forbidden just to be safe (but need to pass a message to the custom error handler,
        # hence why I'm adding an argument when raising the error)
        if validate_current_timestamp(timestamp) is False:
            raise InternalError("Invalid Request Timestamp", {"error": 400})
        if verify_cert_url(request_headers.get('HTTP_SIGNATURECERTCHAINURL')) is False:
            raise InternalError("Invalid Certificate Chain URL", {"error": 400})
        if verify_signature(request_body, request_headers.get('HTTP_SIGNATURE'), request_headers.get('HTTP_SIGNATURECERTCHAINURL')) is False:
            raise InternalError("Invalid Request Signature", {"error": 400})
