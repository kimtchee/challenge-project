#!/bin/bash

export FLASK_ENV='development'
export FLASK_APP='person_service/app.py'
exec flask run
