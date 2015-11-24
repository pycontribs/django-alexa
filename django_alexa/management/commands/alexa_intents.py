from __future__ import absolute_import
import json
from django.core.management.base import BaseCommand, CommandError
from ...api import IntentsSchema

class Command(BaseCommand):
    help = 'Prints the Alexa Skills Kit intents schema'

    def handle(self, *args, **options):
        data = IntentsSchema.generate_schema()
        self.stdout.write(json.dumps(data, indent=4, sort_keys=True))