#!/usr/bin/env python3

from pwn import *
import collections
import os
import random
import json
import sys

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

def solve(r):
    with open("lol.json", "r") as f:
        l = json.load(f)
    
    g_s = b"Guess: "
    r.recvline()
    lookup = l

    guess = random.randint(1,0xFF)
    guess = f"{guess}".encode()

    r.sendline(guess)
    while True:
        print(guess)

        rec = r.recvline().strip(b"\n").split(b" ")[-1].decode()
        print(rec)
        try:
            ll = int(rec)
        except ValueError as e:
            break

        if ll in lookup:
            if int(guess.decode()) not in lookup[ll]:
                lookup[ll].append(int(guess.decode()))
        else:
            lookup[ll] = [int(guess.decode())]
        
        if ll == 1:
            guess = 0xff
        elif ll-1 not in lookup:
            guess = random.randint(1,0xFF)
        else:
            guess = random.choice(lookup[ll-1])
        
        guess = f"{guess}".encode()
        r.sendline(guess)
    
    with open("lol.json", "w") as f:
        lookup = json.dump(lookup, f)
    
    exit()
    

if __name__=="__main__":
    host, port, config_port = os.getenv("CHAL_HOST", "172.17.0.1"), int(os.getenv("CHAL_PORT", 31337)), int(os.getenv("CONFIG_PORT", 8001))
    
    r = remote(host,port)

    r = process("./chal.py")

    submit_ticket(r)

    if (flag := solve(r)):
        p(f"Solved! Got flag: {flag}")
    else:
        p("Did not solve.")

    r.close()
