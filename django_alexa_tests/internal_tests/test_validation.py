import pytest
from django_alexa.internal import validation


class TestValidateResponseLimit:
    def test_validate_response_limit_fail(self):
        with pytest.raises(Exception) as exc_info:
            value = 'x' * 1000 * 1000 * 24 + 'x'
            validation.validate_response_limit(value)
            msg = "Should raise exception, response > 24 kb"
        assert "InternalError" in str(exc_info), msg

    def test_validate_response_limit_pass(self):
        value = 'x' * 1000 * 1000 * 24
        validation.validate_response_limit(value)


class TestValidateAppIds:
    def test_validate_app_ids_fail(self):
        with pytest.raises(Exception) as exc_info:
            app_id = 'non_valid_id_example'
            validation.validate_app_ids(app_id)
            msg = "Should raise exception, app id not valid"
        assert "InternalError" in str(exc_info), msg

    def test_validate_app_ids_pass(self):
        pass

class TestVerifyCertUrl:
    def test_valid_url_1(self):
        url = "https://s3.amazonaws.com/echo.api/test"
        assert validation.verify_cert_url(url), 'Should be a valid url without port'

    def test_valid_url_2(self):
        url = "https://s3.amazonaws.com:443/echo.api/test"
        assert validation.verify_cert_url(url), 'Should be a valid url with port'

    def test_invalid_url_1(self):
        url = " "
        assert not validation.verify_cert_url(url), 'Should be an invalid url'

    def test_invalid_url_2(self):
        url = None
        assert not validation.verify_cert_url(url), 'Should be an invalid url, given None'