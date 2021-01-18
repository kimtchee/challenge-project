#!/bin/bash

export FLASK_ENV='development'
export FLASK_APP='test_proj/app.py'
exec flask run
