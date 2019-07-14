django-alexa
============

.. image:: https://badge.fury.io/py/django-alexa.svg
    :target: https://badge.fury.io/py/django-alexa
    :alt: Current Version

.. image:: https://travis-ci.com/pycontribs/django-alexa.svg?branch=master
    :target: https://travis-ci.com/pycontribs/django-alexa
    :alt: Build Status

.. image:: https://coveralls.io/repos/github/pycontribs/django-alexa/badge.svg?branch=master
    :target: https://coveralls.io/github/pycontribs/django-alexa?branch=master

.. image:: https://pyup.io/repos/github/pycontribs/django-alexa/shield.svg
     :target: https://pyup.io/repos/github/pycontribs/django-alexa/
     :alt: Updates

.. image:: https://pyup.io/repos/github/pycontribs/django-alexa/python-3-shield.svg
     :target: https://pyup.io/repos/github/pycontribs/django-alexa/
     :alt: Python 3

.. image:: https://requires.io/github/pycontribs/django-alexa/requirements.svg?branch=master
     :target: https://requires.io/github/pycontribs/django-alexa/requirements/?branch=master
     :alt: Requirements Status

.. image:: https://snyk.io/test/github/pycontribs/django-alexa/badge.svg?targetFile=requirements.txt
     :target: https://snyk.io/test/github/pycontribs/django-alexa/badge.svg?targetFile=requirements.txt
     :alt: Vulnerbilities Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Code Style: black

Amazon Alexa Skills Kit integration for Django

The django-alexa framework leverages the django-rest-framework package to support
the REST API that alexa skills need to use, but wraps up the bolierplate for intent
routing and response creation that you'd need to write yourself.

Freeing you up to just write your alexa intents and utterances.

Full Documentation
------------------
https://django-alexa.readthedocs.io/en/latest/

Quickstart
----------

Feeling impatient? I like your style.

.. code-block:: bash

    $ pip install django-alexa

In your django settings.py add the following:

.. code-block:: python

    INSTALLED_APPS = [
        'django_alexa',
        'rest_framework',  # don't forget to add this too
        ...
    ]

In your django urls.py add the following:

.. code-block:: python

    urlpatterns = [
        url(r'^', include('django_alexa.urls')),
        ...
    ]

Your django app will now have a new REST api endpoint at `/alexa/ask/`
that will handle all the incoming request and route them to the intents defined
in any "alexa.py" file.

Set environment variables to configure the validation needs:

.. code-block:: bash

    ALEXA_APP_ID_DEFAULT="Your Amazon Alexa App ID DEFAULT"
    ALEXA_APP_ID_OTHER="Your Amazon Alexa App ID OTHER" # for each app
    ALEXA_REQUEST_VERIFICATON=True # Enables/Disable request verification


You can service multiple alexa skills by organizing your intents by an app name.
See the intent decorator's "app" argument for more information.

If you set your django project to DEBUG=True django-alexa will also do some
helpful debugging for you during request ingestion, such as catch all exceptions
and give you back a stacktrace and error type in the alexa phone app.

django-alexa is also configured to log useful information such as request body,
request headers, validation as well as response data, this is all configured
through the standard python logging setup using the logger 'django-alexa'

In your django project make an `alexa.py` file.
This file is where you define all your alexa intents and utterances.
Each intent must return a valid alexa response dictionary.  To aid in this the
django-alexa api provides a helper class called `ResponseBuilder`.
This class has a function to speed up building these dictionaries for responses.

Please see the documentation on the class for a summary of the details or head
to https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference
and checkout the more verbose documentation on proper alexa responses

Example:

