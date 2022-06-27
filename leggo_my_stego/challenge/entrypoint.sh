#!/bin/sh

# Start the leggo stego service
/usr/local/bin/python /app/leggostego.py -s

# /usr/local/bin/python /app/leggostego.py -v -a ${SERVICE_HOST} -p ${SERVICE_PORT} &

# Point users to the right port
# echo "Please connect to the satellite imaging system at $SERVICE_HOST:$SERVICE_PORT"
# if [ -z ${TIMEOUT} ]; then
#     echo "You have 600 seconds."
#     sleep 600
# else
#     echo "You have ${TIMEOUT} seconds."
#     sleep ${TIMEOUT}
# fi