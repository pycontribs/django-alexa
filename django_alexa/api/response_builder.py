from __future__ import absolute_import
from ..serializers import ASKResponseSerializer, ASKOutputSpeechSerializer, ASKRempromptSerializer, ASKCardSerializer


class ResponseBuilder(object):
    """
    Simple class to help users to build alexa responses
    """

    @classmethod
    def create_response(cls,
                        message=None, message_is_ssml=False,
                        reprompt=None, reprompt_is_ssml=False,
                        title=None, content=None, card_type=None,
                        end_session=True):
        """
        Shortcut to create a fully baked ASKResponseSerializer
        
        Output Speech:
        message - text message to be spoken out by the Echo
        message_is_ssml - If true the "message" is ssml formated and should be treated as such
        
        Reprompt Speech:
        reprompt - text message to be spoken out by the Echo
        reprompt_is_ssml - If true the "repropt" is ssml formated and should be treated as such
        
        Card:
        card_type - A string describing the type of card to render.
        title - A string containing the title of the card. (not applicable for cards of type LinkAccount).
        content - A string containing the contents of the card (not applicable for cards of type LinkAccount).
                  Note that you can include line breaks in the content for a card of type Simple.
        
        end_session - flag to determine whether this interaction should end the session
        
        For more comprehensive documentation see:
        https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference
        """
        data = {}
        data['shouldEndSession'] = end_session
        if message:
            data['outputSpeech'] = cls.create_speech(message=message,
                                                     is_ssml=message_is_ssml)
        if title or content:
            data['card'] = cls.create_card(title=title,
                                           content=content,
                                           card_type=card_type)
        if reprompt:
            data['reprompt'] = cls.create_reprompt(message=reprompt,
                                                   is_ssml=reprompt_is_ssml)
        response = ASKResponseSerializer(data=data)
        response.is_valid(raise_exception=True)
        return response

    @classmethod
    def create_speech(cls, message=None, is_ssml=False):
        data = {}
        if is_ssml:
            data['type'] = "SSML"
            data['ssml'] = message
        else:
            data['type'] = "PlainText"
            data['text'] = message
        speech = ASKOutputSpeechSerializer(data=data)
        speech.is_valid(raise_exception=True)
        return speech

    @classmethod
    def create_reprompt(cls, message=None, is_ssml=False):
        data = {}
        data['outputSpeech'] = cls.create_speech(message=message,
                                                 is_ssml=is_ssml)
        reprompt = ASKRempromptSerializer(data=data)
        reprompt.is_valid(raise_exception=True)
        return reprompt
     
    @classmethod
    def create_card(cls, title=None, content=None, card_type=None):
        data = {"type": card_type or "Simple"}
        if title: data["title"] = title
        if content: data["content"] = content
        card = ASKCardSerializer(data=data)
        card.is_valid(raise_exception=True)
        return card