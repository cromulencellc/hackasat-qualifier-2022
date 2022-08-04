import numpy as np
import sys
import os
from datetime import datetime, timezone
import cesium
import gmat
from timeout import timeout, TimeoutError
# Default timeout is set to 240 just in case gmat runs slower on the load
time = int(os.getenv("TIMEOUT",240))


@timeout(time)
def challenge(  ):
    LunarRadius = 1750
    EarthRadius = 6378
    L4_Proximity = 200000
    L4_arrival_date = datetime( year=2022 , month=4 , day=1, tzinfo= timezone.utc )
    start_date = datetime( year=2022, month=1 , day=22, tzinfo= timezone.utc)
    stop_date = datetime( year=2022 , month=9,  day=1 , tzinfo= timezone.utc)
    dv_limit = 2.0
    # booster conditions:
    t = "2022 Jan 21.0"
    a = 295911.9425900026
    e = 0.8898246770000006
    inc = 27.0092517
    raan = 17.82128320000001
    aop = 149.2278077
    M = 0.1621535087


    #

    gmat_exe = gmat.Gmat("./GMAT/R2020a")
    gmat_template = gmat.GmatTeplate()
    
    gmat_template.set_start_stop( start_date , stop_date )
    gmat_template.add_log('Booster', "EarthMJ2000Eq", "booster")
    gmat_template.add_log('Luna', "EarthMJ2000Eq", "moon")
    gmat_template.add_log('Booster', "Moon" , "booster_moonframe")
    gmat_template.add_log('Booster', "L4" , "booster_l4frame")
    service_port = os.getenv("SERVICE_PORT",12000)
    service_host = os.getenv("SERVICE_HOST","localhost")
    print("Save our mining operation!")
    
    print("The orbital elements for the booster are: ")
    print("Gregorian TT: {} ".format(t))
    print("Semimajor axis: {} km".format(a))
    print("Eccentricity: {}".format(e))
    print("Inclination: {} deg".format( inc ))
    print("RAAN: {} deg".format( raan ))
    print("Argument of periapsis: {} deg".format(aop))
    print("Mean anomaly: {} ".format(M))
    print("--------------------------------------------")
    print("Provide a list of maneuvers to put the booster at L4 and keep it nearby")
    print("If your manuevers are valid you can view the trajectory at {}:{}".format(service_host, service_port) )
    print("You can manuever as many times as you want but you only have {} km/s of deltaV left".format( dv_limit))
    print("Time is in Gregorian TT:  YYYY-MM-DD HH:MM:SS.sss")
    print("Manuevers are in Earth Centered Mean of J2000 Equitorial Coordinate system")
    
    print("Input your manuevers in the following format: ")
    print("Time , Delta VX, Delta VY, Delta VZ")

    print("Enter 'DONE' when you want have added all your maneuvers")

    keep_going = True 
    while( keep_going ):
        
        print("Input next maneuver:")
        entry = input()
        entry = entry.replace("\n","")
        if( "DONE" == entry  ):
            keep_going = False
        else:
            gmat_template.add_maneuver( entry )
    # Check that we have enough delta v for the mission
    total_dv = gmat_template.get_total_dv()
    if( total_dv > dv_limit ):
        print("Incorrect")
        print("We dont have the fuel to do these maneuvers")
        return False
    valid_times = gmat_template.validate_order()
    if( False == valid_times  ):
        print("Maneuver times must be after the epoch and be given in order")
        return False
    
    script_name = "./gmat_scripts/mission.script"
    gmat_template.render( template_directory="./gmat_scripts" , template_filename="gmat_template.script" ,  out_path=script_name)

    print("Calculating..... (this may take a few seconds) ", flush=True)
    
    gmat_exe.run_script( script_name )
    print("Checking your trajectory.... (this may also take a few seconds)" , flush=True)
    booster_earth = gmat_exe.get_log('booster.txt')
    booster_moon = gmat_exe.get_log('booster_moonframe.txt')
    booster_L4 = gmat_exe.get_log('booster_l4frame.txt')
    moon = gmat_exe.get_log('moon.txt')
    
    
    earth_ok = check_proximity( data=booster_earth , min_proximity=EarthRadius , loc="Earth" , snark="The booster re-entered the earth, we'll definitely get fined for that")
    moon_ok = check_proximity( data=booster_moon , min_proximity=LunarRadius , loc="Moon" , snark="You crashed into the moon. Space mining ops had to be evacuated.")
    l4_ok = check_proximity( data=booster_L4 , max_proximity=L4_Proximity , loc="L4" , from_date=L4_arrival_date,  snark="Keep the booster near L4 please") 
    # Make template
    booster_czml = cesium.CesiumOrbitTemplate()
    booster_czml.set_orbit( booster_earth , decimation=3)
    booster_czml.set_window( start_date, stop_date ) 
    booster_czml.render( template_directory="viewer/czml", template_filename="booster.template", out_path="viewer/czml/booster.czml", name="Booster")
    
    moon_czml = cesium.CesiumOrbitTemplate()
    moon_czml.set_orbit( moon , decimation=3)
    moon_czml.set_window( start_date, stop_date ) 
    moon_czml.render( template_directory="viewer/czml", template_filename="booster.template", out_path="viewer/czml/moon.czml", name="Moon")
    
    result = earth_ok and moon_ok and l4_ok
    
    return result

def check_proximity( data , min_proximity=-np.Inf , max_proximity=np.Inf , from_date=datetime(year=1, month=1,day=1) , to_date=datetime(year=4000,month=1,day=1),  loc="" , snark ="" ):
    for item in data:

        time = item["time"]
        position = np.array( [ item["X"], item["Y"], item["Z"]])
        d_to_center =  np.linalg.norm( position )
        time_str = time.strftime("%Y %b %D %H:%m:%S.%f ")
        from_date = from_date.replace( tzinfo=timezone.utc)
        to_date = to_date.replace( tzinfo=timezone.utc)
        dt1 = time - from_date
        dt2 = time - to_date
        if( (dt1.total_seconds() > 0 ) and (dt2.total_seconds()<0)):
            if( d_to_center < min_proximity ):
                print("Incorrect")
                print("Proximity alarm - you got to close to {} at {}".format(loc,time_str))
                print(snark)
                return False
            if( d_to_center > max_proximity ):
                print("Incorrect")
                print("Proximity alarm - you got too far from {} at {}".format(loc, time_str))
                print(snark)
                return False
    return True
def game_over():
    f = open("game_over.txt")
    lines  = f.readlines()
    for line in lines:
        print( line )
    f.close()



if __name__ == "__main__":
    try:
        
        result = challenge()

        
    
        if( True == result ):
            print("Complete!")
            print("Flag: {}".format(  os.getenv("FLAG") ))
        else:
            print("Bye.")
    finally:
        print("Qutting")
    sys.exit(0)