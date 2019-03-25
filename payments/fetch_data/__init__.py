import os

from payments.fetch_data.worker import celery_app as my_app
from payments.fetch_data.tasks import start_fetching

if not os.getenv('PAYMENTS_TESTING_MODE'):
    start_fetching()
