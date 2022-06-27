import receiver
import control
from threading import Thread
import os 
import argparse
import socket
import time
import sys
def handleticket(socket):
    ticket = os.getenv("CHAL_TICKET")
    if( ticket  != None ):
        socket.recv(1000)
        print("Sending ticket - {}".format( ticket ), flush=True)
        socket.send( ticket.encode('utf-8'))
        socket.send( "\n".encode('utf-8'))
        ticket_sent = True
def listen( ip,port ):
    time.sleep( 3 )
    print("Solver listening on: {} {}".format( ip,port))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    handleticket(s)
    data = s.recv(1000)
    print( data.decode("UTF-8") , flush=True)

    continue_reading = True
    total = ""
    while( continue_reading ):
        data = s.recv(1000)
        chonk = data.decode("UTF-8")
        #print( chonk )
        total = total + chonk 
        if( "Exiting" in total ):
            continue_reading = False 



def solve( args ):
    print("Attempting to solve")
    
    port = int( os.getenv("CHAL_PORT", 8000 ) ) 
    host = os.getenv("CHAL_HOST", "172.17.0.1")
    max_cmds= 290
    # 
    listenerThread = Thread( target=listen , args=(host,port))
    listenerThread.start() 
    time.sleep(15)
    
    target_host = input("Enter hostname for samples/commands: " )
    sample_port = int(input("Enter port for samples:"))
    command_port = int(input("Enter port for commands: "))

    # start controller thread
    ctlThread = Thread( target=control.control_antenna , args=(target_host,command_port,max_cmds) )
    ctlThread.start()
    print("Threads running")
    # Receiver needs to run in the main thread 

    rx = receiver.receiver_main( sample_ip=target_host, sample_port=sample_port)
    #
    print("Running until control is done")
    ctlThread.join()
    print("Stopping gnuradio")
    #receiver.stop_flowgraph( rx )
    #listenerThread.join()
    print("Solver exiting")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-port", dest="sample_port", type=int, default=8002)
    parser.add_argument("--command-port", dest="cmd_port", type=int, default=8001) 
    args = parser.parse_args()
    solve( args )
    sys.exit( 0  )