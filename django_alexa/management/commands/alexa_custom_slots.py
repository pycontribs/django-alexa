from __future__ import absolute_import
import json
from ..base import AlexaBaseCommand


class Command(AlexaBaseCommand):
    help = 'Prints the Alexa Skills Kit custom slot schema for an app'

    def do_work(self, app):
        data = IntentsSchema.generate_custom_slots(app=app)
        self.stdout.write('\n'.join(data))
