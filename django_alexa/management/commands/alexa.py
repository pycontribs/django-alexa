from __future__ import absolute_import
from django.core.management import call_command
from ..base import AlexaBaseCommand


class Command(AlexaBaseCommand):
    help = "Prints the Alexa Skills Kit schema's for an app"

    def do_work(self, app):
        self.stdout.write("\n#### SCHEMAS FOR {0} ####\n".format(app))
        call_command("alexa_intents", app)
        call_command("alexa_custom_slots", app)
        call_command("alexa_utterances", app)
        self.stdout.write("\n#####################################\n")
