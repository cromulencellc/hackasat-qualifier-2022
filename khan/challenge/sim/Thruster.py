from Basilisk.utilities import simulationArchTypes, macros
from Basilisk.architecture import messaging

import numpy as np
def clamp( inData , limit ):
    out = []
    for item in inData:
        if( item > limit ):
            val = limit 
        elif( item < -limit ):
            val = -limit
        else: 
            val = item 
        out.append( val )
    return np.array(out)
class Thruster(simulationArchTypes.PythonModelClass):
    """
    """
    def __init__(self, modelName, modelActive=True, modelPriority=-1):
        super(Thruster, self).__init__(modelName, modelActive, modelPriority)
        # 
        self.last_t = 0
        
        self.remaining = 200
        self.full_tank=  200 
        self.force_limit = 20
        # Input message sturcture
        self.inForceMsg = messaging.CmdForceInertialMsgReader()

        # Output body torque message name
        # 
        self.outForceMsg = messaging.CmdForceInertialMsg()
        
    def status(self):
        if( self.remaining > 0 ):
            return "Fuel available"
        elif( self.remaining == self.full_tank ):
            return "Fuel Full"
        else:
            return "Empty"
    def reset(self, currentTime):
        # Nothing actually happens here -because we dont do anything
        return

    def updateState(self, currentTime):
        dt = ( currentTime - self.last_t) * macros.NANO2SEC 
        
        # If we have fuel use it - otherwise we cant do anything
        if( self.remaining > 0  ):
            cmd = self.inForceMsg().forceRequestInertial
            limited = clamp( cmd , self.force_limit) 
            total_impulse = np.linalg.norm( limited )  *dt
   
            if( total_impulse  > self.remaining):
                ratio = self.remaining / total_impulse
           
                limited =  ratio * limited 

        else:
            limited = np.array( [0,0,0] )

        self.remaining -= dt * np.linalg.norm( limited ) 
        payload = messaging.CmdForceInertialMsgPayload()
        payload.forceRequestInertial = limited 
        self.outForceMsg.write(payload , currentTime, self.moduleID)
        self.last_t = currentTime
        return