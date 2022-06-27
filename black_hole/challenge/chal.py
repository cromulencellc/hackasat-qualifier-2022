#!/usr/bin/env python3

import binascii
import numpy as np
import os
import random
import secrets
import sys

from collections import defaultdict

# Local imports
from libs.timeout import timeout, TimeoutError, MINUTE

MSG_SIZE = 256
LOWER_RANDOM_MSG_SIZE = int(MSG_SIZE * 0.55)
UPPER_RANDOM_MSG_SIZE = int(LOWER_RANDOM_MSG_SIZE * 0.37) + LOWER_RANDOM_MSG_SIZE
NUM_OF_BYTES_GUESSES = UPPER_RANDOM_MSG_SIZE*(UPPER_RANDOM_MSG_SIZE+1) // 2 + 3*UPPER_RANDOM_MSG_SIZE

# Challenge enviroment variables
FLAG = os.getenv("FLAG", "flag{0bscur3!s3cur3}")
TO = int(os.getenv("TIMEOUT", 5 * MINUTE))

# Print properly in docker/socket env
def p(s, end="\n", flush=True):
    sys.stdout.write(f"{s}{end}")
    if flush: sys.stdout.flush() 

class BlackHole():
    def __init__(self):
        self.encoding = defaultdict(dict)
        self.create_transpositions()
        self.create_random_msgs()

    def create_transpositions(self):
        for num_len in range(1,MSG_SIZE+1):
            perm = np.random.permutation(MSG_SIZE)
            self.encoding[num_len]["trans"] = list(perm[:num_len])

    def create_random_msgs(self):
        for num_len in range(1,MSG_SIZE+1):
            self.encoding[num_len]['encode'] = b'\x00'
            while(b'\x00' in self.encoding[num_len]['encode']):
                self.encoding[num_len]['encode'] = secrets.token_bytes(MSG_SIZE)

    def encode_msg(self, msg):
        msg_nums, msg_len = list(msg), len(msg)

        encoded_msg = list(self.encoding[msg_len]["encode"])

        for idx, num in enumerate(msg_nums):
            encoded_msg[self.encoding[msg_len]["trans"][idx]] ^= num
        
        assert len(encoded_msg) == MSG_SIZE

        return bytes(encoded_msg)

@timeout(TO)
def challenge(bh):
    success = False

    rnd_msg_size = random.randint(LOWER_RANDOM_MSG_SIZE, UPPER_RANDOM_MSG_SIZE)
    while(b'\x00' in (random_msg := secrets.token_bytes(rnd_msg_size))): continue

    random_msg = bh.encode_msg(random_msg)

    p(f"Encoded msg is: {binascii.hexlify(random_msg).decode()}")
    p(f"We can stream {NUM_OF_BYTES_GUESSES} bytes of data before the sat kills the connection. Please help. (Send your message in hex.)")

    def p_err_and_sub(err_msg):
        nonlocal bytes_left
        p(err_msg)
        bytes_left -= l_len

    bytes_left = NUM_OF_BYTES_GUESSES
    while bytes_left > 0 and not success:
        p(f"({bytes_left}) Msg: ", end="")
        line = sys.stdin.readline()
        
        line = line.replace("\n","")

        l_len = len(line)
        bytes_left -= (l_len // 2)
        if l_len % 2 == 1:
            p("Must provide even-length string")
            continue
        elif l_len > 2*(MSG_SIZE-1):
            p(f"Size of msg cannot be greater than {MSG_SIZE-1}")
            continue
        elif l_len == 0:
            p(f"Size of msg must be greater than 0")
            continue
        elif bytes_left < 0:
            bytes_left += (l_len // 2)
            p(f"Msg too large, you only have {bytes_left} bytes left...")
            continue

        # Check to make sure that the message doesn't contain "00" on a byte alignment
        for b_idx in range(0, len(line)-2, 2):
            if "00" == line[b_idx:b_idx+2]:
                p("Must provide message with no NULL bytes (00)")
                continue
        
        try:
            msg = binascii.unhexlify(line)
        except binascii.Error as e:
            if str(e) == "Odd-length string":
                p("Must provide even-length string")
                continue
                # exit(-1)
            elif str(e) == "Non-hexadecimal digit found":
                p("Must provide hexadecimal digits only")
                continue
                # exit(-1)
            continue
                
        encoded_msg = bh.encode_msg(msg)
        encoded_msg_hex = binascii.hexlify(encoded_msg).decode()

        p(encoded_msg_hex)

        if encoded_msg == random_msg:
            p(f"Satellite-link synced! Flag: {FLAG}")
            exit(0)

    return success

if __name__ == "__main__":
    p("Generating black hole...\n")
    bh = BlackHole()

    sys.stdin.flush()

    try:
        success = challenge(bh)
    except TimeoutError:
        p("\nTimeout, Bye")
        sys.exit(1)

    if not success:
        p("You ran out of data to send! Bye.")