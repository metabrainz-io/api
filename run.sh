#!/bin/bash

uwsgi --ini "${API_ROOT}/restapi/restapi.ini"
service nginx reload && service nginx restart

# if file exists
tail -f "${API_ROOT}/logs/uwsgi-emperor.log"