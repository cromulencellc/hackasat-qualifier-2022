from datetime import datetime, timedelta
import os 
import skyfield.api as sf
import auth
import relativity
import numpy
from timeout import timeout,TimeoutError

to = int( os.getenv("TIMEOUT",120))

@timeout(to)
def challenge( satellite , tle_file ):
    ts = sf.load.timescale()

    # super old keygen
    t_old_epoch =  ts.utc(2020, 10 , 2)
    t_old_value =  ts.utc(2020, 10 , 3)
    #
    time_format = """%Y-%m-%dT%H:%M:%S.%f%z"""
    # Stuff the user has to figure out from our binary
    # This is the LIGO Gravational wave observatory in washington state
    lat = 46.455144
    long =  -119.407656
    key = "YaBoiEinsteinsSecretKey"
    period_sec = 50e-6 #update the key counter at this period (seconds)
    # Stuff the user knows already or that we tell them
    C = 299792.458 #km / sec 
    t0 = ts.utc(2021, 2, 2)
    tf = ts.utc(2021, 2, 10)
    synchTime =t0
    ## doothe work
    sats = sf.load.tle_file( tle_file)
    sat_dict = {sat.name: sat for sat in sats}
    sat = sat_dict[satellite]
    ground_station = sf.wgs84.latlon( lat , long )

    # make a satellite clock object
    satellite_clock = relativity.OrbitalClock(satellite,  tle_file )
    # make an authenticator object
    authenticator = auth.totp(secret_key = key , period_secs = period_sec , epoch=synchTime.utc_datetime() ) 

    # Over our time period find the **rise time** for the satellite realtive to our ground station
    t,event = sat.find_events( ground_station , t0 ,tf, altitude_degrees=15.0 )
    rise_times = []
    for t,e in zip( t,event ):
        if( e == 0 ):
            rise_times.append( t )
    # Give the players an old key
    old_keygen = auth.totp( "whatever_this_key_is_dumb" , t_old_epoch.utc_datetime() , 0.00001 )
    old_key = old_keygen.generate( t_old_value.utc_datetime() )    # Display the satellites TLE to the player
    print("We found this key from before we reset the passcode and re-sync'd")
    print(old_key)
    print("TLE")
    print_tle( tle_file, satellite) 
    # Display the authenticator sync time to teh player
    o = synchTime.utc_datetime()
    print("The authenticator was clock-sync'd and started at:{}".format(o.strftime(time_format)))




    # Loop over every rise time and ask them to establish contact by providing the key
    for contact in rise_times:
        
        earth_time_tx = contact
        distance = 0
        o = earth_time_tx.utc_datetime()
        print("The ground station will send the next communication at:{}".format( o.strftime(time_format)) )
        print("Provide the key:")
        
        # calculate the propagation delay
        range_vector = ( sat - ground_station ).at( earth_time_tx )
        # technically this is the range from the ground station to the satellite's position when transmission occurs
        # not when reception occurs. Some basic math for LEO satellites will tell us this is close enough and the transmission time
        #  difference between the two points is ~1.3m ( ~3-4 nanosecond)
        
         
        range_to_satellite = numpy.linalg.norm( range_vector.position.km )
        propagation_delay = range_to_satellite / C 
        earth_time_rcv = earth_time_tx + timedelta( seconds=propagation_delay ) 
        
        time_dilation = satellite_clock.dt_from_earth( earth_time_rcv , synchTime)
        #print("Time dilation is {}\n".format( time_dilation))
        #print( "The satellite received signal at {} the synch time is {}".format(earth_time_rcv.utc_strftime(),synchTime.utc_strftime()) )
        orbit_time_rcv = earth_time_rcv + timedelta( seconds=time_dilation ) 
        #print("Earth Tx: {} \n Sat Tx: {}\n {}\n ".format( earth_time_tx.utc_datetime(), earth_time_rcv.utc_datetime() ,orbit_time_rcv.utc_datetime() ))
        correct_key = authenticator.generate( orbit_time_rcv.utc_datetime()  )

        answer = input() 

        if( answer == correct_key ):
            print("Correct - communication established")
        else: 
            print("Wrong")
            return False

    return True
def print_tle( file_name , satellite ):
    f = open( file_name , "rt")
    lines = f.readlines()
    lines = [x.rstrip() for x in lines]
    sat_start = lines.index( satellite )
    
    for k in range(1,3):
        print( lines[sat_start+k])


    f.close()

if __name__ == "__main__":
    try:
        success = challenge( "NOAA 6 [-]", 'data.tle')
        if( success ):
            print("You are a master of spacetime!")
            print("Complete!")  
            flag = os.getenv('FLAG')
            print("Here is your flag: {}".format( flag ))
        else:
            print("Later.")
    except TimeoutError:
        print("Timeout.......bye")