#!/bin/bash
python /app/src/manage.py initwgm && python gunicorn --chdir /app/src app.wsgi --bind 127.0.0.1:8888