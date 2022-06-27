# Hello World Solver
import os
import sys
import socket

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
    print(f"Connect to {host}:{port}", flush=True)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
   
    # pass ticket to ticket-taker
    if ticket:
        prompt = s.recv(128)  # "Ticket please:"
        s.send((ticket + "\n").encode("utf-8"))

    # receive challenge
    challenge = s.recv(256)
    challenge = challenge.decode('UTF-8')
    print(challenge,end='', flush=True)

    # provide response
    response = '72,65,67,75,65,83,65,84,51\n'
    print(response, flush=True)
    s.send(response.encode("utf-8"))
    
    response = '-701,140,773,-726,149,791,-654,134,721\n'
    print(response, flush=True)
    s.send(response.encode("utf-8"))

    # receive and print flag
    i = 0
    while (i <4):
        r = s.recv(256)
        print(r.decode('utf-8'),end='', flush=True)
        i = i+1