import time
import os
import receiver
import socket
import argparse
import bit_checker 
import threading
import json

def handle_ticket( socket ):
    ticket = os.getenv("CHAL_TICKET")
    if( ticket  != None ):
        socket.recv(1000)
        print("Sending ticket - {}".format( ticket ), flush=True)
        socket.send( ticket.encode('utf-8'))
        socket.send( "\n".encode('utf-8'))
        ticket_sent = True

def merge_json( f1 , f2 , out ):
    file1 = open(f1,"rt")
    file2 = open(f2,"rt")
    a = json.load( file1 )
    b = json.load( file2 )
    file1.close()
    file2.close()
    
    out_dict = {**a, **b}
    o_file = open(out ,'wt')
    text = json.dumps( out_dict )
    o_file.write( text) 
    o_file.close()

def solver( host , port , tx_file ,rx_file  ):
    # Load up the tx-config file 
    f = open(tx_file,'rt')
    text = f.read()
    text = text.replace("\n","") # get rid of new lines
    text = text + "\n"
    f.close()
    #
    merge_json( tx_file , rx_file ,"tmp.json")
    #
    io = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    io.connect((host, port))
    # Handle the ticket if needed - otherwise keep going
    handle_ticket( io )
    challenge = io.recv( 4096 ).decode('utf-8')
    print( challenge, flush=True )
    io.send( text.encode('utf-8') )
    time.sleep(5)    
    setup = io.recv( 4096 )
    print( setup.decode('utf-8') , flush=True)
    print("Enter sample host: ",flush=True)
    sample_host = input()
    print("Enter sample port: ",flush=True)
    sample_port = int(input())
    print("Running receiver")
    t = threading.Thread( target=receiver.run_rx , args=("tmp.json",sample_host,sample_port))
    t.setDaemon(True)
    t.start()
    #receiver.run_rx( "tmp.json" , sample_host , sample_port )
    time.sleep(120)
    




if __name__ == "__main__":
    host = os.getenv("CHAL_HOST", "127.0.0.1") 
    port = int( os.getenv("CHAL_PORT", 8000) )
    parser = argparse.ArgumentParser()
    parser.add_argument("--tx-config", dest="tx", type=str , required=True) 
    parser.add_argument("--rx-config", dest="rx", type=str , required=True) 
    args = parser.parse_args()
    solver( host , port  , args.tx, args.rx )
