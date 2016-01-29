from __future__ import absolute_import
from django.core.management.base import BaseCommand
from ..internal import IntentsSchema


class AlexaBaseCommand(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('args', metavar='app_label', nargs='*',
            help='Restricts data to the specified app_label')
        parser.add_argument('-a', '--all', action='store_true', dest='do_all_apps', default=False,
            help="If specified will return all apps schema's")

    def handle(self, *app_labels, **options):
        do_all_apps = options.get('do_all_apps')
        if len(app_labels) == 0:
            if do_all_apps:
                app_labels = IntentsSchema.apps.keys()
            else:
                app_labels = ["base"]
        for app in app_labels:
            self.do_work(app)
