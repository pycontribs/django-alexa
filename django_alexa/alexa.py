from __future__ import absolute_import
from .api import intent, ResponseBuilder


@intent
def LaunchRequest():
    """Default Start Session Intent"""
    return ResponseBuilder.create_response(message="Welcome. Say help if you would like help. What would you like to do next?",
                                           reprompt="What would you like to do next?",
                                           end_session=False)

@intent
def CancelIntent():
    """Default Cancel Intent"""
    return ResponseBuilder.create_response(message="Actions Canceled! What would you like to do next?",
                                           reprompt="What would you like to do next?",
                                           end_session=False)

@intent
def StopIntent():
    """Default Stop Intent"""
    return ResponseBuilder.create_response(message="Stopping Actions. Goodbye!")

@intent
def HelpIntent():
    """Default Help Intent"""
    return ResponseBuilder.create_response(message="No help was configured!")


@intent
def SessionEndedRequest():
    """Default End Session Intent"""
    return ResponseBuilder.create_response(message="Have a nice day. Goodbye!")
