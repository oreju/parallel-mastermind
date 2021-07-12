from .utils import run_tasks_in_parallel
from django.http import HttpResponse


def get_names(request, name):
    results = run_tasks_in_parallel(name, 'get_name')
    return HttpResponse(results)


