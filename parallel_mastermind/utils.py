import concurrent.futures
from . import settings
import importlib
import requests
import logging
logger = logging.getLogger(__name__)

def get_active_backends():
    services_data = settings.PARALLEL_SERVICES
    classes = []
    for service in services_data.keys():
        if services_data[service]['ENABLED'] == 'TRUE':
            active_backend = services_data[service]['ACTIVE_BACKEND']
            module_path, class_name = active_backend.split(':')
            module = importlib.import_module(module_path)
            classes.append(getattr(module, class_name))
    return classes


def run_tasks_in_parallel(name, method):
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for backend in [x for x in get_active_backends()]:
            futures.append(
                executor.submit(
                    getattr(backend(), method), name=name
                )
            )

        for future in concurrent.futures.as_completed(futures):
            try:
                results.append(future.result())
            except requests.ConnectTimeout as err:
                logger.error(err)
    return results
