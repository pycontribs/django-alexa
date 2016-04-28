from __future__ import absolute_import
from .api import intent, ResponseBuilder


@intent
def LaunchRequest(**kwargs):
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
    return ResponseBuilder.create_response(message="Welcome.",
                                           reprompt="What would you like to do next?",
                                           end_session=False)


@intent
def CancelIntent(**kwargs):
    """
    Default Cancel Intent
    ---
    cancel
    """
    return ResponseBuilder.create_response(message="Canceling actions not configured!",
                                           reprompt="What would you like to do next?",
                                           end_session=False)


@intent
def StopIntent(**kwargs):
    """
    Default Stop Intent
    ---
    stop
    end
    nevermind
    """
    return ResponseBuilder.create_response(message="Stopping actions not configured!")


@intent
def HelpIntent(**kwargs):
    """
    Default Help Intent
    ---
    help
    info
    information
    """
    return ResponseBuilder.create_response(message="No help was configured!")


@intent
def SessionEndedRequest(**kwargs):
    """
    Default End Session Intent
    ---
    quit
    """
    return ResponseBuilder.create_response()
