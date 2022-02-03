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

# Make
python3 "${API_ROOT}/restapi/manage.py" makemigrations accounts token_nfts
python3 "${API_ROOT}/restapi/manage.py" makemigrations

# Migrate
python3 "${API_ROOT}/restapi/manage.py" migrate

# Restore
python3 "${API_ROOT}/restapi/manage.py" loaddata "${API_ROOT}/restapi/fixtures/roles.json"

# FIXME: Err installing fixtures: "The row in table 'token_blacklist_outstandingtoken' with primary key '1' has an invalid foreign key: token_blacklist_outstandingtoken..."
#python3 "${API_ROOT}/restapi/manage.py" loaddata "${API_ROOT}/restapi/fixtures/backup.json"

deactivate