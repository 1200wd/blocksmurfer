#!/bin/bash

source ~/venv/blocksmurfer/bin/activate
export PYTHONWARNINGS="ignore:Unverified HTTPS request"

#flask db upgrade
#flask translate compile

exec gunicorn -c gunicorn_config.py app:app
