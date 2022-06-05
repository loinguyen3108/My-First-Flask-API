#!/bin/sh bash
flask db init
flask db migrate
flask db upgrade