#!/bin/bash

echo "Running install..."
python3 -m pip install -r requirements.txt

python3 manage.py collectstatic