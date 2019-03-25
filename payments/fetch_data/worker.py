"""
By Amir Mofakhar <amir@mofakhar.info>
"""
# pragma: no cover
import os
from celery import Celery

from payments import settings

import logging

_LOG = logging.getLogger()

celery_app = Celery(__name__)

_LOG.info('---')

if not os.getenv('PAYMENTS_TESTING_MODE'):
    broker_url = os.getenv('CELERY_BROKER_URL', 'filesystem://')
    broker_dir = os.getenv('CELERY_BROKER_FOLDER', settings.CELERY_BROKER_FOLDER)

    backend_dir = os.getenv('CELERY_BACKEND_FOLDER', settings.CELERY_BACKEND_FOLDER)

    for folder in ['out', 'processed']:
        if not os.path.exists(os.path.join(broker_dir, folder)):
            os.makedirs(os.path.join(broker_dir, folder))

    backend_abs = os.path.abspath(backend_dir)
    if not os.path.exists(backend_abs):
        os.makedirs(backend_abs)

    celery_app.conf.update({
        'broker_url': broker_url,
        'broker_transport_options': {
            'data_folder_in': os.path.join(broker_dir, 'out'),
            'data_folder_out': os.path.join(broker_dir, 'out'),
            'data_folder_processed': os.path.join(broker_dir, 'processed')
        },
        'imports': ('payments.fetch_data.tasks',),
        'result_persistent': True,
        'task_serializer': 'json',
        'result_serializer': 'json',
        'result_backend': 'file://{}'.format(backend_abs),
        'task_ignore_result': False,
        'accept_content': ['json']})

