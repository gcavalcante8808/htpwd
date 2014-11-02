#!/bin/bash

source /data/backstage/bin/activate
gunicorn -error-logfile htpwd_error.log -p gunicorn.pid -D -c gunicorn.py htpwd.htmanager:APP
