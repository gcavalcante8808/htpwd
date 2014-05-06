#!/bin/bash

HTPASSWD_FILE=/data/myfile.htpasswd
SECRET_KEY="MYKEYAAFADFADFAF"
REGEXP="\d{11}@test.com"
TARGET_PAGE=www.google.com

export HTPASSWD_FILE SECRET_KEY REGEXP TARGET_PAGE
source /data/backstage3.3/bin/activate
gunicorn -D -c gunicorn.py htpwd.htpwd:app
