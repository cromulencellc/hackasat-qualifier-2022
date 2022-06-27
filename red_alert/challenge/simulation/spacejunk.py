import skyfield.api as sf
import skyfield.elementslib as elements
from sgp4.api import Satrec , WGS84
import numpy as np
import yaml 
import datetime
import collision
class SpaceJunk:
    def __init__( self, tle_file , sim_time ):
        sats = sf.load.tle_file( tle_file)
        self.satellites = {sat.name: sat for sat in sats}
        self.junk = dict()
        self.junk_number = 0
        self.timescale = sf.load.timescale()
        self.time = sim_time 
        

    def get_junk(self):
        return self.junk
    def create_junk( self, collision_file  ):
        f = open(collision_file , 'rt')
        text = f.read()
        f.close()
        collisions = yaml.safe_load( text  )

        for item in collisions["collisions"]:
            sat = item["satellite"]
            time_in   = item["time"]
            sat = self.satellites[sat]
            time =  self.time + datetime.timedelta( seconds=time_in)
            state = sat.at( time ) 
            position = state.position
            velocity = state.velocity
            #print("Collision at {} at time {}".format( position.km , time.utc_strftime()))
            self.single_junk( time , position ,velocity)
            
    def destroy( self , name ):
        print("{} destroyed dy lasers".format( name ))
        del self.junk[ name ]
    def single_junk( self , collision_time , position , velocity ):
        mu_km_s = 398600.8
        vel_rot = np.eye(3) 
        th = 0.1
        v_scale = 1.1
        vel_rot[0][0]= 1
        vel_rot[0][1]= 0
        vel_rot[0][2]= 0
        vel_rot[1][0]= 0
        vel_rot[1][1]= np.cos( th )
        vel_rot[1][2]= np.sin( th )
        vel_rot[2][0]= 0
        vel_rot[2][1]= -np.sin(th)
        vel_rot[2][2]= np.cos(th)
        velocity_new = vel_rot @ (velocity.km_per_s * v_scale).reshape(3,1)

        o = elements.OsculatingElements(position, sf.Velocity(km_per_s=velocity_new.reshape(3,)), collision_time, mu_km_s)
        
        name = "JUNK_{}".format( self.junk_number )
        no_kazi = np.sqrt( mu_km_s / np.power( o.semi_major_axis.km, 3 )  ) * 60 # multiple n by 60 to transform from rad/s to rad/minute
        satrec = Satrec()
        epoch =  self.timescale.utc( 1949,12,31,0,0,27)# put in those stupid leap seconds :(
        delta = collision_time - epoch
        satrec.sgp4init(
            WGS84,           # gravity model
            'i',             # 'a' = old AFSPC mode, 'i' = improved mode
            self.junk_number,               # satnum: Satellite number
            delta,       # epoch: days since 1949 December 31 00:00 UT ( mar 18 2022)
            0,      # bstar: drag coefficient (/earth radii)
            0, # ndot: ballistic coefficient (revs/day)
            0.0,             # nddot: second derivative of mean motion (revs/day^3)
            o.eccentricity,       # ecco: eccentricity
            o.argument_of_periapsis.radians, # argpo: argument of perigee (radians)
            o.inclination.radians, # inclo: inclination (radians)
            o.mean_anomaly.radians, # mo: mean anomaly (radians)
            no_kazi, # no_kozai: mean motion (radians/minute)
            o.longitude_of_ascending_node.radians, # nodeo: right ascension of ascending node (radians)
            
        )

        
        sat = sf.EarthSatellite.from_satrec(satrec, self.timescale)
        #print('Epoch:', sat.epoch.utc_jpl())
        #print("Pos Collison: {}".format( sat.at( collision_time ).position.km))
        self.junk[name] = sat
        self.junk_number += 1 
    def at( self , time_in ):
        out = dict()
        t =  time_in 
        for name,sat in self.junk.items():
            state = sat.at( t )
            out[name] = state 
        return out 

        
if __name__ == "__main__":
   c =  SpaceJunk( "sats.tle" )
   c.single_junk( "collisions.yml", 1.2 , )
