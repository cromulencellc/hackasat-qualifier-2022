from curses import COLOR_RED
from os import sync
import skyfield.api as sf
import numpy


class OrbitalClock:
    def __init__(self, satellite , tle_file):
        sats = sf.load.tle_file( tle_file)
        sat_dict = {sat.name: sat for sat in sats}
        self.satellite = sat_dict[satellite]
        pass
    def dt_from_earth( self,  time , sync_time ):
        C = 299792.458 #km/sec
        # Compute the clock corrections based on a circular orbit
        n = self.satellite.model.no_kozai / 60 
        MU =398600.4418 #km^3 / s^2 (EARTH)
        R_E = 6378 #km
        period = 2*numpy.pi/n
        semi_major = numpy.cbrt( MU * numpy.square( (period/(2*numpy.pi)) )  ) 
        
        circ_vel = numpy.sqrt( MU * 2/ semi_major )
        dU = - ( MU /  semi_major) + (MU/R_E)
        potential_drift = dU / (C*C)
        special_drift =   numpy.square(circ_vel / (2*C) )
        drift_rate = -special_drift  + potential_drift
        # CHECK MATH AGAINST
        # https://en.wikipedia.org/wiki/Error_analysis_for_the_Global_Positioning_System#Calculation_of_time_dilation
        #print("N: {}".format( n ))
        #print("Period: {} ".format(period))
        #print("Potential Drift Rate: {}".format(potential_drift))
        #print("Special Drift Rate: {}".format(special_drift))
        #print("Dift rate {}".format( drift_rate))
        #print("R_sat: {}".format(semi_major))
        
        time_since_sync = time.utc_datetime() - sync_time.utc_datetime()
        avg_correction = drift_rate * time_since_sync.total_seconds()
        
        # Add the eccentricity based correction      
        obs = self.satellite.at(time)
        pos = obs.position.km
        vel = obs.velocity.km_per_s
        eccentricity_correction = -2 * numpy.dot( pos , vel ) / ( numpy.square(C) )
        #print("ecc corr {}".format( eccentricity_correction))

        correction = avg_correction + eccentricity_correction
        #print("Relativity: {}".format(correction) )
        return correction


if __name__ == "__main__":
    print("Relativity test")
    ts = sf.load.timescale()

    clock = OrbitalClock( "GPS BIIR-4  (PRN 20)" , "gps.tle")
    synchTime = ts.utc(2021 , 1, 27 )
    
    #for k in range( 0 , 24):
    time = ts.utc(2021 , 1 , 28 , 0 , 0 , 0 )
    corr = clock.dt_from_earth( time, synchTime )
    print(corr) 
    
    # GPS satellites expect:
    #    +45.8us of gravitational potential time drift
    #    -7.21us of special relativity (velocity) time drift 
    # Per day .... this should print out 3.84e-5 seconds if correct