from lib2to3.pgen2 import driver
import math
import numpy as np
from numpy import vectorize
import crosslink.generate
import crosslink.tlehelp
import sys, select
import os 
import skyfield.api as sf
import position
import random
from timeout import timeout, TimeoutError

time = int(os.getenv("TIMEOUT",90))

def challenge( sat , timeout , tle , seed ):
    
    # settings
    rr_noise = 0.05
    r_noise = 0.01 # noise variance of 10 m
    n_measurements = 1
    dt = 100
    vel_tolerance = 0.1  # 100 m/s
    pos_tolerance = 0.05 # 50 meters
    clock_bias = 0.00005
    sats = sf.load.tle_file( tle )
    by_name = {k.name: k for k in sats}
    startTime = by_name[sat].epoch.utc_strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    
    gen = crosslink.generate.CrossLinkGen( tle , seed , r_noise , rr_noise , clock_bias)
    
    correct = position.getPosition( tle , sat , startTime )


    gen.generate( sat , startTime , n_measurements*dt, dt )

    # Only print the TLEs to the satellites you saw 
    print("TLE")
    crosslink.tlehelp.print_sats( tle , gen.satsViewed() )

    print("Measurements")
    gen.dump(filename=False)
    print("What's my position: x,y,z")
    pos_response = input()
    try: 
        pos_answer = str_to_vec( pos_response )
        vec_is_ok( pos_answer )
    except: 
        print("Position string not formatted")
        return False
    print("What's my velocity: vx,vy,vz")
    vel_response = input()

    try: 
        vel_answer = str_to_vec( vel_response )
        vec_is_ok( vel_answer )
    except:
        print("Velocity string not formatted correctly")
        return False


    # print the data
    print( "Answer received")
    # Wait for answer 
    i = True
    #i,o,e = select.select([sys.stdin],[],[], timeout )
    if( i ):
        # you gave an answer
        
        #answer = sys.stdin.readline().strip()
        correct = compare( correct[0] , pos_answer , correct[1], vel_answer , pos_tolerance , vel_tolerance )
        if( True == correct ):
            print("Correct")
            return True
        else:
            print("Wrong!")
            return False
    

    else:
        print("Too slow")
        # didnt answer in time
        return False
def vec_is_ok( invec):
    
    for val in invec :
        
        if(False == math.isfinite( val )):
            raise ValueError 
def str_to_vec( str_in ):
    vec =  np.fromstring( str_in , dtype=float, count=-1 , sep=',')
    if( vec.size != 3 ):
        raise "Vector doesnt have 3 elements"

    return vec
def compare( p1 , p2 , v1 ,v2 , tol_P , tol_V ):
    dR = p1 - p2
    dV = v1 - v2 

    pos_error = np.linalg.norm( dR )
    vel_error = np.linalg.norm( dV )
    #print( "Pos error: {} Vel error: {}".format( pos_error , vel_error))
    if( ( pos_error <=  tol_P) and ( vel_error <= tol_V) ):
        return True    
    return False
    
@timeout(time)
def batch_challenge( num_solves , timeout , tle ):
    seed = os.getenv("SEED")
    if not seed:
        print("No seed provided")
        sys.exit(-1)
    # This is probably hard enough that we dont need to see it
    random.seed( 10 )
    
       
    #sats = random.choices(  crosslink.tlehelp.available(tle) , k=num_solves)
    sats = ["COMM-1337"]
    for sat in sats :
        
        success = challenge( sat , timeout , tle , seed )
        if( False == success):
            #sorry
            return False
    return True
    

if __name__ == "__main__":
    

    success = batch_challenge( 1 , 20 , "data.tle" )
    if success:
        print("You did it - yay!")
        flag = os.getenv('FLAG')
        print(flag)
        print("Complete!")
    else:
        print("Incorrect...bye")
    sys.exit(0)