#!/bin/bash
source ~/venv/blocksmurfer/bin/activate
#flask db upgrade
#flask translate compile
exec gunicorn -b localhost:5000 --access-logfile - --error-logfile - app:app --workers 4

