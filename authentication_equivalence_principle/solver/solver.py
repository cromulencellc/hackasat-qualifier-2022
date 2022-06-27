import helper
import os
import sys
import skyfield.api as sf
import datetime
import argparse
import hmac
import numpy as np
import keycracker
def solver_batch(host,port , args , auth_file,  keyfile ):
    # First things first lets crack the key file
    config = keycracker.crack_keys(   keyfile  ,auth_file,)   
    #
    io = helper.stdio_solve_helper( host=host ,port=port, prompt="Provide the key:" , solved="Complete!" , wrong="Later.", encoding="UTF-8")
    tle_file = open('challenge_tle.txt','wt')
    io.handle_ticket()
    # Set up our challenge IO helper to look for these blocks of text
    io.add_challenge_block(name="TLE",header="TLE", reset = False)
    io.add_challenge_block(name="SYNC", header="The authenticator was clock-sync'd and started at:" , reset = False )
    io.add_challenge_block(name="TIME", header="The ground station will send the next communication at:", reset = True )
    # Loop until the challenge is complte
    while( False == io.is_complete()  ):
        ## IMPORTANT: PLAYERS NEED TO reverse engineer these valus
        period_sec = config["period"]
        secret_key = config["hmac_key"]
        ground_station = ( config["lat"] , config["lon"]) 
        # Wait for the challenge to be sent to us
        io.wait_for_single_challenge( )
        # store the TLE data to a file
        tle_file = open('challenge_tle.txt','wt')
        tle_file.write("SAT1") # the challenge doesnt give us the satellite name - but its irrelevant
        tle_file.write( io.get("TLE") ) 
        tle_file.close()
        # Get the time of synchronization and time of  send
        sync_time = io.get("SYNC").replace("\n","")
        send_time = io.get("TIME").replace("\n","")
        # use the solver function to solve it
        answer = solve( 'challenge_tle.txt' , sync_time , send_time, secret_key , period_sec , ground_station, args["propagation"], args["relativity"] )
        answer = answer + "\n"
        # send the answer (and a \n)
        io.send_answer(answer)
        # tell our io helper to wait for a new set of challenges
        io.reset()
def solve( tle , sync_time , time_of_send ,secret_key, period_sec, ground_station , with_prop_delay , with_time_dilation ):
    time_format = """%Y-%m-%dT%H:%M:%S.%f%z"""
    C = 299792.458 #Speed of light  - km / sec   
    ts = sf.load.timescale() # skyfield timescale
    
    # make strings into datetimes
    send =  datetime.datetime.strptime(time_of_send, time_format)
    sync =  datetime.datetime.strptime( sync_time,time_format)
    # convert to skyfield times
    t_send = ts.from_datetime( send )
    t_sync = ts.from_datetime( sync )
    # use some default values
    prop_delay = 0.0
    time_dilation = 0.0
    # load up our tle file
    sats = sf.load.tle_file( tle )
    sat_dict = {sat.name: sat for sat in sats}
    sat = sat_dict["SAT1"]
    ## If propagation delay is turned on calculate it here
    if( True == with_prop_delay ):
        # get the satellite from the TLE

        gs = sf.wgs84.latlon( ground_station[0] , ground_station[1] )

        range_vector = ( sat - gs ).at( t_send )
        prop_delay = np.linalg.norm( range_vector.position.km ) / C
        print("propagation delay is: {}".format( prop_delay ))
    # If relativity is turned on solve time dilation here
    if( True == with_time_dilation):
        # Claculate the average time dilation for a circular orbit
        n =sat.model.no_kozai / 60 
        MU =398600.4418 #km^3 / s^2 (EARTH)
        R_E = 6378 #km
        period = 2*np.pi/n
        period = 2*np.pi/n
        semi_major = np.cbrt( MU * np.square( (period/(2*np.pi)) )  ) 
        circ_vel = np.sqrt( MU * 2/ semi_major )
        dU = - ( MU /  semi_major) + (MU/R_E)
        potential_drift = dU / (C*C)
        special_drift =   np.square(circ_vel / (2*C) )
        drift_rate = -special_drift  + potential_drift
        ellapsed = ( send - sync ).total_seconds()
        time_dilation = drift_rate * ellapsed
        print("Time dilation: {}".format( time_dilation))

    # Calculate time on the satellite clock
    satellite_clock = send + datetime.timedelta( seconds=(prop_delay + time_dilation) ) 
    time_since_sync = satellite_clock - sync
    # Calculate TOTP count value on the satellite clock
    count = int( time_since_sync.total_seconds() / period_sec ) 
    print("Count {}\n".format(count))
    count_bytes = count.to_bytes(8,"little")
    # create a new HMAC-SHA256 encoding of our secret key and message
    keygen =  hmac.new( secret_key.encode("utf-8"), msg = count_bytes , digestmod='sha256')
    key = keygen.hexdigest() #put it in hex



    return key
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('--no-relativity', dest='relativity', help='Run the solver but skip relativity', default=True,action='store_false')
    parser.add_argument('--no-propagation', dest='propagation',help='Run the solver but skip propagation delay', default=True, action='store_false')
    parser.add_argument('--auth-data', dest='authfile',help='Encrypted AuthFile', default="authdata.bin")
    parser.add_argument('--key-file', dest='keyfile',help='Auth Key', default="key.txt")

    args = vars(parser.parse_args())
    host = os.getenv("CHAL_HOST","172.17.0.1") 
    port = int( os.getenv("CHAL_PORT",12345) ) 

    if( not host ):
        sys.exit(-1)
    if( not port ):
        sys.exit(-1)
    solver_batch(host, port, args , args["authfile"] ,args["keyfile"])