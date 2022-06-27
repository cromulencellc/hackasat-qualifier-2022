#!/bin/sh

echo ${FLAG} > /app/flag/flag.txt

# Start the screaming fist service
/usr/local/bin/python /app/screamingfist.py ${SERVICE_HOST} ${SERVICE_PORT}