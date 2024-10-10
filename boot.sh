#!/bin/bash

source ~/venv/blocksmurfer/bin/activate
export PYTHONWARNINGS="ignore:Unverified HTTPS request"

#flask db upgrade
#flask translate compile

exec gunicorn -b 0.0.0.0:5000 --access-logfile - --error-logfile - app:app --workers 4

