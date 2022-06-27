#!/bin/sh


function exit_handler()
{
    echo "Shutting down"
    docker compose logs -t >> docker.logs
    # docker compose down
    shutdown now
    exit 0
}

trap exit_handler SIGINT
trap exit_handler SIGHUP

echo "Challenge starting....please wait"
# make sure docker is up?!?!
sudo systemctl start docker.service 
#
docker compose up -d > /dev/null 2>&1

echo "Wait 10 sec for services to start completely"
sleep 10

curl -u admin:spacemath \
  "http://127.0.0.1:3000/api/alertmanager/grafana/config/api/v1/alerts" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d @configure_contact_points.json \
  > /dev/null 2>&1

echo "Connect to $SERVICE_HOST:$SERVICE_PORT in your browser."

# docker compose up -d groundstation > /dev/null 2>&1
docker compose logs -f groundstation
echo "DONE"
docker compose down