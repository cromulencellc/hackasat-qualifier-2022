import fpga
import bitstream
import os
import socket
import sys
from timeout import timeout,TimeoutError

to = int( os.getenv("TIMEOUT",300))

@timeout(to)
def challenge():
    flag = os.getenv("FLAG","flag{CONTACT_AN_ADMIN_IF_YOU_SEE_THIS}")
    port = int( os.getenv("BITSTREAM_PORT",5000))
    filename = 'user-bitstream.bit'
    keep_going = True
    service_host = os.getenv("SERVICE_HOST", "localhost") 
    service_port = os.getenv("SERVICE_PORT", port) 
    print("To configure FPGA connect via TCP and send/rcv data at {}:{}".format(service_host, service_port))
    print("Connect to the configuration port as a TCP client", flush=True)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))
    sock.listen( 1 )
    target, address =  sock.accept() 
    print("Client connected" ,flush=True)
    cfgEngine = fpga.FPGA( flag , target )
    # Run unless the user sends an empty bitstream
    while(keep_going):
        try:
            # Get the bitstream from the player
            print("Send bitstream bytes over the the bitstream port", flush=True)
            bs = target.recv( 200000 )
            # Make sure it has non-zero size
            if( len( bs ) ==  0):
                print("Empty bitstream sent - challenge exiting", flush=True)
                sys.exit(0)
            if( len(bs) > 1000 ):
                # Lets limit bitstream size to 1k bytes
                print("Bitstream too big - challenge exiting", flush=True)
                sys.exit(1)
            # Write it to a file
            f = open(filename,'wb')
            f.write( bs )
            f.close()
            # Run it
            cfgEngine.run(filename)
            keep_going = False
        except (fpga.FpgaResetError, bitstream.BitStreamError) as error:
            # If we get an error of some kind - reset the FPGA and continue
            print("\n",flush=True)
            cfgEngine.reset()
            keep_going = True 


if __name__ == "__main__":
    try:
        challenge()
        print("Exiting....bye",flush=True)
    except TimeoutError:
        print("Timeout.......bye",flush=True)