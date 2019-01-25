#!/usr/bin/env bash

# this script should be executed as: nohup ./deploy.sh & disown
export KEY=$(python -c "import os, base64; print b'%s' % base64.b64encode(os.urandom(24))")
rm -f catalog.log
gunicorn --log-level info --log-file catalog.log -w 4 -b 127.0.0.1:8080 application:app