import json
import unittest as unittest

from django_alexa.api import ResponseBuilder


class TestAlexaApi(unittest.TestCase):

    def test_response_builder(self):
        data = {
            'version': '',
            'response': {
                'shouldEndSession': True,
                'outputSpeech': {'type': 'PlainText', 'text': 'This is a test!'}
            },
            'sessionAttributes': {}
        }
        response = ResponseBuilder.create_response(message="This is a test!")
        self.assertEquals(json.dumps(response), json.dumps(data))
