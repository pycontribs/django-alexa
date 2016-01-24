from __future__ import absolute_import
import logging

log = logging.getLogger(__name__)


class ResponseBuilder(object):
    """
    Simple class to help users to build alexa response data
    """
    version = ""

    @classmethod
    def set_version(cls, version):
        cls.version = version

    @classmethod
    def create_response(cls,
                        message=None, message_is_ssml=False,
                        reprompt=None, reprompt_is_ssml=False, reprompt_append=True,
                        title=None, content=None, card_type=None,
                        end_session=True, **kwargs):
        """
        Shortcut to create the data structure for an alexa response

        Output Speech:
        message - text message to be spoken out by the Echo
        message_is_ssml - If true the "message" is ssml formated and should be treated as such

        Reprompt Speech:
        reprompt - text message to be spoken out by the Echo
        reprompt_is_ssml - If true the "reprompt" is ssml formated and should be treated as such
        reprompt_append - If true the "reprompt" is append to the end of "message" for best practice voice interface design

        Card:
        card_type - A string describing the type of card to render. ("Simple", "LinkAccount")
        title - A string containing the title of the card. (not applicable for cards of type LinkAccount).
        content - A string containing the contents of the card (not applicable for cards of type LinkAccount).
                  Note that you can include line breaks in the content for a card of type Simple.

        end_session - flag to determine whether this interaction should end the session

        kwargs - Anything added here will be persisted across requests if end_session is False

        For more comprehensive documentation see:
        https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference
        """
        data = {}
        data['version'] = cls.version
        data['response'] = cls._create_response(message, message_is_ssml,
                                               reprompt, reprompt_is_ssml, reprompt_append,
                                               title, content, card_type,
                                               end_session)
        data['sessionAttributes'] = kwargs
        log.debug("Response Data: {0}".format(data))
        return data

    @classmethod
    def _create_response(cls,
                        message=None, message_is_ssml=False,
                        reprompt=None, reprompt_is_ssml=False, reprompt_append=True,
                        title=None, content=None, card_type=None,
                        end_session=True):
        data = {}
        data['shouldEndSession'] = end_session
        if message:
            if reprompt_append and reprompt is not None:
                message += " " + reprompt
                message_is_ssml = True if any([message_is_ssml, reprompt_is_ssml]) else False
            data['outputSpeech'] = cls._create_speech(message=message,
                                                      is_ssml=message_is_ssml)
        if title or content:
            data['card'] = cls._create_card(title=title,
                                            content=content,
                                            card_type=card_type)
        if reprompt:
            data['reprompt'] = cls._create_reprompt(message=reprompt,
                                                    is_ssml=reprompt_is_ssml)
        return data

    @classmethod
    def _create_speech(cls, message=None, is_ssml=False):
        data = {}
        if is_ssml:
            data['type'] = "SSML"
            data['ssml'] = "<speak>" + message + "</speak>"
        else:
            data['type'] = "PlainText"
            data['text'] = message
        return data

    @classmethod
    def _create_reprompt(cls, message=None, is_ssml=False):
        data = {}
        data['outputSpeech'] = cls._create_speech(message=message,
                                                 is_ssml=is_ssml)
        return data

    @classmethod
    def _create_card(cls, title=None, content=None, card_type=None):
        data = {"type": card_type or "Simple"}
        if title: data["title"] = title
        if content: data["content"] = content
        return data