.. code-block:: python

    from django_alexa.api import fields, intent, ResponseBuilder

    HOUSES = ("gryffindor", "hufflepuff", "ravenclaw", "slytherin")

    @intent
    def LaunchRequest(session):
        """
        Hogwarts is a go
        ---
        launch
        start
        run
        begin
        open
        """
        return ResponseBuilder.create_response(message="Welcome to Hog warts school of witchcraft and wizardry!",
                                               reprompt="What house would you like to give points to?",
                                               end_session=False,
                                               launched=True)


    class PointsForHouseSlots(fields.AmazonSlots):
        house = fields.AmazonCustom(label="HOUSE_LIST", choices=HOUSES)
        points = fields.AmazonNumber()


    @intent(slots=PointsForHouseSlots)
    def AddPointsToHouse(session, house, points):
        """
        Direct response to add points to a house
        ---
        {points} {house}
        {points} points {house}
        add {points} points to {house}
        give {points} points to {house}
        """
        kwargs = {}
        kwargs['message'] = "{0} points added to house {1}.".format(points, house)
        if session.get('launched'):
            kwargs['reprompt'] = "What house would you like to give points to?"
            kwargs['end_session'] = False
            kwargs['launched'] = session['launched']
        return ResponseBuilder.create_response(**kwargs)

The django-alexa framework also provides two django management commands that
will build your intents and utterances schema for you by inspecting the code.
The django-alexa framework also defines some best practice intents to help
get you up and running even faster, but allows you to easily override them,
as seen above with the custom LaunchRequest.

.. code-block:: bash

    >>> python manage.py alexa_intents
    {
        "intents": [
            {
                "intent": "StopIntent",
                "slots": []
            },
            {
                "intent": "PointsForHouse",
                "slots": [
                    {
                        "name": "points",
                        "type": "AMAZON.NUMBER"
                    },
                    {
                        "name": "house",
                        "type": "HOUSE_LIST"
                    }
                ]
            },
            {
                "intent": "HelpIntent",
                "slots": []
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
                "intent": "UnforgivableCurses",
                "slots": []
            },
            {
                "intent": "CancelIntent",
                "slots": []
            }
        ]
    }

.. code-block:: bash

    >>> python manage.py alexa_utterances
    StopIntent stop
    StopIntent end
    HelpIntent help
    HelpIntent info
    HelpIntent information
    LaunchRequest launch
    LaunchRequest start
    LaunchRequest run
    LaunchRequest begin
    LaunchRequest open
    PointsForHouse {points} {house}
    PointsForHouse {points} points {house}
    PointsForHouse add {points} points to {house}
    PointsForHouse give {points} points to {house}
    SessionEndedRequest quit
    SessionEndedRequest nevermind
    CancelIntent cancel

.. code-block:: bash

    >>> python manage.py alexa_custom_slots
    HOUSE_LIST:
      gryffindor
      hufflepuff
      ravenclaw
      slytherin

There is also a convience that will print each of this grouped by app name

.. code-block:: bash

    >>> python manage.py alexa
    ... All of the above data output ...



Utterances can be added to your function's docstring seperating them from the
regular docstring by placing them after '---'.

Each line after '---' will be added as an utterance.

When defining utterances with variables in them make sure all of the requested
variables in any of the utterances are defined as fields in the slots
for that intent.

The django-alexa framework will throw errors when these management commands run
if things seem to be out of place or incorrect.


Contributing
------------

- The master branch is meant to be stable. I usually work on unstable stuff on a personal branch.
- Fork the master branch ( https://github.com/pycontribs/django-alexa/fork )
- Create your branch (`git checkout -b my-branch`)
- Install required dependencies via pipenv install
- Run the unit tests via pytest or tox
- Run `tox`, this will run black (for formatting code), flake8 for linting and pytests
- Commit your changes (git commit -am 'added fixes for something')
- Push to the branch (git push origin my-branch)
- If you want to merge code from the master branch you can set the upstream like this: 
  `git remote add upstream https://github.com/pycontribs/django-alexa.git`
- Create a new Pull Request (Travis CI will test your changes)
- And you're done!

- Features, Bug fixes, bug reports and new documentation are all appreciated!
- See the github issues page for outstanding things that could be worked on.


Credits: Kyle Rockman 2016
