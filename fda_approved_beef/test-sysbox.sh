
#!/usr/bin/bash

CHAL_HOST=$1
CHAL_PORT=$2
WEB_PORT=$3
CLI_PORT=$4
FLAG=$5
TIMEOUT=$6

echo "Running with ${CHAL_HOST}, Chal Ports: ${CHAL_PORT}, ${WEB_PORT}, ${CLI_PORT} with FLAG: ${FLAG}"
container_name=$(docker run -d --rm -p ${WEB_PORT}:5000 -p ${CLI_PORT}:5001 -e SERVICE_HOST=${CHAL_HOST} -e SERVICE_PORT=${WEB_PORT} -e FLAG=${FLAG} -e TIMEOUT=${TIMEOUT} registry.mlb.cromulence.com/has3/quals/challenges/fprime-exploitation/fprime-exploitation\:challenge)
echo "Sysbox container started challenge ready"
# docker exec -i ${container_name} '/bin/bash' '/challenge/run.sh'
# echo "Challenge Started. nc ${CHAL_HOST} ${CHAL_PORT}"
socat -v tcp-listen:${CHAL_PORT},reuseaddr exec:"docker exec -i ${container_name} '/bin/bash' '/challenge/run.sh'" > log2>&1 &
echo "Challenge Started: ${CHAL_HOST}:${CHAL_PORT}"
echo "Run solver"
docker run --runtime=runc -it --rm -e CHAL_HOST=${CHAL_HOST} -e CHAL_PORT=${CHAL_PORT} --net=host registry.mlb.cromulence.com/has3/quals/challenges/fprime-exploitation/fprime-exploitation:solver
# pkill socat