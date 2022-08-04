"""Cross-Link problem generator23

.. moduleauthor:: Mike Walker

"""
import skyfield.api as sf
import numpy as np
import datetime
from . import tlehelp
import argparse
import sys
import random
class CrossLinkGen:
    """ CrossLinkGen class is used as a tool to generate cross link data and put it out to the user based on the following equation:

    Terminology:
    Satellite name - The name of the satellite in the TLE database
    Observer: The satellite that is communicating with other satellites
    Constellation: All the satellites in the TLE file with the exception of the observer

    """
    def __init__(self, tleDatabase , seed , r_noise , rr_noise , bias = 0):
        # load and store the TLE 
        sats = sf.load.tle_file( tleDatabase)
        self.clock_bias = bias
        
        self.satellites = {sat.name: sat for sat in sats}

        self.r_noise = r_noise
        self.rr_noise = rr_noise
        self.available = tlehelp.available(tleDatabase)

        random.seed( seed )
        pass
    
    
    def generate(self , observer , startUTC, length , timeIncrement ):
        """
        Generate measurements between the observer satellite and every other satellite in the tle database between the start and end times indicated

        :param observer: Generate cross link measurements between this satellite and all other satellites in the constellation
        :param startUTC: A datetime.datetime object at which the measurements should be started
        :param length: length of the set of measurements (seconds)
        :param timeIncrement: time between measurements (seconds)
        """
        if( observer not in self.available ):
            raise("The observer you selected is not in the database bro")
        
        
        # Generate truth data
        data = dict()
        ts = sf.load.timescale()
        startTime = self.satellites[observer].epoch 
        stopTime = startTime + datetime.timedelta( seconds = length ) 
        times = ts.linspace( startTime , stopTime , int(length/timeIncrement) )
        #TODO: filter down to a more minimal number of satellites so users cant just look at the ranging data and see which satellite isnt there
        for satellite in self.available:
            
            if( satellite == observer):
                pass
            else:
                measurements = self.generateSingleLink( observer, satellite , times  )
                data[satellite] = measurements

        # generate noisy data
        # TODO

        self.data = data
        pass
        # Generate a link between an observer and responder for a time vec
    def generateSingleLink( self , observer , responder , times  ):
        """
        Generates the observations for a cross link between two satellites.

        :param observer: The satellite name of the satellite that is observing the ranging measurement
        :param responder: The satellite that is communicating with the observer
        :param times: A python array of datetime objects at which the measurements should be gneerated
        :return: A vector of tuples. A single entry in the vector represents one of the times requested. The tuple is arrange as (time ,range ,range rate)
        """
        
        orbit1 = self.satellites[observer]
        orbit2 = self.satellites[responder]
        outVector = []
        for time in times:
            #orbit1 = orbital.Orbital( satellite=observer , tle_file=self.tle)
            #orbit2 = orbital.Orbital( satellite=responder, tle_file=self.tle)

            state1 = orbit1.at( time )
            state2 = orbit2.at( time )
            #state1 = orbit1.get_position( time , normalize=False)
            #state2 = orbit2.get_position( time, normalize=False )

            r1 = state1.position.km
            v1 = state1.velocity.km_per_s
            r2 = state2.position.km
            v2 = state2.velocity.km_per_s
            # Calculate visibility
            R1 = np.linalg.norm( r1 )
            R2 = np.linalg.norm( r2 )
            RE = 6378 # radius at the equator
            mask_extra = 5 # mask all satellites this many deg above earth's limb
            earth_mask = np.degrees(np.arccos( RE / R1 )) + mask_extra
            angle_to_target = np.degrees( np.arccos( np.dot( r1 , r2 )/ (R1*R2) ) ) 
            if( angle_to_target  < earth_mask ):
                out = self.computeLOS( r1,v1,r2,v2)
                newTup = ( time , out[0] , out[1])
                outVector.append(newTup)
            else:
                pass
        return outVector 
            



    def computeLOS( self , r1,v1, r2,v2):
        """ 

        Helper function to compute line of sight measurements between to points moving at given velocities.

        :param r1: position vector of the first object
        :param r2: position vector of the second object
        :param v1: velcoity vector of the first object
        :param v2: velcoity vector of the second object
        :return: A tuple containing range and range rate

        The range is calculated as:

        .. math::  \\rho = \lvert  \overrightarrow{r_2} - \overrightarrow{r_1}  \lvert + \\eta

        Where:

        .. math:: \\eta \sim \\mathcal{N}\left( 0 , \sigma^2_{\\rho} \\right) 


        The range rate is calculated as:

        .. math:: \\Delta R = \overrightarrow{r_2} - \overrightarrow{r_1}
        
        .. math:: \\Delta V = \overrightarrow{v_2} - \overrightarrow{v_1}

        .. math::  \\dot{\\rho} = \\frac{ \overrightarrow{\\Delta R} - \overrightarrow{\\Delta V}  }{ \\rho } + \\nu

        Where:

        .. math:: \\nu \sim \\mathcal{N}\left( 0 , \sigma^2_{ \\dot{\\rho}} \\right) 


        Assumptions:
        
        - The coordinates of r1, r2, v1, v2 are measured in the same reference frame "E"
        - The velocity vectors v1, v2 are measured with respect to the same reference fame "I"
        - "E" and "I" are not necessarily equivalent reference frames but may be
        """
        C = 299792.458 # Speed of light km/s

        dR = r2-r1
        dV = v2-v1
        noiseR = random.gauss(0, self.r_noise )
        noiseRR = random.gauss(0, self.rr_noise )

        range = np.linalg.norm( dR ) + noiseR  + ( C * self.clock_bias )
        rangeRate =   ( np.dot( dR , dV) / range ) + noiseRR
        return (range, rangeRate)

    def dump(self , filename , header=None):
        """
        Dump the generated measurements to a file in csv format.

        :param filename: path of the file you want the measurments dumped into
        :param truth: If set to true this function will dump truth measurments, otherwise the measurements will have noise
        The format of the file is:
        time (utc) , range (km) , range rate (km/s)
        """
        if( filename ):
            f = open(filename,'wt')
        else:
            f= sys.stdout
        
        if( self.clock_bias == 0 ):
            header = "Observations {}\n Time, Range, Range Rate\n"
        else: 
            header = "Observations {}\n Time, Pseudorange, Pseudorangerate\n"
        data = self.data
    
        for satellite , timeseries in data.items():
            if( len( timeseries ) > 0 ):
                f.write(header.format(satellite))
                for entry in timeseries:
                    # data is a tuple of three scalars time , range  , range rate
                    time = entry[0].utc_strftime("""%Y-%m-%dT%H:%M:%S.%f%z""")
                    range = entry[1]
                    rangerate = entry[2]
                    line = "{}, {}, {}\n".format( time , range , rangerate) 
                    f.write( line )
        if( f is not sys.stdout ):
            f.close()
    def satsViewed( self ):
        out = []
        for sat,timeseries in self.data.items():
            if( len(timeseries) > 0):
                out.append( sat )
        return out


