"""
By Amir Mofakhar <amir@mofakhar.info>
"""
OPEN_PAYMENTS_API_ENDPOINT = 'https://openpaymentsdata.cms.gov/resource/8pru-svmk.json'
FETCHING_DATA_PERIOD_SECOND = 3600

CELERY_BROKER_FOLDER = '/var/lib/payments/broker'
CELERY_BACKEND_FOLDER = '/var/lib/payments/backend'
CELERY_TASK_ID = '122'
