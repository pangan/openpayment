#!/bin/bash

celery worker --app=payments.fetch_data.tasks --concurrency=1 --loglevel=INFO -B