if __name__ == "__main__":
    timeFormat=  """%Y-%m-%dT%H:%M:%S.%f%z""" 
    parser = argparse.ArgumentParser(description='Generate data for the cross-link problem')
    parser.add_argument("--tle", dest="tle", required=True)
    parser.add_argument("--satellite", dest="satellite", required=True)
    parser.add_argument("--range-noise", dest="rng_noise", type=float , default=0.0 )
    parser.add_argument("--range-rate-noise", dest="rr_noise", default=0.0)
    parser.add_argument("--start", default=datetime.datetime.utcnow().strftime(timeFormat))
    parser.add_argument("--length",type=float, default =10000 )
    parser.add_argument("--dt" , default=1000 , type=float)
    parser.add_argument("--seed", type=int , default=1)
    parser.add_argument("--output", default="out.txt")
    parser.add_argument("--n", type=int , default=6   )
    inputs =parser.parse_args(sys.argv[1:])

    print("Example orbit ranging")
    gen = CrossLinkGen( inputs.tle , inputs.seed , inputs.rng_noise , inputs.rr_noise )
    startTime = datetime.datetime.strptime( inputs.start , timeFormat )

    gen.generate( inputs.satellite , datetime.datetime.utcnow() , inputs.length , inputs.dt)
    gen.dump(filename=inputs.output )


