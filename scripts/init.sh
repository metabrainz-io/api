#!/bin/bash

# check dirs
# python3 $API_ROOT/restapi/manage.py collectstatic
# mkdir $API_ROOT/restapi/media

cp $API_ROOT/nginx/restapi.conf /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/restapi.conf /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default