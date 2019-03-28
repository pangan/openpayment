# payments

This service fetches payments data and lets the user to search on any 
field and download the result as a XLS file.

* File system is used for Celery to make the application more simple.
 It is possible to use RabbitMQ or Redis in production.
  
## Settings
`payments/settings.py` is used for application settings :

```
# URL for fetching payments data
OPEN_PAYMENTS_API_ENDPOINT = 'https://openpaymentsdata.cms.gov/resource/8pru-svmk.json'

# Period for fetching and updating payments data
FETCHING_DATA_PERIOD_SECOND = 3600

# Make sure the path for broker and backend exist and user has write permission.
CELERY_BROKER_FOLDER = '/var/lib/payments/broker'
CELERY_BACKEND_FOLDER = '/var/lib/payments/backend'

# Celery task ID, no need to change it!
CELERY_TASK_ID = '122'
```

## How to run it

### Docker

Just run the below command:

   `docker-compose up`

It will create the image and runs all the services in docker.
Check the screen until it runs the celery worker and be ready. 
After celery worker runs and fetches the data you can access
the application by port 8000:

`http://localhost:8000` 

### Running on your machine

* Make a python 3.7 virtual environment:

    `virtualenv .venv`

* Active the virtual environment:

    `source .venv/bin/activate`

*  Install the requirements:

    `pip install -r requirements.txt -r test_requirements.txt`

* Run celery worker by below command or `run_celery_worker.sh`

    `celery worker --app=payments.fetch_data.tasks --loglevel=INFO -B`

* Run the application in another thread by any one of the below commands:

    * `python -m payments.dev_run`
    
    or
    * `gunicorn -b0.0.0.0:5000 --reload -w1 payments.app:api`

* You can access the application by port 5000:

    `http://localhost:5000`
    
## Tests 

### Unit tests

Run below command for unit tests:
 
    `nosetests -v tests --with-coverage --cover-package payments --cover-min-percentage=100`
    
### pep8

Run below command for pep8 checking:

    `flake8 --max-line-length=99 payments`
