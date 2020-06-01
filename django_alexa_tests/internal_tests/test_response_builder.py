import pytest
import mock

from django_alexa.internal import ResponseBuilder


class TestResponseBuilder:
    def test_card_simple(self):
        rb = ResponseBuilder.create_response(
               card_type="Simple",
               content="Some content", title="Title")
        assert rb['response']['card'] == {'content': 'Some content', 'title': 'Title', 'type': 'Simple'}

    def test_card_standard(self):
        rb = ResponseBuilder.create_response(
               card_type="Standard", card_text="Some text", title="Some title",
               card_image_small="https://example.org/pic_small.jpg",
               card_image_large="https://example.org/pic_large.jpg")
        assert rb['response']['card'] == {'type': 'Standard', 'title': 'Some title', 'image': {'smallImageUrl': 'https://example.org/pic_small.jpg', 'largeImageUrl': 'https://example.org/pic_large.jpg'}, 'text': 'Some text'}
