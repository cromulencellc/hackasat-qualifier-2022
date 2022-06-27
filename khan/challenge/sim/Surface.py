from Basilisk.utilities import simulationArchTypes
from Basilisk.architecture import messaging

import numpy as np

class Surface(simulationArchTypes.PythonModelClass):
    """
    """
    def __init__(self, planet,  modelName, modelActive=True, modelPriority=-1):
        super(Surface, self).__init__(modelName, modelActive, modelPriority)

        # Input message sturcture
        self.pvtMsg = messaging.SCStatesMsgReader()
        self.planet = planet
        self.miss_limit = 1000.0 # Must hit the LZ within this distance
        self.shock_limit = 8
        self.last_pos = None 


    def reset(self, currentTime):
        # Nothing actually happens here -because we dont do anything
        return

    def updateState(self, currentTime):
        # Get my message data
        position = self.pvtMsg().r_BN_N
        velocity = np.linalg.norm( self.pvtMsg().v_BN_N )
        altitude = np.linalg.norm(position ) - (self.planet.radEquator )
     
     
        total_impulse = 1.0 * velocity 
        if( (altitude < 0 ) and (total_impulse > self.shock_limit) ):

            print("You hit the planet and destroyed the probe at {} m/s".format( total_impulse ))
            raise ImpactError
        if( (altitude < 0 ) and (total_impulse <= self.shock_limit )):
            miss = 0 
            if( miss < self.miss_limit ):
                print("What a great landing")
                raise Landing
            else:
                print("You missed the landing zone")
                raise Missed
        self.last_pos = position
        return

class ImpactError( Exception ):
    pass

class Landing(Exception):
    pass

class Missed(Exception):
    pass