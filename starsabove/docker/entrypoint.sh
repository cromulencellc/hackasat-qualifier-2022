#!/bin/bash

(gosu server /src/server) &
(gosu client2 /src/client 2 8) &
(gosu client8 /src/client 8 8) &
env -i DOWNLINK=1 /usr/sbin/gosu client /src/client 5 8