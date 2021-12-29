#!/bin/bash

python3 $ROOT_DIR+restapi/manage.py dumpdata > $ROOT_DIR+restapi/fixtures/backup.json