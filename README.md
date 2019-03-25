# payments

## What is it
What does the service do
## Who wants it
Who is the consumer of this service
## How to run it
`docker-compose up`

`celery worker --app=payments.fetch_data.tasks --concurrency=1 --loglevel=INFO -B`
## Unit tests 

`nosetests -v tests --with-coverage --cover-package payments --cover-min-percentage=100`