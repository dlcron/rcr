#!/bin/sh

gunicorn -w 1 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 rcr.api:app