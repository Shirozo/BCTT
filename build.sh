#!/bin/bash

echo "Running install..."
python3 -m pip install -r requirements.txt
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

set -e

python3 manage.py collectstatic

echo "Creating superuser..."
python manage.py createsuperuser --no-input --username 'admin' --email '1@1.com' <<EOF
'admin'
EOF
