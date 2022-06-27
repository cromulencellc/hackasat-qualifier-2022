import os
import sys
import socket
import subprocess
from time import sleep

def calculate_route():
    # Run once_unop_a_dijkstar and get the output. Split by the new lines and strip off first and last elements (non-Starlunk satellites).
    sats = subprocess.check_output("/solver/test.sh").decode("utf-8").split("\n")[1:-2]

    # Strip off the "Starlunk-" part of the name and the trailing '"'
    result = []
    for sat in sats:
        result.append(sat.split("Starlunk-")[1][:-1])

    return ", ".join(result)

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
        sleep(1)
        prompt = s.recv(128)  # "Ticket please:"
        s.send((ticket + "\n").encode("utf-8"))

    print()

    # receive challenge
    i = 0
    while i < 16:
        challenge = s.recv(64)
        challenge = challenge.decode('UTF-8')
        print(challenge,end='')
        i += 1

    challenge = s.recv(1024)
    challenge = challenge.decode('UTF-8')
    print(challenge,end='')

    sleep(1)
   
    # send answer
    answer = calculate_route()
    print(f"Sending: {answer}")
    s.send(f"{answer}\n".encode('utf-8'))

    # get flag
    result = s.recv(256)
    print(result.decode("utf-8"))

    print()