#!/bin/bash
gunicorn -b0.0.0.0:5000 --reload -w1 payments.app:api
