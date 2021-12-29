#!/bin/bash

# make \ migrate \ load
python3 restapi/manage.py makemigrations accounts && \
python3 restapi/manage.py makemigrations && \
python3 restapi/manage.py migrate && \
python3 restapi/manage.py loaddata restapi/fixtures/roles.json