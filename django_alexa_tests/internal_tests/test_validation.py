import pytest
import mock
from django_alexa.internal import validation
from imp import reload
from datetime import datetime, timedelta
import pytz
import os


class TestValidation:
    def test_validate_response_limit(self):
        valid_value = 'x' * 1000 * 1000 * 24
        validation.validate_response_limit(valid_value)

        with pytest.raises(Exception) as exc_info:
            invalid_value = 'x' * 1000 * 1000 * 24 + 'x'
            validation.validate_response_limit(invalid_value)
            msg = "Should raise exception, response > 24 kb"
        assert "InternalError" in str(exc_info), msg

    @mock.patch.dict(os.environ, {'ALEXA_APP_ID_DEFAULT': 'valid_app_id_default'})
    def test_validate_app_ids(self):
        reload(validation)
        valid_app_id = 'valid_app_id_default'
        validation.validate_app_ids(valid_app_id)

        with pytest.raises(Exception) as exc_info:
            invalid_app_id = 'non_valid_app_id'
            validation.validate_app_ids(invalid_app_id)
            msg = "Should raise exception, app id not valid"
        assert "InternalError" in str(exc_info), msg

    def test_validate_current_timestamp(self):
        current_time = datetime.utcnow()
        timestamp = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        msg = 'Should be a valid timestamp'
        assert validation.validate_current_timestamp(timestamp), msg

        invalid_time = current_time - timedelta(minutes=2, seconds=30)
        invalid_timestamp = invalid_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        msg = 'Shoud not be a valid timestamp'
        assert not validation.validate_current_timestamp(invalid_timestamp), msg

    def test_validate_char_limit(self):
        valid_value = 'x' * 7998
        validation.validate_char_limit(valid_value)

        with pytest.raises(Exception) as exc_info:
            invalid_value = 'x' * 8000 + 'x'
            validation.validate_char_limit(invalid_value)
            msg = "Should raise exception, too many characters"
        assert "InternalError" in str(exc_info), msg

    def test_verify_cert_url(self):
        url = "https://s3.amazonaws.com/echo.api/test"
        assert validation.verify_cert_url(url), 'Should be a valid url without port'

        url = "https://s3.amazonaws.com:443/echo.api/test"
        assert validation.verify_cert_url(url), 'Should be a valid url with port'

        url = " "
        assert not validation.verify_cert_url(url), 'Should be an invalid url'

        url = None
        assert not validation.verify_cert_url(url), 'Should be an invalid url, given None'

    def test_verify_signature(self):
        request_body = 'request_body'
        signature = None
        cert_url = ' '
        msg = 'Should fail, signature = None'
        assert not validation.verify_signature(request_body, signature, cert_url), msg

        signature = ''
        msg = 'Should fail, signature is empty'
        assert not validation.verify_signature(request_body, signature, cert_url), msg

    def test_validate_alexa_request(self):
        pass
