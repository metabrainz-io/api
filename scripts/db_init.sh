#!/bin/bash

# make
python3 restapi/manage.py makemigrations accounts token_nfts
python3 restapi/manage.py makemigrations

# migrate
python3 restapi/manage.py migrate

# restore
python3 restapi/manage.py loaddata restapi/fixtures/roles.json
python3 restapi/manage.py loaddata restapi/fixtures/backup.json
