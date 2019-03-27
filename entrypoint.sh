#!/bin/bash -ex

celery worker --app=payments.fetch_data.tasks  --loglevel=INFO -B &

gunicorn -b0.0.0.0:5000 --reload -w1 payments.app:api
