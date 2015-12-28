from __future__ import absolute_import
from .api import intent, ResponseBuilder


@intent
def LaunchRequest():
    """
    Default Start Session Intent
    ---
    launch
    open
    resume
    start
    run
    load
    begin
    """
    return ResponseBuilder.create_response(message="Welcome. Say help if you would like help. What would you like to do next?",
                                           reprompt="What would you like to do next?",
                                           end_session=False)


@intent
def CancelIntent():
    """
    Default Cancel Intent
    ---
    cancel
    """
    return ResponseBuilder.create_response(message="Actions Canceled! What would you like to do next?",
                                           reprompt="What would you like to do next?",
                                           end_session=False)


@intent
def StopIntent():
    """
    Default Stop Intent
    ---
    stop
    end
    """
    return ResponseBuilder.create_response(message="Stopping Actions. Goodbye!")


@intent
def HelpIntent():
    """
    Default Help Intent
    ---
    help
    info
    information
    """
    return ResponseBuilder.create_response(message="No help was configured!")


@intent
def SessionEndedRequest():
    """
    Default End Session Intent
    ---
    quit
    nevermind
    """
    return ResponseBuilder.create_response()
