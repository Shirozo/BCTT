#!/bin/bash

echo "Running install..."
pip install -r requirements.txt

python3.9 manage.py collectstatic