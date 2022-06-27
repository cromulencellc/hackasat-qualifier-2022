#!/bin/bash

echo "Build QualsRef Deployment"
flag=$1

if [ -d build-fprime-automatic-native ]; then
    rm -rf build-fprime-automatic-native
fi

if [ -d build-artifacts ]; then
    rm -rf build-artifacts
fi

# echo "Update toolchain file"
# cp challenge.cmake /home/has/fprime/fprime/cmake/toolchain/challenge.cmake

echo "Cleanup to good state prior to build"
fprime-util purge -f

# if [ -z "${FLAG_PASSCODE}" ]; then
#     passcode=$(python3 genpasscode.py)
#     # passcode="123456_654321_qwerty"
#     echo "Set FlagPasscode to ${passcode}"
#     export FLAG_PASSCODE=${passcode}
#     if grep "FLAG_PASSCODE" env.ini; then
#         echo "Update existing env.ini"
#         sed -i "s/\(FLAG_PASSCODE=\).*/\1YD0WLPJRZ5MWEWEG/" env.ini
#     else
#         echo "Add FLAG_PASSCODE to env.ini"
#         echo "FLAG_PASSCODE=${passcode}" >> env.ini
#     fi
# fi

echo "Generate fprime build cache"
fprime-util generate

echo "Run Build"
fprime-util build

# echo "Write FlagData to file .FlagData"
flagData=${FLAG:-flag{test123test123987654321qwertyuiopasdfghjkl1234567890abcdefghijklmnopqrstuvwxyz0123456789}}
echo "Create and set perms on FlagData File"
echo "${flagData}" > FlagData.txt
chmod 600 FlagData.txt

echo "Copy runtime files to bin folder"
cp FlagData.txt build-artifacts/Linux/bin/.FlagData
cp attempt.txt build-artifacts/Linux/bin/

echo "Update executable name"
mv build-artifacts/Linux/bin/QualsRef build-artifacts/Linux/bin/satellite.exe

if [ $? -eq 0 ]; then
    echo "Complete. FLAG: ${flagData}"
else
    echo "Build Failed"
fi