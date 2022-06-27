#!/bin/bash

function exit_handler()
{
    echo "Shutting down"
    docker compose logs -t > docker.logs
    docker compose down
    shutdown now
    exit 0
}

trap exit_handler SIGINT

echo "Now with 2022 more F-Prime"
echo "Challenge Web Page Starting at http://${WEB_IP}:${WEB_PORT}"
echo "CLI available at ${GDS_IP}:${GDS_PORT}"

timeRemaining=${TIMEOUT:-900}
while [ ${timeRemaining} -gt 0 ]; do
    if [ $((timeRemaining % 60)) -eq 0 ]; then
        echo "Time remaining to solve: ${timeRemaining} seconds"
    fi
 
    timeRemaining=$((timeRemaining - 1))
    sleep 1
done
echo "Time is up. Try again with new ticket...."
stop_container
exit 0