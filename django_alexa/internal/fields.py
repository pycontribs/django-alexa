'''These are the only fields supported by the Alexa skills kit'''
from __future__ import absolute_import


class AmazonSlots(object):
    '''Base for all amazon slots'''
    pass


class AmazonField(object):
    '''Base for all amazon fields'''
    amazon_name = None

    def get_slot_name(self):
        return self.amazon_name


class AmazonCustom(AmazonField):

    def get_choices(self):
        return []


class AmazonLiteral(AmazonField):
    amazon_name = "AMAZON.LITERAL"


class AmazonNumber(AmazonField):
    amazon_name = "AMAZON.NUMBER"


class AmazonDate(AmazonField):
    amazon_name = "AMAZON.DATE"


class AmazonTime(AmazonField):
    amazon_name = "AMAZON.TIME"


class AmazonDuration(AmazonField):
    amazon_name = "AMAZON.DURATION"


class AmazonUSCity(AmazonField):
    amazon_name = "AMAZON.US_CITY"


class AmazonFirstName(AmazonField):
    amazon_name = "AMAZON.US_FIRST_NAME"


class AmazonUSState(AmazonField):
    amazon_name = "AMAZON.US_STATE"


class AmazonFourDigitNumber(AmazonField):
    amazon_name = "AMAZON.FOUR_DIGIT_NUMBER"
