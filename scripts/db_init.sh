#!/bin/bash

# make
python3 $API_ROOT+restapi/manage.py makemigrations accounts token_nfts
python3 $API_ROOT+restapi/manage.py makemigrations

# migrate
python3 $API_ROOT+restapi/manage.py migrate

# restore
python3 $API_ROOT+restapi/manage.py loaddata $API_ROOT+restapi/fixtures/roles.json
python3 $API_ROOT+restapi/manage.py loaddata $API_ROOT+restapi/fixtures/backup.json