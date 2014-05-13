#!/bin/bash

HTPASSWD_FILE=/data/myfile.htpasswd
SECRET_KEY="MYKEYAAFADFADFAF"
REGEXP="\d{11}@test.com"
TARGET_PAGE=www.google.com

export HTPASSWD_FILE SECRET_KEY REGEXP TARGET_PAGE
source /data/backstage/bin/activate
gunicorn -error-logfile htpwd_error.log -p gunicorn.pid -D -c gunicorn.py htpwd.htpwd:app
