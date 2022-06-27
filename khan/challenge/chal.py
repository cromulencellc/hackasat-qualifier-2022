#!/usr/bin/env python3

import os
import sys
import time
import sim.lander
import threading
import fsw.wrapper
import web_interface 
# Local imports
from timeout import timeout, TimeoutError, MINUTE


TO = int(os.getenv("TIMEOUT", 10 * MINUTE))

@timeout(TO)
def challenge():
    web_interface.mtx.acquire()
    web = threading.Thread(target=web_interface.run_web )
    zmq = threading.Thread( target=fsw.wrapper.zmq_interface, args=(5001,5000) )
    
    embedded=  threading.Thread( target= fsw.wrapper.embedded )
    zmq.setDaemon(True)
    embedded.setDaemon(True)
    web.setDaemon(True)
    web.start()
    web_interface.mtx.acquire( )
    zmq.start()
    embedded.start()
    print("Please wait for probe simulation to run", flush=True)
    success = sim.lander.run()
    print("Simulation complete", flush=True)
    return success

if __name__ == "__main__":
    try:
        flag = os.getenv("FLAG", "flag{CONTACT_AN_ADMIN_IF_YOU_SEE_THIS}")
        os.environ["FLAG"] = "nice try"
        host = os.getenv( "SERVICE_HOST", "localhost")
        port = os.getenv( "SERVICE_PORT", 5000)
        print("Upload binary at: {}:{}".format( host,port), flush=True)
        success = challenge()
    except TimeoutError:
        print("\nTimeout, Bye")
        sys.exit(1)

    if success:
        print("Here is your flag:")
        print( flag , flush=True)
        time.sleep(0.5)
        print("\nCongrats!", flush=True)
    else:
        print("Try again...")
        tout = 300
        print("Telemetry available for  at {}:{}/tm".format(host,port) , flush=True)
        time.sleep( tout )

    
