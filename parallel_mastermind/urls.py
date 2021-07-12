"""parallel_mastermind URL Configuration"""
from django.urls import path
from parallel_mastermind.views import get_names

urlpatterns = [
    path('api/<str:name>/', get_names),
]
