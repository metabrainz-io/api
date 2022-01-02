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

# Run application
uwsgi --ini "${API_ROOT}/restapi/restapi.ini"
service nginx reload && service nginx restart

# Watch logs
LOG_DJANGO="${API_ROOT}/logs/django.log"
LOG_UWSGI="${API_ROOT}/logs/uwsgi-emperor.log"

if [[ $1 == '--watch' ]]
then
    if [[ $2 == 'django' ]]
    then
        if [ -f ${LOG_DJANGO} ]
        then
            tail -f $LOG_DJANGO
            exit
        else
            echo "Err: No django logs found"
        fi
    elif [[ $2 == 'uwsgi' ]]
    then
        if [ -f ${LOG_UWSGI} ]
        then
            tail -f $LOG_UWSGI
            exit
        else
            echo "Err: No uwsgi logs found"
        fi
    fi
fi