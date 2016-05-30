#!/bin/sh
set -e # stops execution on error
rm -rf "Disaster Communication Platform/dcp/migrations"
python "Disaster Communication Platform/manage.py" makemigrations
python "Disaster Communication Platform/manage.py" migrate --run-syncdb --noinput
python "Disaster Communication Platform/__travis/mkadmin.py"
python "Disaster Communication Platform/manage.py" test