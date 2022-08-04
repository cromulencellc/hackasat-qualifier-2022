import os
import sys
import random
import orbital
import numpy as np
import astropy 
from timeout import timeout,TimeoutError

to = int( os.getenv("TIMEOUT",120))

def str_to_vec( str_in ):
    vec =  np.fromstring( str_in , dtype=float, count=-1 , sep=',')
    if( vec.size != 3 ):
        raise "Vector doesnt have 3 elements"
    return vec
def single( ):
    pos_tolerance = 10.0
    vel_tolerance = 0.1
    correct = True
    print("Orbital Elements: ")
    RE = 6378.0
    a = 10.0 * RE
    e =  0.3 
    i = 63.0 
    RAAN =  25.0 
    peri = 78.0
    mu = 398600.5  # km^3 / s^2
    n = np.sqrt( mu / np.power(a,3))
    M = 10.0 #random.random( ) * 360.0
    times = ['2022-01-01T00:00:00']
    t = astropy.time.Time(times, format='isot', scale='utc')    
    orbit = orbital.elements.KeplerianElements( a=a*1000.0, e=e, i=np.deg2rad(i), raan=np.deg2rad(RAAN) , arg_pe=np.deg2rad(peri), M0=np.deg2rad(M), body=orbital.bodies.earth , ref_epoch=t )
    orbit.propagate_anomaly_by(M=0.0)
    pos_truth = orbit.r/1000.0
    vel_truth = orbit.v/1000.0
    print("Given the following orbit elements: ")
    print("semi-major axis: {} km".format(a))
    print("eccentricity: {}".format(e))
    print("inclination: {} deg".format(i))
    print("RAAN: {} deg".format(RAAN))
    print("Mean anomaly: {} deg".format(M))
    print("Argument of periapsis: {} deg".format(peri))
    print("Time: {}".format( t[0] ))
    print("Find the state vector of the statellite")
    print("Position: X,Y,Z " , flush=True)
    pos_answer = input( )
    p = str_to_vec( pos_answer )
    print("Velocity: Vx,Vy,Vz", flush=True)
    vel_answer = input( ) 
    v = str_to_vec( vel_answer )
    dP = np.linalg.norm( pos_truth - p )
    dV = np.linalg.norm( vel_truth - v )
    print("dP: {} dV: {}".format( dP ,dV ), flush=True)
    if( dP > pos_tolerance ):
        print("Position incorrect", flush=True)
        correct = False 
    if( dV > vel_tolerance ):
        print("Velocity incorrect", flush=True)
        correct = False
    
    return correct
    


@timeout( to )
def main():
    N = 5
    
    for k in range( N ):
        ok = single( )
        if( False == ok ):
            print("Wrong", flush=True)
            print("....Later" , flush=True)
            sys.exit(0)
        print("Correct" , flush=True)
    flag = os.getenv("FLAG")
    print("Flag: {}".format( flag ) , flush=True)


if __name__ == "__main__":
    try:
        main()
    except TimeoutError:
        print("Timeout.....bye")
    sys.exit(0)