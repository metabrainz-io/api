#!/bin/bash

python3 $API_ROOT+restapi/manage.py makemigrations
python3 $API_ROOT+restapi/manage.py migrate