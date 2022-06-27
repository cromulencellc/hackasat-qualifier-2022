#!/bin/bash

sh -c 'sleep 300 && echo "\nTimeout, Bye" && kill -s TERM 1' &
qemu-sparc32plus -E FLAG=${FLAG} -E SEED=$(python3 -c "import secrets;print(secrets.randbelow(2**32))") /challenge/bitflipper