#!/bin/bash

# Set envs
ENV=.env
if [ ! -e ${ENV} ]
then
    echo "Err: Failed to initialize, no '.env' file found."
    exit
fi

set -a
source $ENV
set +b

source "${API_ROOT}/env/bin/activate"

# Dump
python3 "${API_ROOT}/restapi/manage.py" dumpdata > "${API_ROOT}/restapi/fixtures/backup.json"

deactivate