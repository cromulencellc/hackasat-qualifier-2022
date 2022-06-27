#!/usr/bin/env python3

from binascii import hexlify,unhexlify
from cmd import PROMPT
from pwn import *

MAX_MSG_SIZE = 256

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

def count_zeros_xor(msg_l, encoded_msg_l):
    total_zeros = 0

    for msg_num, encoded_num in zip(msg_l, encoded_msg_l):
        if (msg_num ^ encoded_num) == 0: total_zeros += 1
    
    return total_zeros

def solve(r):
    PROMPT = b"Msg: "
    r.recvuntil(b"Encoded msg is: ")
    encoded_msg = unhexlify(r.recvline().strip(b"\n"))
    encoded_msg_l = list(encoded_msg)

    for msg_size in range(1, MAX_MSG_SIZE):
        r.recvuntil(PROMPT)

        msg = b'FF'*msg_size

        r.sendline(msg)

        encode_guess_ones = unhexlify(r.recvline().strip(b"\n"))

        encode_guess_ones_l = list(encode_guess_ones)
        cnt = count_zeros_xor(encode_guess_ones_l, encoded_msg_l)

        if cnt >= (MAX_MSG_SIZE - msg_size):
            break

    p(f"Got Matches:{cnt} | Size: {msg_size}")

    r.recvuntil(PROMPT)

    new_msg = []
    sol = set(range(1,msg_size+1))
    sol.add(255)

    for i in range(1,msg_size+1):
        new_msg.append(f"{i:02x}")
    new_msg = "".join(new_msg).encode()

    r.sendline(new_msg)

    num = unhexlify(r.recvline().strip(b"\n"))

    num_l = list(num)

    guess = list()

    for i,j in zip(num_l, encode_guess_ones_l):
        guess.append(i^j^0xFF)
    
    if(set(guess) == sol):
        pass
        # print("yay")

    transpose = [0] * msg_size
    for idx in range(1,msg_size+1):
        transpose[idx-1] = guess.index(idx)
    unencoded = [255] * msg_size

    for ind in range(msg_size):
        unencoded[ind] ^= encoded_msg_l[transpose[ind]]
        unencoded[ind] ^= encode_guess_ones_l[transpose[ind]]

    answer = hexlify(bytes(unencoded))

    r.recvuntil(PROMPT)
    r.sendline(answer)
    r.recvline()

    flag_resp = r.recvline(timeout=2)

    if b"flag" in flag_resp:
        return flag_resp[flag_resp.find(b"flag"):].strip(b"\n").decode()
    
    return ""

if __name__=="__main__":
    host, port, config_port = os.getenv("CHAL_HOST", "172.17.0.1"), int(os.getenv("CHAL_PORT", 31337)), int(os.getenv("CONFIG_PORT", 8001))
    
    r = remote(host,port)

    submit_ticket(r)

    if (flag := solve(r)):
        p(f"Solved! Got flag: {flag}")
    else:
        p("Did not solve.")

    r.close()
