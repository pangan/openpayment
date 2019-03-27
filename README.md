# payments

This service fetches payments data and lets the user to search on any 
field and download the result as a XLS file. 

## Settings

## How to run it

### Docker

Just run the below command:

    `docker-compose up`

It will create the image and runs all the services in docker.
Check the screen until it runs the celery worker and be ready. 
If celery worker is not ready yet, it will show `Celery not ready!` just wait
and let it to be connected.
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

    `celery worker --app=payments.fetch_data.tasks --concurrency=1 --loglevel=INFO -B`

* Run the application in another thread by any of below commands:

    * `./run_api.sh`
    
    or
    * `python -m payments.dev_run`
    
    or
    * `gunicorn -b0.0.0.0:5000 --reload -w1 payments.app:api`

* You can access the application by port 5000:

    `http://localhost:5000`
    
## Unit tests 

`nosetests -v tests --with-coverage --cover-package payments --cover-min-percentage=100`