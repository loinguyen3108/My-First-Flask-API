#!/bin/sh
sleep 15
flask db init
flask db migrate
flask db upgrade

/venv/bin/python app.py