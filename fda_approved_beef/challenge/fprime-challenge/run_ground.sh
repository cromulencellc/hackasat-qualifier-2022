
#!/bin/bash
echo "Starting ground station"
cd /home/ground/ground-system
VIRTUAL_ENV=/home/ground/ground-system/fprime-venv
export PATH="$VIRTUAL_ENV/bin:$PATH"
fprime-gds -n --dictionary dict/RefTopologyAppDictionary.xml --gui-addr 0.0.0.0 --tts-port 5001
# fprime-gds -n --dictionary dict/RefTopologyAppDictionary.xml --gui-addr 0.0.0.0