#!/bin/sh
set -e # stops execution on error
rm -rf "Disaster Communication Platform/dcp/migrations"
python "Disaster Communication Platform/manage.py" makemigrations --initial
python "Disaster Communication Platform/manage.py" syncdb --noinput
python "Disaster Communication Platform/manage.py" migrate dcp
python "Disaster Communication Platform/__travis/mkadmin.py"
python "Disaster Communication Platform/manage.py" test