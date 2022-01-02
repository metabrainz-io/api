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

# Init
if [ ! -e "${API_ROOT}/restapi/static" ]
then
    echo "Initializing django '/static'.."
    source "${API_ROOT}/env/bin/activate"
    python3 "${API_ROOT}/restapi/manage.py" collectstatic
    deactivate
else
    echo "Found directory '/static'!"
fi

if [ ! -e "${API_ROOT}/restapi/media" ]
then
    echo "Creating django '/media'.."
    mkdir "${API_ROOT}/restapi/media"
else
    echo "Found directory '/media'!"
fi


cp "${API_ROOT}/nginx/restapi.conf" /etc/nginx/sites-available/


if [ ! -e "/etc/nginx/sites-enabled/restapi.conf" ]
then
    echo "Symlink from: 'sites-available/restapi.conf' to '/etc/nginx/sites-enabled/'.."
    ln -s /etc/nginx/sites-available/restapi.conf /etc/nginx/sites-enabled/
fi

if [ -e "/etc/nginx/sites-enabled/default" ]
then
    echo "Removing nginx defaults.."
    rm /etc/nginx/sites-enabled/default
fi

echo "Done initializing!"