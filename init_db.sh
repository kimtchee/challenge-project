#!/bin/bash

psql -U postgres -d test -a -f ./db_scripts/deploy/0001_create_person_tables.sql
