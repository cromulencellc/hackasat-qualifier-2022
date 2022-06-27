#!/bin/sh
rm flag.txt

# create the flag file
echo "$FLAG" >> flag.txt

### use gnuradio to generate the iq file
python3 path_effects.py