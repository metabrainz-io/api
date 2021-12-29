#!/bin/bash

python3 $ROOT_DIR+restapi/manage.py makemigrations
python3 $ROOT_DIR+restapi/manage.py migrate