#!/bin/sh

pip3 install -r requirements.txt
gunicorn -b :8080 -w 2 app:app
