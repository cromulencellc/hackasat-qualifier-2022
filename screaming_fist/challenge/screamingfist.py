#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import re
import subprocess
import argparse
from random import randrange
from itertools import cycle
from base64 import b64decode
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad, unpad
from socketserver import StreamRequestHandler, ThreadingTCPServer
import os

CODING = 'UTF-8'


class DummyResponses:
    def __init__(self):
        self.dummy_cmds = [
            'mem_list',
            'mem_reg',
            'mem_read',
            'mem_write',
            'mem_free',
            'app_list',
            'app_start',
            'app_stop',
            'app_del',
            'app_cmd'
        ]

    def is_dummy_cmd(self, cmd: str):
        for dummy_cmd in self.dummy_cmds:
            if dummy_cmd in cmd:
                return True
        return False

    @staticmethod
    def telemetry() -> bytes:
        telemetry = """+-------------------------------------------------------------------------------------+
|        Payload        |  T  |    Wattage   |    Bus ID     |      Memory      | CPU | 
|-------------------------------------------------------------------------------------|
|   GPS Omni. Proc. 1   | {t1}C |     {w1}W     | 10000-61-0110 |   {m1}/2048MiB   | {p1}% |
|   GPS Omni. Proc. 2   | {t2}C |     {w2}W     | 10000-43-0110 |   {m2}/2048MiB   | {p2}% | 
|    GPS Uni. Proc. 1   | {t3}C |     {w3}W     | 10000-42-4542 |   {m3}/2048MiB   | {p3}% |
|        "METAL"        | {t4}C |     {w4}W     | 10000-56-1677 |   {m4}/8192MiB   | {p4}% |
|        "BRICK"        | {t5}C |     {w5}W     | 10000-92-0740 |   {m5}/8192MiB   | {p5}% |
|   BLACK ICE "ALICE"   | 99C |  [REDACTED]  |  [REDACTED]   | 5.1e+7/5.2e+7MiB | 99% |
+-------------------------------------------------------------------------------------+""" \
            .format(t1=str(randrange(71, 76)), t2=str(randrange(71, 76)), t3=str(randrange(82, 90)),
                    t4=str(randrange(82, 90)), t5=str(randrange(62, 69)),
                    m1=str(randrange(1412, 1489)), m2=str(randrange(1801, 1898)), m3=str(randrange(1987, 2047)),
                    m4=str(randrange(8102, 8190)), m5=str(randrange(8102, 8190)),
                    p1=str(randrange(41, 56)), p2=str(randrange(41, 56)), p3=str(randrange(81, 100)),
                    p4=str(randrange(81, 100)), p5=str(randrange(65, 72)),
                    w1=str(randrange(100, 122)), w2=str(randrange(100, 122)), w3=str(randrange(180, 200)),
                    w4=str(randrange(180, 200)), w5=str(randrange(180, 200)))

        return telemetry.encode(CODING) + b'\n'

    @staticmethod
    def gibberish() -> bytes:
        gibberish_length = (randrange(200, 3000))
        return get_random_bytes(gibberish_length)

    @staticmethod
    def border(data: list):
        data = [line.strip() for line in data]
        line_max = max(len(longest_bytes) for longest_bytes in data)
        top_and_bottom = b'+' + b'-' * (line_max + 2) + b'+\n'
        start = b'| '
        end = b' |\n'

        bordered_data = top_and_bottom

        for line in data:
            if line:  # If the line object isn't empty, add it to the formatted output
                # The reason why we are decoding and encoding is that we want to use the "true" length in Russian, and
                # not the line length in raw format.
                if len(line.decode(CODING)) < line_max:
                    spaces = " " * (line_max - len(line.decode(CODING)))
                    line = (line.decode(CODING) + spaces).encode(CODING)
                bordered_data += start + line + end
        bordered_data += top_and_bottom
        return bordered_data


