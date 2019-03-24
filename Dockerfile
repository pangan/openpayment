FROM python:3

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./payments /reorg/payments

COPY *.sh /reorg/

WORKDIR /reorg

RUN chmod +x run_all_services.sh run_api.sh run_celery_worker.sh
