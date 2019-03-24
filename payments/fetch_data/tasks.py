"""
By Amir Mofakhar <amir@mofakhar.info>
"""
import logging
from time import sleep

import requests
from celery.result import AsyncResult

from payments.settings import (OPEN_PAYMENTS_API_ENDPOINT, CELERY_TASK_ID,
                               FETCHING_DATA_PERIOD_SECOND)
from payments.fetch_data.worker import celery_app

_LOG = logging.getLogger()


def get_payments_data_from_api():
    payments_data = None
    try:
        payments_request = requests.get(OPEN_PAYMENTS_API_ENDPOINT)
        if payments_request.status_code == 200:
            payments_data = payments_request.json()
    except Exception as e:
        _LOG.error('payments request error: %s' % str(e))
    return payments_data


@celery_app.task
def fetch():  # pragma: no cover
    fetch.apply_async(None, countdown=FETCHING_DATA_PERIOD_SECOND, task_id=CELERY_TASK_ID)
    return get_payments_data_from_api()


def start_fetching():
    fetch.apply_async(None, task_id=CELERY_TASK_ID)


def get_data_from_celery():
    result = AsyncResult(CELERY_TASK_ID, app=celery_app)
    ret_data = None

    sleep_time = 1
    while not result.ready():
        _LOG.warning('Celery not ready!')
        sleep(sleep_time)
        sleep_time += 1

    try:
        ret_data = result.get(timeout=10)
    except Exception as e:
        _LOG.error('Celery error: %s' % str(e))

    return ret_data


