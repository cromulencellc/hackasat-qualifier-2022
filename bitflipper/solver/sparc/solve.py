#!/usr/bin/env python3

from pwn import *
import collections
import os
import random
import json
import sys

# Local imports
from gen import Gen

BITS = 16
LEVEL = b"level"
PROMPT = b"Guess: "

# Print properly in docker/socket env
def p(s, end="\n", flush=True):
    sys.stdout.write(f"{s}{end}")
    if flush: sys.stdout.flush()

def submit_ticket(r):
    ticket = os.getenv("TICKET")

    if ticket:
        r.recvuntil("Ticket please:")
        r.sendline(ticket.encode())
        p("Sent ticket")

def find_level(line):
    if LEVEL in (l_l := line.lower()):
        lvl_idx = l_l.index(LEVEL)+len(LEVEL)+1
        level = chr(l_l[lvl_idx])

        return level
    
    return 0

def solve(r,lookup):
    n = lambda num: str(lookup[num]).encode()

    hint_num = 17

    line = r.recvuntil(PROMPT).lower()

    if LEVEL in line:
        p(f"On level: {find_level(line)}")

    r.sendline(n(BITS))

    count = 0
    while count < 100:
        line = r.recvline()
        if b"flag" in line:
            l = line.decode()
            flag_idx = l.index("flag")
            return l[flag_idx:]
        line = line.lower()
        if LEVEL in line:
            p(f"On level: {find_level(line)}")
            r.recvuntil(PROMPT)
            r.sendline(n(BITS))
        elif b"completed" in line:
            continue
        else:
            try:
                hint = line.strip(b"\n").split(b" ")[-1].decode()
                hint_num = int(hint)
            except ValueError as e:
                p(f"Did not get a number. Got: {hint} instead. Bailing out...")
                exit(-1)
        
            guess = n(hint_num)

            r.sendline(guess)
        
        count += 1

if __name__=="__main__":
    host, port, config_port = os.getenv("CHAL_HOST", "172.17.0.1"), int(os.getenv("CHAL_PORT", 31337)), int(os.getenv("CONFIG_PORT", 8001))
    
    g = Gen(BITS)

    r = remote(host,port)

    # r = process("./chal.py")

    submit_ticket(r)

    if (flag := solve(r,g.lookup_by_diff)):
        p(f"Solved! Got flag: {flag}")
    else:
        p("Did not solve.")

    r.close()
