#!/bin/bash

# make
python3 $ROOT_DIR+restapi/manage.py makemigrations accounts token_nfts
python3 $ROOT_DIR+restapi/manage.py makemigrations

# migrate
python3 $ROOT_DIR+restapi/manage.py migrate

# restore
python3 $ROOT_DIR+restapi/manage.py loaddata $ROOT_DIR+restapi/fixtures/roles.json
python3 $ROOT_DIR+restapi/manage.py loaddata $ROOT_DIR+restapi/fixtures/backup.json