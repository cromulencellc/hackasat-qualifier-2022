#!/usr/bin/env python3

import requests
import subprocess

from binascii import hexlify,unhexlify
from pwn import *

PATCHFILE = "solve.patch"
STATIC_NAME = "Lander"

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
    filename = f"{STATIC_NAME}_patched"

    r.recvuntil(b"Upload binary at: ")
    address = r.recvline().strip(b"\n").decode()

    p(f"Patching binary {STATIC_NAME}")

    s = subprocess.Popen(["bspatch", STATIC_NAME, filename, PATCHFILE])
    if (ret_code := s.wait(5)) != 0:
        p(f"Binary patch failed. Got ret: {ret_code}. Bailing out...")
        exit(-1)

    url = "http://" + address + "/upload"
    data = {'name': 'file', 'filename': filename}
    files = {'file': (filename, open(filename, "rb"))}
    req = requests.post(url, data=data, files=files)

    if b"File uploaded" not in req.content:
        p(b"File did not upload correctly. Received: {req.content}. Bailing out...")
        exit(-1)
    
    p("File uploaded successfully. Waiting for simulation...")

    r.recvuntil(b"flag:\n", timeout=30)

    flag_resp = r.recvline()

    if b"flag" in flag_resp:
        return flag_resp[flag_resp.find(b"flag"):].strip(b"\n").decode()
    
    return ""

if __name__=="__main__":
    host, port = os.getenv("CHAL_HOST", "172.17.0.1"), int(os.getenv("CHAL_PORT", 3000))
    
    
    r = remote(host,port)

    submit_ticket(r)

    if (flag := solve(r)):
        p(f"Solved! Got flag: {flag}")
    else:
        p("Did not solve.")

    r.close()
