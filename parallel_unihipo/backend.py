from parallel_mastermind.backend import ServiceBackend
from django.conf import settings as settings_services

import collections

Settings = collections.namedtuple('Settings', ['backend_url'])
unihipo_settings = settings_services.PARALLEL_SERVICES.get('UniHipo', {})


class UniHipoBackend(ServiceBackend):

    def __init__(self):
        self.settings = Settings(
            backend_url=unihipo_settings.get('CREDENTIALS').get('url')
        )

    def get_name_api(self, name=False):
        url = self.settings.backend_url + '?name=%s' % name
        data = self.get_request(url)
        return {'unihipo': data}

    def get_name(self, name):
        return self.get_name_api(name)
