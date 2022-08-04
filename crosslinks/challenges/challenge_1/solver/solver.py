import os
import sys
import socket
import cost_solver

def solve( host,port  ):
    # connect to the challenge
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    complete = False
    keep_solving = True 
    total = 0
    ticket_sent = False
    while( keep_solving ):
        keep_reading = True 
        challenge =""

        while( keep_reading ):
            
            data = s.recv(10000)
            
            chonk = data.decode("UTF-8")
            
            challenge = challenge + chonk
            total = total + len(chonk)
            if( challenge.find("Ticket please:") != -1 and (ticket_sent == False ) ) :
                ticket = os.getenv("CHAL_TICKET")
                print("Sending ticket - {}".format( ticket ), flush=True)
                s.send( ticket.encode('utf-8'))
                s.send( "\n".encode('utf-8'))
                ticket_sent = True
                
            if( challenge.find("What satellite am I:") !=-1 and challenge.find("TLE") !=-1 ):
                #print("Received a challenge: ")
                # do some cleanup
                start_ind = challenge.find("TLE")
                end_ind = challenge.find("What satellite am I:")
                #print("Received a challenge: {} {}".format( start_ind , end_ind )) 
                challenge = challenge[start_ind:end_ind]
                
                print(challenge, flush=True)

                keep_reading = False
            if( challenge.find("Complete!") != -1 ):
                print(challenge, flush=True)

                complete = True
                keep_reading = False
        
        if( complete ):
            print("Done", flush=True)
            keep_solving = False
        else:
            sat = solve_single( challenge )
            print("Sending answer", flush=True)
            sat = sat + "\n"
            s.send( sat.encode('utf-8'))
def solve_single(  challenge ) :
    # split the challenge into data 
    loc_tle_start = challenge.find("TLE\n")
    loc_measure_start = challenge.find("Measurements\n")
    loc_measure_end = challenge.find("What satellite am I:")

    tle_string = challenge[loc_tle_start+4:loc_measure_start]
    measure_string = challenge[loc_measure_start+13:loc_measure_end]
    
    T = open("tle_socket.tle" ,'wt')
    T.write( tle_string )
    T.close()

    M = open("measure_socket.txt" ,'wt')
    M.write( measure_string )
    M.close()
    # run the solver
    b = cost_solver.BruteForceSolver( "tle_socket.tle" , "measure_socket.txt")
    sat = b.solve()
    print("I think its  {}".format( sat ))
    return sat

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

    print("Solving at {}:{}".format(host,port) , flush = True )
    solve(host,port)