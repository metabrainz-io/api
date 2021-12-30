#!/bin/bash

python3 "${API_ROOT}/restapi/manage.py" dumpdata > "${API_ROOT}/restapi/fixtures/backup.json