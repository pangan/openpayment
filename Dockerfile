FROM python:3

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./payments /reorg/payments

COPY entrypoint.sh /reorg/

WORKDIR /reorg

RUN chmod +x entrypoint.sh
