from __future__ import absolute_import
import json
from ..base import AlexaBaseCommand
from ...internal import IntentsSchema


class Command(AlexaBaseCommand):
    help = 'Prints the Alexa Skills Kit intents schema for an app'

    def do_work(self, app):
        data = IntentsSchema.generate_schema(app=app)
        self.stdout.write(json.dumps(data, indent=4, sort_keys=True) + "\n")
