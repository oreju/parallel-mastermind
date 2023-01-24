Parallel MasterMind
=======================

Parallel MasterMind is a demo project.

Task Description
-----------------------------
Given a list of APIs URLs (or database connections for simplicity,
but ideally it would be hidden behind some interface) make the query
(simple search string for a single field, e.g. first name) against
all of them (preferably in some kind of parallel/async fashion)
and combine results into single data structure that can be easily
accessed and traversed through (read only, it can object oriented
if you want).

Overview
-----------------------------
Parallel MasterMind API's is accessed http://0.0.0.0:8000/api/<str:name>/ address.

parallel_mastermind - containing parent class in backend.py file that could be reused
in others modules (connect to db, make get request for API), method to run
parallel in tasks.py and connection settings to APIs in settings.py file.
parallel_back4app - one of the modules that gathering US universities / colleges
from parseapi.back4app.com
parallel_unihipo - module is gathering information for to get universities from
universities.hipolabs API

List of APIs used
-----------------------------
1. http://universities.hipolabs.com/search
2. https://parseapi.back4app.com/classes/Usuniversitieslist_University
