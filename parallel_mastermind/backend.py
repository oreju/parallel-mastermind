import json
import requests
from django.db import connections, DatabaseError
import logging
logger = logging.getLogger(__name__)


class ServiceBackendNotImplemented(NotImplementedError):
    pass


class ServiceBackend:
    """ Basic service backed with only common methods pre-defined. """

    def __init__(self):
        self.settings = []
        self.database_parameters = {}

    def get_request(self, url, headers={}):
        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
        return json.loads(r.content.decode('utf-8'))

    # TODO: These methods could be used in the future.
    #  To be able to connect to Database if API's option is not available.

    def _get_db_connection(self, force=False):
        engine = self.database_parameters['engine']
        host = self.database_parameters['host']
        port = self.database_parameters['port']
        name = self.database_parameters['name']
        user = self.database_parameters['user']
        password = self.database_parameters['password']
        key = '/'.join([name, host, port])

        if key not in connections.databases or force:
            connections.databases[key] = {
                'ENGINE': engine,  # e.g. django.db.backends.postgresql',
                'NAME': name,
                'HOST': host,
                'PORT': port,
                'USER': user,
                'PASSWORD': password
            }

        return connections[key]

    def _execute_query(self, query, *args, **kwargs):
        logger.info('Executing query %s to External DB' % query)
        try:
            cursor = self._get_db_connection().cursor()
            cursor.execute(query, *args, **kwargs)
            return cursor
        except DatabaseError as e:
            logger.exception('Can not execute query the External DB.')
            raise e

    def get_name_db(self, name):
        # # -- EXAMPLE --
        # '''
        # Execute query to External DB to select name.
        # :param name: Search Name
        # :return names_list: [('name')]
        # '''
        #
        # query = (
        #     "SELECT name "
        #     "FROM org_unit "
        #     "WHERE name like %s"
        # )
        #
        # query = query % name.lower()
        # names_list = self._execute_query(query).fetchall()
        # return names_list
        pass

    def get_name_api(self, name):
        pass

    def get_name(self, name):
        raise ServiceBackendNotImplemented
