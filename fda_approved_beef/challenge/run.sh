#!/bin/bash

function exit_handler()
{
    echo "Shutting down"
    docker compose logs -t >> docker.logs
    # docker compose down
    shutdown now
    exit 0
}

cd /challenge

BASE_IP=${SERVICE_HOST:-localhost}
BASE_PORT=${SERVICE_PORT:-5000}

WEB_IP=${BASE_IP}
WEB_PORT=${BASE_PORT}
GDS_IP=${BASE_IP}
GDS_PORT=$((BASE_PORT + 1))

export WEB_IP=${WEB_IP}
export WEB_PORT=${WEB_PORT}
export GDS_IP=${GDS_IP}
export GDS_PORT=${GDS_PORT}


# echo "Start docker service"

systemctl start docker.service 

# echo "Wait for Docker to start "
echo "Wait for system to initialized"
sleep 5
compose_capture=$(docker compose up -d 2>&1)
sleep 5
echo ${compose_capture} >> docker.logs

trap exit_handler SIGINT
trap exit_handler SIGHUP

echo "Challenge Web Page Starting at http://${WEB_IP}:${WEB_PORT}"
echo "CLI available at ${GDS_IP}:${GDS_PORT}"
echo "Now F'DA Approved Beef"
echo "Get the system to return flag in telemetry to win"

timeRemaining=${TIMEOUT:-900}
while [ ${timeRemaining} -gt 0 ]; do
    if [ $((timeRemaining % 60)) -eq 0 ]; then
        echo "Time remaining to solve: ${timeRemaining} seconds"
    fi
    timeRemaining=$((timeRemaining - 1))
    sleep 1
done
echo "Time is up. Try again with new ticket...."
exit_handler
exit 0

# tail -f /tmp/ground.log
