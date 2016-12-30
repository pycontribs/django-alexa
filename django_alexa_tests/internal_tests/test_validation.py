import pytest
from django_alexa.internal import validation


class TestVerifyCertUrl:
    def test_valid_url_1(self):
        url = "https://s3.amazonaws.com/echo.api/test"
        r = validation.verify_cert_url(url)
        assert r == True, 'Should be a valid url without port'

    def test_valid_url_2(self):
        url = "https://s3.amazonaws.com:443/echo.api/test"
        r = validation.verify_cert_url(url)
        assert r == True, 'Should be a valid url with port'

    def test_invalid_url_1(self):
        url = "this is the url"
        r = validation.verify_cert_url(url)
        assert r == False, 'Should be an invalid url'

    def test_invalid_url_2(self):
        url = None
        r = validation.verify_cert_url(url)
        assert r == False, 'Should be an invalid url, given None'