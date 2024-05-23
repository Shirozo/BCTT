#!/bin/bash

# Exit on any error
set -e

# Ensure the necessary environment variables are se

# Change to the directory containing manage.py

# Run the Django management command to create the superuser
echo "Creating superuser..."
python manage.py createsuperuser --no-input --username 'hello' --email '1@1.com' <<EOF
'123@admin'
EOF
