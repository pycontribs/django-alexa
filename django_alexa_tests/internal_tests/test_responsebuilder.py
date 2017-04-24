import pytest
import mock
from django_alexa.internal import response_builder

class TestResponseBuilder:
    def test_card_image(self):
	rb = ResponseBuilder.create_response(card_type="Simple", content="Some content")
	pass