class SpaceVehicleSimulator:
    def __init__(self):
        self.aes_key = bytes.fromhex('667E23029E4C4BD46E3863429F2B53A9')
        self.cbc_mac_keys = [
            bytes.fromhex('DBF7464C02A2C97DDD0438A167BF3F21'),  # Key 0; used for all log_[something] cmds
            bytes.fromhex('78BEDFB09D794FFC1C8B9AC34E16C601'),  # Key 1; used for all mem_[something] cmds
            bytes.fromhex('92DCEFD3D4ABAFE01F5B12D71D737D6D'),  # Key 2; used for all app_[something] cmds
            bytes.fromhex('38746F66D25874A67FBFB9FB0F248F1B'),  # Key 3; revealed in intel doc
        ]
        self.macs = [
            bytes.fromhex('55D0861A0B838272AC41447142725EBA'),  # log_info
            bytes.fromhex('87AA8B944D3FD46855D0B88F393564B9'),  # log_warn
            bytes.fromhex('E690BF761526072A995A2D499AA36436'),  # log_query
            bytes.fromhex('5C2F1078C86AD55F0D4376DA4F044863'),  # mem_list
            bytes.fromhex('799EBB43CC375584D456B5115D68F494'),  # mem_reg
            bytes.fromhex('33E8BDD872DD6ED2EEF43474DADCADCB'),  # mem_read
            bytes.fromhex('3A5296716F4B0F00A4A02688245F9BDA'),  # mem_write
            bytes.fromhex('456EAC5EE717E47FB2C3C017A4DC76A7'),  # mem_free
            bytes.fromhex('03A56772D2C8D5E1CFC92D6691E52B3D'),  # app_list
            bytes.fromhex('8E87F9AEC9BB56742631394561671662'),  # app_start
            bytes.fromhex('E677A014A3A7B109C869154469596E97'),  # app_stop
            bytes.fromhex('6F8FD6B7267DE70E116325155332ADA0'),  # app_del
            bytes.fromhex('D882099AA9AC241134C57FBC2D96B476'),  # app_cmd
            bytes.fromhex('119D1617B58273114880776ADB5E75AB'),  # query_payload_telemetry.
            #                                                      This is what the players must collide with.
        ]
        self.pattern = cycle(['A4', 'A1', 'A2', 'A3', 'A6', 'A9', 'A8'])
        self.logs = []
        self.dummy_responses = DummyResponses()
        self.__log_generator()

    def respond(self, recv: bytes) -> bytes:
        response: bytes = b''

        encrypted_command_list = [enc_cmd for enc_cmd in recv.split(b'\0') if enc_cmd]  # Split commands w/o empty bytes
        for encrypted_command in encrypted_command_list:
            try:
                unverified_cmd = self.__decrypt_cmd(b64decode(encrypted_command))
                response += self.verify_and_process_command(unverified_cmd)
            except ValueError:
                # This is our padding oracle :)
                response += self.dummy_responses.border(['Bad padding'.encode(CODING)])
        return response

    def verify_and_process_command(self, unverified_cmd):
        response = b''
        unverified_cmd_args = re.findall(b'{[^}]*}', unverified_cmd)
        if not unverified_cmd_args:
            response += self.dummy_responses.border(['Argument not found'.encode(CODING)])
        else:
            unverified_cmd_arg = unverified_cmd_args[0]  # Get argument before it is removed
            unverified_cmd = re.sub(b'{[^}]*}', b'', unverified_cmd)  # Strip the argument from the command
            if self.__verify_cmds(unverified_cmd):
                response += self.process_command((unverified_cmd, unverified_cmd_arg))
            else:
                # This is if the players just try to run sys_shell, which intentionally will not work as a MAC for
                # sys_shell doesn't exist. This should signal to the players to try to cause a CBC_MAC collision.
                # """Should""".
                response += self.dummy_responses.border(
                    ['The MAC is not on the approved list.'.encode(CODING)])
        return response

    def process_command(self, verified_cmd):
        response = b''

        try:
            verified_cmd = (verified_cmd[0].decode(CODING), verified_cmd[1].decode(CODING))
        except UnicodeDecodeError:
            response += self.dummy_responses.border(['Cannot decode to UTF-8'.encode(CODING)])
        else:
            cmd = verified_cmd[0]
            arg = verified_cmd[1][1:-1]  # Getting rid of brackets here.
            if 'log_info' in cmd:
                self.logs.append(b'INFO: ' + arg.encode(CODING))
                response += self.dummy_responses.border([b'OK'])
            elif 'log_warn' in cmd:
                self.logs.append(b'WARN: ' + arg.encode(CODING))
                response += self.dummy_responses.border([b'OK'])
            elif 'log_query' in cmd:
                try:
                    response += self.dummy_responses.border(self.logs[-int(arg):])
                except ValueError:
                    response += self.dummy_responses.border(['Not an integer'.encode(CODING)])
            elif self.dummy_responses.is_dummy_cmd(cmd):
                response += self.dummy_responses.gibberish()
            elif 'query_payload_telemetry' in cmd:
                response += self.dummy_responses.telemetry()
            elif 'system_shell' in cmd:
                cmd_result = subprocess.run(arg.split(), cwd='/app/flag/',
                                            capture_output=True, timeout=1)
                response += self.dummy_responses.border([cmd_result.stdout, cmd_result.stderr])
            else:
                # This is a hint that tells the player they succeeded in bypassing the CBC-MAC check, but aren't
                # running a valid command. Ideally the player will run sys_shell{some command} without needing to
                # run into this.
                response += self.dummy_responses.border(['The command passed CBC-MAC verification but the command is '
                                                         'unknown. This error should not occur.'.encode(CODING)])
        finally:
            return response

    def __log_generator(self):
        awacs = 'E-3 "OVERLORD": '.encode(CODING)
        num_logs = randrange(4000, 4150)
        self.logs.append('INFO: CP-46: cleared logs'.encode(CODING))
        while len(self.logs) < num_logs:
            current_pattern = self.pattern.__next__()
            self.logs.append(awacs + 'is in zone '.encode(CODING) + current_pattern.encode(CODING))

            if randrange(0, 3) == 0:
                self.logs.append(awacs + 'uploaded '.encode(CODING)
                                 + str(randrange(9 * 100000, 10 * 1000000)).encode(CODING) + ' bytes'.encode(CODING))

            if randrange(0, 3) == 0:
                self.logs.append(awacs + 'downloaded '.encode(CODING)
                                 + str(randrange(9, 50000)).encode(CODING) + ' bytes'.encode(CODING))

    def __decrypt_cmd(self, encrypted_cmd: bytes) -> bytes:
        iv = encrypted_cmd[:AES.block_size]
        cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted_cmd[AES.block_size:])
        unpadded = unpad(decrypted, AES.block_size)
        return unpadded

    @staticmethod
    def __cbc_mac(key: bytes, data_to_digest: bytes) -> bytes:
        iv = b'\0' * 16
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return cipher.encrypt(pad(data_to_digest, AES.block_size))[-16:]

    def __verify_cmds(self, unverified_cmd: bytes) -> bool:
        for key in self.cbc_mac_keys:
            unverified_cmd_mac = self.__cbc_mac(key, unverified_cmd)
            for mac in self.macs:
                if unverified_cmd_mac == mac:
                    return True
        return False


