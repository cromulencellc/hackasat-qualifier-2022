import sys
import socket
import os
import subprocess
import time


if __name__ == "__main__":
    host = os.environ.get('CHAL_HOST')
    port = os.environ.get('CHAL_PORT')

    ticket = os.environ.get('TICKET', "")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Connect to challenge. {host}:{port}", flush=True)
    
    sock.connect((host, int(port)))
    fsock = sock.makefile('rw')
    if len(ticket):
        fsock.readline()
        fsock.write(ticket + '\n')
        fsock.flush()
        line = fsock.readline()
        print(line, flush=True)
        lines=1
        while "Challenge Web Page" not in line:
            lines+=1
            line = fsock.readline()
            print(line, flush=True)
            if (lines > 5):
                print("Solver failed")
                sys.exit(1)
    # _ = fsock.readline()
    # line = fsock.readline()
    # print(line, flush=True)
    host,port = line.rstrip().split('/')[-1].split(":")
    print(host, port, flush=True)
    env = os.environ
    env['CHAL_HOST'] = host
    env['CHAL_PORT'] = port
    print("Sleeping to let the system boot for 30sec...", flush=True)
    time.sleep(30)

    process = subprocess.Popen(["/bin/bash", '-c', './solver.sh 2>&1'], env=env)

    # for line in process.stdout:
    #     print(">>> " + str(line.rstrip()), flush=True)
    #     process.stdout.flush()

    process.wait()