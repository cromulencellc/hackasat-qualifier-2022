import crosslink.generate
import crosslink.tlehelp
import sys
import os 
import random 
import skyfield.api as sf
from timeout import timeout, TimeoutError

time = int(os.getenv("TIMEOUT",90))

def challenge( sat , tle , seed ):
    
    correct = sat 
    # settings
    rr_noise = 1
    r_noise = 10

 
    n_measurements = 15
    dt = 100

    sats = sf.load.tle_file( tle )
    by_name = {k.name: k for k in sats}
    startTime = by_name[sat].epoch.utc_datetime()

    gen = crosslink.generate.CrossLinkGen( tle , seed , r_noise , rr_noise )
    print_tle( tle )
    gen.generate( sat , startTime , n_measurements*dt, dt)
    print("Measurements")
    gen.dump(filename=False)
    print("What satellite am I:")


    # print the data
    response = input()
    # Wait for answer 
    i = True
    #i,o,e = select.select([sys.stdin],[],[], timeout )
    if( i ):
        # you gave an answer
        answer =response
        #answer = sys.stdin.readline().strip()
        print("You answered {}".format(answer))
        if( answer == correct):


            print("Correct")
            return True
        else:
            return False
    

    else:
        print("Too slow")
        # didnt answer in time
        return False
def print_tle( tle_file ):
    print("TLE")
    f = open(tle_file)
    lines = f.readlines( )
    for line in lines:
        print(line.strip())

@timeout(time)
def batch_challenge( num_solves ,  tle ):

    
    # pick 5 satellites at random
    seed = os.getenv("SEED")
    if not seed:
        print("No seed provided")
        sys.exit(-1)
    random.seed( seed )
    sats = random.choices(  crosslink.tlehelp.available(tle) , k=num_solves)
    for sat in sats :
        
        success = challenge( sat ,  tle  ,seed )
        if( False == success):
            #sorry
            return False
    return True
    

if __name__ == "__main__":
    

    success = batch_challenge( 5 ,  "data.tle" )
    if success:
        print("Welcome to flag town, population: you")
        flag = os.getenv('FLAG')
        print(flag)
        print("Complete!")
    else:
        print("Incorrect...bye")