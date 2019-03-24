from payments.fetch_data.worker import celery_app as my_app
from payments.fetch_data.tasks import start_fetching

start_fetching()