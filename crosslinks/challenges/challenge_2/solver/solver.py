import os
import socket
import sys
import batch_solver
import time
def solve( host, port  ):
    lookfor = [ "What's my position: x,y,z\n","TLE\n" , "Measurements\n"]
    # connect to the challenge
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    complete = False
    keep_solving = True 
    total = 0
    count = 1
    ticket_sent = False
    while( keep_solving ):
        keep_reading = True 
        challenge =""
        found = 0
        while( keep_reading ):
            
            data = s.recv(10000)
            chonk = data.decode("UTF-8")
            challenge += chonk 
            found = []
            for item in lookfor:
                idx = challenge.find(item)
                if( -1 != idx  ):
                    found.append( idx ) 
            if( -1 != challenge.find("bye")):
                print(challenge)
                sys.exit(-1)
            if( challenge.find("Ticket please:") != -1 and (ticket_sent == False ) ) :
                ticket = os.getenv("CHAL_TICKET")
                print("Sending ticket - {}".format( ticket ), flush=True)
                s.send( ticket.encode('utf-8'))
                s.send( "\n".encode('utf-8'))
                ticket_sent = True
                
            if( -1 != challenge.find("Complete!") ) :
                print(challenge, flush=True)
                complete = True
                keep_reading = False


            if( len(lookfor) == len(found) ):
                # hey we found all the prompts!
                keep_reading = False
                prompt = found[0]
                tle_start = found[1]
                measures_start = found[2]
                print(challenge, flush=True)

        if( complete ):
            print("Done", flush=True)
            keep_solving = False
        else:
            tle_string = challenge[tle_start+4:measures_start]
            measure_string = challenge[measures_start+13:prompt]
            out = solve_single( tle_string , measure_string  )
            
            pos = out[0] 
            vel = out[1] 
            pos_str = "{},{},{}\n".format( pos[0] , pos[1], pos[2])
            vel_str = "{},{},{}\n".format( vel[0] , vel[1], vel[2])

            print("Sending position {}".format(pos_str) , flush=True)
            s.send( pos_str.encode('utf-8'))
            x = s.recv(1000)
            print( x.decode("UTF-8") )
            print('Sending velocity {}'.format(vel_str), flush=True)
            s.send( vel_str.encode('utf-8'))


def solve_single( tle_string , measurement_string ):
    T = open("tle_socket.tle" ,'wt')
    T.write( tle_string )
    T.close()

    M = open("measure_socket.txt" ,'wt')
    M.write( measurement_string )
    M.close()

    s = batch_solver.SmartSolver( "tle_socket.tle" , "measure_socket.txt")
    out = s.solve()
    return out 
if __name__ == "__main__":
    

    host = os.getenv("CHAL_HOST")
    if not host:
        print("No HOST supplied from environment")
        sys.exit(-1)

    # get port from environment
    port = int(os.getenv("CHAL_PORT","0"))
    if port == 0:
        print("No PORT supplied from environment")
        sys.exit(-1)

    print("Solving at {}:{}".format(host,port))
    solve(host,port)
    sys.exit(0)