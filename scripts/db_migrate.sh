#!/bin/bash

python3 restapi/manage.py makemigrations
python3 restapi/manage.py migrate