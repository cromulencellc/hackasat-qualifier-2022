import os

from transmitter import transmitter_main
import data_file
import argparse
import time
from timeout import timeout,TimeoutError

to = int( os.getenv("TIMEOUT",400))

@timeout(to)
def challenge( args ):
    print("Keep the signal power high if to get the flag")
    print("\n\n")
    # These lines are here to support our infrastructure
    service_host = os.getenv("SERVICE_HOST","localhost")
    service_port = os.getenv("SERVICE_PORT", args.src_port)
    command_port = int(service_port)
    sample_port = command_port+1
    print("Antenna pointing TCP server accepts commands at {}:{}".format( service_host , command_port ))
    print("Sample TCP server will provide samples at {}:{}".format( service_host , sample_port))
    flag = os.getenv('FLAG')
    time.sleep(1)
    # Create teh data bit file
    data_file.make_databit_file( "databits.bin", 800 , 4 , flag)
    transmitter_main( source_ip=args.ip , source_port=args.src_port, sink_port=args.snk_port)
    print("Exiting")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--command-port", dest="src_port", type=int, required=True)
    parser.add_argument("--ip", dest="ip", required=True)
    parser.add_argument("--sample-port", dest="snk_port", type=int, required=True)
    args = parser.parse_args()

    try:
        challenge( args )
    except TimeoutError:
        print("Timeout.....bye")