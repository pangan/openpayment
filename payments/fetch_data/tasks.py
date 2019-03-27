"""
By Amir Mofakhar <amir@mofakhar.info>
"""
import logging
from time import sleep

from celery.result import AsyncResult
import requests

from payments.common.utils import get_keys_from_dict
from payments.fetch_data.worker import celery_app
from payments.settings import (CELERY_TASK_ID, FETCHING_DATA_PERIOD_SECOND,
                               OPEN_PAYMENTS_API_ENDPOINT)

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


@celery_app.on_after_configure.connect
def setup_periodic_tasks(**kwargs):  # pragma: no cover
    # Fetching for the first time
    fetch.apply_async((), task_id=CELERY_TASK_ID)

    # Fetching periodically
    celery_app.add_periodic_task(FETCHING_DATA_PERIOD_SECOND, fetch.s(),
                                 name='my_task', task_id=CELERY_TASK_ID)


@celery_app.task
def fetch():  # pragma: no cover
    data = get_payments_data_from_api()
    data_fields.apply_async((data,), task_id='fields-{}'.format(CELERY_TASK_ID))
    return data


@celery_app.task
def data_fields(data):  # pragma: no cover
    ret_fields = get_keys_from_dict(data)
    return ret_fields


def _get_from_celery(task_id):  # pragma: no cover
    result = AsyncResult(task_id, app=celery_app)
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


def get_data_from_celery():
    return _get_from_celery(CELERY_TASK_ID)


def get_fields_from_celery():
    return _get_from_celery('fields-{}'.format(CELERY_TASK_ID))