class SVSimulatorHandler(StreamRequestHandler):
    def handle(self):
        dummy_responses = DummyResponses
        space_vehicle = SpaceVehicleSimulator()
        command_data_queue = b''
        while True:
            try:
                client_data = self.request.recv(1024)
                if client_data == b'':  # No data received - stop handling this request
                    return
                # No valid commands received (valid commands are terminated with a null byte)-
                # keep waiting for more data on the socket
                if b'\x00' not in client_data:
                    command_data_queue += client_data
                    continue
                client_data = command_data_queue + client_data  # Join with any data previously received
                # If this data does not end with a null byte (end of command), then keep extra
                # data around since we're expecting to receive the rest of the command in another recv call
                if client_data[-1] != b'\x00':
                    last_delimiter = client_data.rfind(b'\x00')
                    command_data_queue = client_data[last_delimiter + 1:]
                    client_data = client_data[:last_delimiter]
                data_to_send_back_to_client = space_vehicle.respond(client_data)
                self.wfile.write(data_to_send_back_to_client)
            except BrokenPipeError:
                # Client disconnected
                return
            except Exception as err:
                # Some other exception happened
                # logging.exception(err)
                self.wfile.write(dummy_responses.border(['Crashed! Restarting...'.encode(CODING)]))
                return


class TCPServerWithReuse(ThreadingTCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        self.allow_reuse_address = True
        ThreadingTCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)


def main(args=None):
    if args is None:
        parser = argparse.ArgumentParser()
        parser.add_argument('host')
        parser.add_argument('port', type=int)
        args = parser.parse_args()
    service_host = os.getenv("SERVICE_HOST")
    service_port = os.getenv("SERVICE_PORT")
    logging.basicConfig(level=logging.INFO)

    with TCPServerWithReuse((args.host, args.port), SVSimulatorHandler) as server:
        print("Please connect to the space vehicle command service at {}:{}".format(service_host, service_port),
              flush=True)
        server.serve_forever()
        server.shutdown()
    print("Exiting", flush=True)


if __name__ == '__main__':
    print("\n", flush=True)
    main()
