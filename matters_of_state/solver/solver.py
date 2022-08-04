import socket
import os
import numpy as np
import sys
import re 
import sgp4.api as sp4
import datetime
import helper

def get_value( text , preamble ):
    lines = text.split("\n") 
    out = ""
    for line in lines:
        if( preamble in line ):
            out = line 
    value = re.findall("\d+\.\d+", out)

    return float(value[0] )
def get_date( text ,preamble):
    lines = text.split("\n") 
    out = ""
    for line in lines:
        if( preamble in line ):
            out = line.replace(preamble,"") 
            out = out.replace("UTC","")
            out = out.strip()
            out=out+"+0000"
    date = datetime.datetime.strptime( out  , '%Y-%m-%d %H:%M:%S%z')

    return date
def mean_to_eccentic( M , e , tol=1e-5 ):

    if( M > np.pi ):
        M0 = np.pi*2 - M 
    else:
        M0 = M 
    E_guess = np.arange( 0 , np.pi , tol )
    M_Guess =  E_guess - e*np.sin(E_guess )

    dM =abs( M0 - M_Guess ) 
    ind = np.argmin( dM , axis=0)
    if( M > np.pi ):
        E = 2*np.pi - E_guess[ind]
    else:
        E = E_guess[ind]
    print("Eccentric anomaly is: {}".format( E))
    return E


def solve_single( sock ):
    print("Trying to solve", flush=True)

    challenge = sock.read_until(["Find" ,"Flag","Wrong"])
    print(challenge , flush=True)
    if( "Wrong" in challenge):
        sys.exit(0)
    if( "Flag" in challenge):
        print(sock.get_remaining() , flush=True)
        sys.exit(0)

    

    a = get_value( challenge , "semi-major")
    e = get_value( challenge , "eccentricity")
    i = get_value( challenge , "inc")
    RAAN = get_value( challenge , "RAAN")
    peri  = get_value(challenge, "Argument")
    M = get_value(challenge, "Mean")
    mu = 398600.4418  # km^3 / s^2
    #d  = get_date( challenge , "Time:")
    inc = np.deg2rad( i )
    E = mean_to_eccentic( np.deg2rad(M),  e )
    TA = np.arccos( (np.cos(E)-e)/(1- e*np.cos(E)))
    print( "True Anomaly is:  {}".format( TA ))
    R = np.deg2rad( RAAN )
    W = np.deg2rad( peri ) + TA 
    
    r = a*(1- e*np.cos(E))
    v = np.sqrt( mu * ( (2/r) - (1/a) ) )
    fpa = np.arctan( e*np.sin(TA ) / (1+ e*np.cos(TA)))
    if( TA > np.pi ):
        fpa = -fpa
    D1 = np.array( [np.cos(-W), np.sin(-W), 0 , -np.sin(-W), np.cos(-W) , 0 ,0 ,0 , 1]) # true anomaly rotation and argp
    D2 = np.array( [1 , 0, 0 , 0, np.cos(-inc) , np.sin(-inc) , 0, -np.sin(-inc), np.cos(-inc)] ) # incl rotation
    D3 = np.array( [np.cos(-R), np.sin(-R), 0 , -np.sin(-R), np.cos(-R) , 0 ,0 ,0 , 1]) # RAAN rotation

    D1 = D1.reshape(3,3)
    D2 = D2.reshape(3,3)
    D3 = D3.reshape(3,3)

    rot = np.matmul( D3, np.matmul( D2, D1 ))
    rot2 = rot.transpose() 
    print( "FPA is {}".format( fpa))
    print("Velocity is: {}".format( v))
    v_r = v * np.sin( fpa )
    v_w = v * np.cos( fpa )
    R_VEC = np.array([r , 0 , 0 ])
    V_VEC = np.array([v_r , v_w , 0 ])
    R_VEC = R_VEC.reshape(3,1)
    V_VEC = V_VEC.reshape(3,1)
    print( V_VEC )

    position = np.matmul( rot , R_VEC ).reshape(1,3)
    velocity = np.matmul( rot,V_VEC).reshape(1,3)
    position = position[0]
    velocity = velocity[0]
    pos = "{},{},{}\n".format( position[0], position[1], position[2])
    vel = "{},{},{}\n".format( velocity[0], velocity[1], velocity[2])
    print("I think the position is: {}".format( pos), flush=True)
    print("I think the velocity is: {}".format( vel ), flush=True)
  
    sock.send( pos )
    sock.send( vel)



def batch_solve(host, port ):
    s = helper.TcpReader( host,  port )
    ticket = os.getenv("CHAL_TICKET")
    if( ticket  != None ):
        s.read_until("Ticket please:")
        print("Sending ticket - {}".format( ticket ), flush=True)
        s.send( ticket)
        s.send( "\n")
        ticket_sent = True
    
    keep_going = True
    while( keep_going ):
        solve_single(s)


if __name__ == "__main__":
    host = os.getenv("CHAL_HOST")
    port = int(os.getenv("CHAL_PORT") ) 
    batch_solve( host , port ) 