#!/bin/sh
set -e # stops execution on error
rm -rf "Disaster Communication Platform/dcp/migrations"
rm -f "Disaster Communication Platform/db.sqlite3"
python "Disaster Communication Platform/manage.py" makemigrations --noinput dcp
python "Disaster Communication Platform/manage.py" migrate --noinput
python "Disaster Communication Platform/__travis/mkadmin.py"
python "Disaster Communication Platform/manage.py" test