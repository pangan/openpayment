#!/bin/bash

celery worker --app=payments.fetch_data.worker.celery_app --concurrency=1 --loglevel=INFO
