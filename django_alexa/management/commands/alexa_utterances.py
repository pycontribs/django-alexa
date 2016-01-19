from __future__ import absolute_import
from django.core.management.base import BaseCommand
from ...internal import IntentsSchema


class Command(BaseCommand):
    help = 'Prints the Alexa Skills Kit utterances schema'

    def handle(self, *args, **options):
        data = IntentsSchema.generate_utterances()
        self.stdout.write('\n'.join(data))
