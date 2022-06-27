import exploit
import os
import socket
import argparse
import time
def handle_ticket(socket):
    ticket = os.getenv("CHAL_TICKET")
    if( ticket  != None ):
        socket.recv(1000)
        print("Sending ticket - {}".format( ticket ), flush=True)
        socket.send( ticket.encode('utf-8'))
        socket.send( "\n".encode('utf-8'))
def solve( file_name ):
    host = os.getenv("CHAL_HOST","172.17.0.1")
    port = int(os.getenv("CHAL_PORT",8000))
    config_port = int( os.getenv("CONFIG_PORT",8001))
    io_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    io_socket.connect((host, port))
    handle_ticket(io_socket) 
    out = io_socket.recv( 100000 )   
    print(out.decode('utf-8'))
    time.sleep(5)
    config_port = int(input("Enter config port: "))
    config_host = input("Enter config host: ")    
    exploit.run(file_name, config_host , config_port)
   
    print("Solved! --- waiting a bit until we close")
    time.sleep(10)
    out = io_socket.recv( 100000 )   
    print(out.decode('utf-8'))
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Attack the fpga with starbleed')
    parser.add_argument('--bit-file', dest='file', help='A yml file containing the commands you want to run', required=True)
    args = vars(parser.parse_args())
    solve(args["file"])
