import satellite
import spacejunk
import database
import datetime
from skyfield.api import utc
import skyfield.api as sf
import threading
import time
from flask import Flask
import collision 
class SimApp( ):
    def __init__( self  ):
        # Webhook
        # Lets be safe!
        self.lock = threading.Lock()
        # Simulation stuff
        ts = sf.load.timescale()
        sim_time =  ts.utc( 2022, 3,17,0,0,0)
        self.constellation = satellite.Constellation("sats.tle", sim_time )
        self.junk = spacejunk.SpaceJunk("sats.tle" , sim_time )
        self.junk.create_junk("collisions.yml")
        self.db = database.SimDatabase(ip="postgres",port=5432,user="player",pw="password",db="red_alert") 
        self.db.create_sat( self.constellation.get_sats() )
        self.db.create_laser()
        self.db.create_detector()
        self.dt =30
        self.t = sim_time
        self.laser_range = 1000
        self.collision_range = 100
        self.detector_range = 5000
    def handle_hook( self, instrument , on ):
        self.lock.acquire( blocking = True )
        sats = self.constellation.get_sats()
        sat = sats["SAT_1"]# hardocded bc there is only1
        if( instrument == "laser"):
            if( True == on ):
                sat.sharks_with_lasers(True)
                pass
            else:
                sat.sharks_with_lasers(False)
                pass
        elif( instrument == "detector"):
            if( True == on ):
                sat.detector( True )
                pass
            else:
                sat.detector( False )
                pass
        else:
            print("Invalid instrument")
        self.lock.release()

    def run_sim( self , flag ):
        N = 600 
        self.db_time = datetime.datetime.utcnow()

        for k in range(N):
            # Make sure that when we run the sim we arent dealing w a webhook
            self.lock.acquire( blocking=True )
            self.t += datetime.timedelta( seconds=self.dt )
            self.db_time += datetime.timedelta( seconds=self.dt )
            print( "Current time: {}".format( self.db_time.strftime("%Y-%m-%d %H:%M:%S")))
            # Let the physics run for a time step
            self.constellation.propagate( self.dt )
            junk_data = self.junk.at( self.t  )
            # Check for collisions
            hits = collision.collisions( self.constellation.get_sats() , junk_data ,self.dt , self.collision_range  )
            # Check for satellite overheat or power outage
            # Do the lasers destroy something?!
            
            laser_targets = collision.collisions( self.constellation.get_sats() , junk_data ,self.dt , self.laser_range  )
            
            # Handle the collisions first 
            for item in hits:
                sat = item["Sat"]
                # Any sort of hit will hurt the satellite
                self.constellation.destroy(sat)
            # Handle the laser targets next
            laser_available = True
            for item in laser_targets:
                sat = item["Sat"]
                junk = item["Junk"]
                lasers = self.constellation.get_sats()[sat].get_laser()
                if( True == lasers[0] and laser_available):
                    self.junk.destroy( junk )
                    laser_available = False

            self.constellation.run_detector( junk_data )
            # Post data to database 
            self.db.post_sats(  self.constellation.get_sats() , self.db_time )    
            self.db.post_laser( self.constellation.get_sats() , self.db_time )
            self.db.post_detector( self.constellation.get_sats() , self.db_time )
            self.lock.release()
            # Make sure we do this sleep after we release the lock.
            time.sleep(1)
        # you did it so you get the flag!
        print("You survived!")
        print(flag)
        

