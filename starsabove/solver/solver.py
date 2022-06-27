# Hello World Solver
import os
import sys
import socket
import re

if __name__ == "__main__":
    # get host from environment
    host = os.getenv("CHAL_HOST")
    if not host:
        print("No HOST supplied from environment")
        sys.exit(-1)

    # get port from environment
    port = int(os.getenv("CHAL_PORT","0"))
    if port == 0:
        print("No PORT supplied from environment")
        sys.exit(-1)

    # get ticket from environment
    ticket = os.getenv("TICKET")

    # connect to service
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
   
    # pass ticket to ticket-taker
    if ticket:
        prompt = s.recv(128)  # "Ticket please:"
        s.send((ticket + "\n").encode("utf-8"))
    
    # receive startup messages
    challenge = s.recv(256)

    msgs = [ 
        "050002000000000000001e0005000500000000001e00",
        "050004000000000000001e000000140003000500000000000400",
        "050003000000000000001e00000014000500000000000300",
        "0500010000000000000004000500000000000500",
        "050004000000000000001e0000001400020003000000"
    ]
    with open("/solver/solution.txt", 'r') as f:
        for msg in f.readlines():
            s.send((msg).encode("utf-8"))
    
    # receive and print flag
    resp = ""
    while True:
        r = s.recv(512).decode('utf-8')
        print(r, end='')
        sys.stdout.flush()
        resp += r
        if re.search(r"flag\{.+\}", r, re.IGNORECASE) is not None: 
            break

