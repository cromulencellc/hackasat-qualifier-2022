import subprocess
import zmq
import socket
import struct
import sys
import os
def demote(user_uid, user_gid):
    def set_ids():
        os.setgid(user_gid)
        os.setuid(user_uid)
    return set_ids
def embedded( arch="arm"):
    if( "x86" == arch  ):
        result = subprocess.run(["web/binary.bin"])
        pass
    elif( "arm" == arch):
        cmd = ["qemu-aarch64" , "-L" , "/usr/aarch64-linux-gnu/", "web/binary.bin"]
        result = subprocess.Popen(cmd, preexec_fn=demote(2000,2000), stdout=sys.stdout ,stderr=sys.stderr)
        pass
def zmq_interface( in_port , out_port ):
    context = zmq.Context()
    zIn = context.socket(zmq.PULL)
    zIn.connect("tcp://localhost:{}".format( in_port ) )
    zOut = context.socket( zmq.PUSH)
    zOut.connect("tcp://localhost:{}".format( out_port ))
    s= socket.socket( socket.AF_INET , socket.SOCK_STREAM)
    s.settimeout(5) # timeout for listening - stop nefarious nerds
    s.bind( ("127.0.0.1",6000))
    s.listen()
    

    try:
        conn, addr = s.accept( )
    except socket.timeout:
        # Protect ourselves from malicious code, protect ourselves from
        print("Your flight software didnt communicate with the bus.")
        print("Bye", flush=True)
        os._exit(1)
    except Exception as e:
        print( e )
        sys.exit(0)

    #print("Connected to software {}".format( addr ))
    while( True ):
        # get data in form
        inMsg = zIn.recv( )
        # Send this over the socket.
        conn.send(inMsg)
        # Wait for it to come back 
        outMsg = conn.recv( 1024 )
        zOut.send(outMsg)
def test_qemu_socket( ):
    s= socket.socket( socket.AF_INET , socket.SOCK_STREAM)
    s.bind( ("127.0.0.1",6000))
    s.listen()
    conn, addr = s.accept( )
    inMsg = struct.pack("<7f", *[10000.0,20000.0,30000.0, 12.0,13.0,14.0 ,1.2])
    print(inMsg)
    conn.send(inMsg)

    outMsg = conn.recv(1024)
    print( "Got {}".format(outMsg))
    s.close()
if __name__ == "__main__":
    test_qemu_socket()
    #zmq_interface(5001,5000)