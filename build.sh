#!/usr/bin/env bash
# build.sh

set -o errexit  # Exit on error

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate
