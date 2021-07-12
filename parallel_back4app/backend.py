from parallel_mastermind.backend import ServiceBackend
from django.conf import settings as settings_services

import collections
import urllib

Settings = collections.namedtuple('Settings', ['backend_url', 'application_id', 'api_key'])
back4app_settings = settings_services.PARALLEL_SERVICES.get('Back4APP', {})


class Back4APPBackend(ServiceBackend):

    def __init__(self):
        self.settings = Settings(
            backend_url=back4app_settings.get('CREDENTIALS').get(
                'url'),
            application_id=back4app_settings.get('CREDENTIALS').get(
                'application_id'),
            api_key=back4app_settings.get('CREDENTIALS').get(
                'api_key'),
        )

    def get_name_api(self, name):
        where = urllib.parse.quote_plus("""
        {
            "name": {
                "$regex": "^.*%s.*$"
            }
        }
        """ % name)
        url = self.settings.backend_url + '?&where=%s' % where
        headers = {
            'X-Parse-Application-Id': self.settings.application_id,
            'X-Parse-REST-API-Key': self.settings.api_key
        }
        data = self.get_request(url, headers=headers)
        if 'results' in data:
            data = data['results']
        return {'back4app': data}

    def get_name(self, name):
        return self.get_name_api(name)
