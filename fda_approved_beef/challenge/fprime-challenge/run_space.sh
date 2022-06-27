echo "Starting spacecraft"
cd /home/space/fsw/
echo "${FLAG}" > /home/space/fsw/.FlagData
unset FLAG
sleep 15
./satellite.exe -a 172.16.238.3 -p 50000
