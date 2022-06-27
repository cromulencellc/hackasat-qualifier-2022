# Hello World Solver
import os
import sys
sys.path.append(os.getcwd())
from pwnlib.tubes.remote import remote
from base64 import b64encode
import json

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
    s = remote(host, port)

    # pass ticket to ticket-taker
    if ticket:
        prompt = s.recvlineS()  # "Ticket please:"
        s.send((ticket + "\n").encode("utf-8"))

    hint_file = open('hints.json', 'rt')
    hints = json.load(hint_file)
    hint_file.close()

    # receive challenge
    challenge_line = s.recvlineS()
    print(challenge_line)
    challenge_line = s.recvlineS()
    print(challenge_line)
    challenge_line = s.recvlineS()
    print(challenge_line)
    [challenge, shasum] = challenge_line.split("\t")
    
    hint = hints[challenge]
    hint['sha256'] = hint['sha256'].strip('\n')
    shasum = shasum.strip("\n")
    if not hint:
        print("didn't have hint for challenge {} with shasum {}".format(challenge, shasum) )
        raise ValueError
    if (hint['sha256'] != shasum):
        print("challenge {} gave shasum:\n{}\n but hint file gave\n{}".format(challenge, shasum, hint['sha256']) )
        raise ValueError

    answer = hints[challenge]['answer']
    print("Need to input: {}".format( answer ))
    # provide response
    response = b64encode(answer.encode('utf-8'))
    print("Thats b64: {}".format(response))
    s.send(response + b"\n")

    # receive and print flag
    print(s.recvrepeatS())
