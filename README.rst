django-alexa
============

.. image:: https://badge.fury.io/py/django-alexa.svg
    :target: https://badge.fury.io/py/django-alexa
    :alt: Version

.. image:: https://requires.io/github/rocktavious/django-alexa/requirements.png?branch=master
    :target: https://requires.io/github/rocktavious/django-alexa/requirements/?branch=master
    :alt: Requirements Status

Amazon Alexa Skills Kit integration for Django

The django-alexa framework leverages the django-rest-framework package to support
the REST API that alexa skills need to use, but wraps up the bolierplate intent
routing and schema creation that you'd handle.

Freeing you up to just write your alexa intents and utterances, and only
needing to provide minimal configuration for your alexa skills.

Quickstart
----------

Feeling impatient? I like your style.

.. code-block:: bash

    $ pip install django-alexa

In your django settings.py add the following:

.. code-block:: python

    INSTALLED_APPS = [
        'django-alexa',
        ...
    ]
    
    # Note currently you cannot distinctly service multiple apps from one django project
    # All intents and utterances will be generated for each app - known limitation
    ALEXA_APP_IDS = ("Your Amazon Alexa App ID",)
    ALEXA_CERT_FILEPATH = "path to cert file used for amazon alexa app"
    ALEXA_PUBLIC_KEY_FILEPATH = "path the key file for the cert file"

The ALEXA_* variables are used for incoming request validation for alexa
skills request from amazon to your django app.

In your django urls.py add the following:

.. code-block:: python

urlpatterns = [
    url(r'^', include('django_alexa.urls')),
    ...
]

Your django app will now have a new api endpoint at /alexa/ask
that will handle all the incoming request routing to intents for all
amazon alexa skills pointed to this endpoint.

In your django project make an alexa.py file.
This file is where you define all your alexa intents and utterances.
Example:

.. code-block:: python

    from django_alexa.api import intent, ResponseBuilder, Serializer, fields
    
    @intent(name="HelpIntent")
    def help():
        """
        ---
        this is my custom help utterance
        """
        return ResponseBuilder.create_response(message="Help!")
    
    class HoroscopeSerializer(Serializer):
        sign = fields.ChoiceField(label="HOROSCOPE_SIGNS", choices=(1,2,3,4,5))
        date = fields.DateField()
    
    @intent(serializer=HoroscopeSerializer)
    def GetHoroscope(sign, date):
        """
        ---
        what is the horoscope for {sign}
        what will the horoscope for {sign} be on {date}
        get me my horoscope
        {sign}
        """
        return ResponseBuilder.create_response(message="Your horoscope is...")

The django-alexa framework also provides two django management commands that
will build your intents and utterances schema for you straight from the code.
The django-alexa framework also defines some best practice intents to help
get you up and running even faster, but allows you to easily override them,
as seen above with the custom HelpIntent

.. code-block:: bash

    >>> python manage.py alexa_intents
    {
        "intents": [
            {
                "intent": "StopIntent", 
                "slots": []
            }, 
            {
                "intent": "HelpIntent", 
                "slots": []
            }, 
            {
                "intent": "GetHoroscope", 
                "slots": [
                    {
                        "name": "sign", 
                        "type": "HOROSCOPE_SIGNS"
                    }, 
                    {
                        "name": "date", 
                        "type": "AMAZON.DATE"
                    }
                ]
            }, 
            {
                "intent": "LaunchRequest", 
                "slots": []
            }, 
            {
                "intent": "SessionEndedRequest", 
                "slots": []
            }, 
            {
                "intent": "CancelIntent", 
                "slots": []
            }
        ]
    }

.. code-block:: python

    >>> python manage.py alexa_utterances
    AMAZON.HelpIntent this is my custom help utterance
    GetHoroscope what is the horoscope for {sign}
    GetHoroscope what will the horoscope for {sign} be on {date}
    GetHoroscope get me my horoscope
    GetHoroscope {sign}

Utterances can be added to your function's docstring seperating them from the
regular docstring by placing them after '---'.

Each line after '---' will be added as an utterance.

When defining utterances with variables in them make sure all of the requested
variables in any of the utterances are defined as fields in the serailizer
for that intent.

The django-alexa framework will throw errors when these management commands run
if things seem to be out of place or incorrect.

Lastly, the django-alexa framework provides a help class to generate the
kind of responses that alexa needs from your service.  This ResponseBuilder
class has a number of arguments to it and maps pretty directly to the
documentation on the alexa skills kit website about the response format.

Please see the documentation on the class for a summary of the details or head
to https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference
and checkout the more verbose documentation on proper alexa responses
