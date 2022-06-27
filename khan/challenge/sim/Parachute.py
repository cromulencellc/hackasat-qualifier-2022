from Basilisk.utilities import simulationArchTypes, macros
from Basilisk.architecture import messaging

import numpy as np

class Parachute(simulationArchTypes.PythonModelClass):
    """
    """
    def __init__(self, drag, modelName, modelActive=True, modelPriority=-1):
        super(Parachute, self).__init__(modelName, modelActive, modelPriority)

        # Input message sturcture
        self.drag = drag 
        self.parachute_deployed = False
        self.parachute_damaged = False
        self.popMsg = messaging.DeviceCmdMsgReader()
        self.pvtMsg = messaging.SCStatesMsgReader()

        # Output body torque message name
        # 
        self.shock_limit = 150
    def status( self ):
        if( self.parachute_damaged ):
            return "DAMAGED"
        elif( self.parachute_deployed ):
            return "DEPLOYED"
        else:
            return "STOWED"
    def reset(self, currentTime):
        # Nothing actually happens here -because we dont do anything
        return

    def updateState(self, currentTime):
        pop = ( self.popMsg().deviceCmd > 0 ) 
        accel = self.pvtMsg().nonConservativeAccelpntB_B 
        total_accel = np.linalg.norm( accel )
        if( True == pop):

            self.parachute_deployed = True 
        if( (True == self.parachute_deployed)
            and ( False == self.parachute_damaged ) )  :
            if( True == self. parachute_damaged ):
                self.drag.coreParams.projectedArea = 0
            if( True == pop ):
                self.drag.coreParams.projectedArea = 15
            if( (False == self.parachute_damaged) and 
                ( total_accel > self.shock_limit )):
                print("Parachute damaged at {}".format( currentTime * macros.NANO2SEC / 3600 ))
                self.parachute_damaged = True 
        else:
            self.drag.coreParams.projectedArea = 0
        return
