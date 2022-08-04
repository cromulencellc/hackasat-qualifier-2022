#!/bin/bash
cd /challenge/
cd viewer
npm start > npmlog.txt&
cd /challenge
python3 challenge.py

if [ -z $TIMEOUT ]; then
    echo "Trajectory viewer up for 300s "
    sleep 300
else
    echo "Trajectory viewer up for $TIMEOUTs"
    sleep $TIMEOUT
fi


