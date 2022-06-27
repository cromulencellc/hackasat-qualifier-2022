from Basilisk.utilities import simulationArchTypes
from Basilisk.architecture import messaging

import numpy as np
class BurnUpError( Exception ):
    pass
class HeatShield(simulationArchTypes.PythonModelClass):
    """
    """
    def __init__(self, modelName, modelActive=True, modelPriority=-1):
        super(HeatShield, self).__init__(modelName, modelActive, modelPriority)

        # Input message sturcture
        self.atmMsg = messaging.AtmoPropsMsgReader()
        self.pvtMsg = messaging.SCStatesMsgReader()
        self.popMsg = messaging.DeviceCmdMsgReader()
        self.heat_shield_on = True
        # Output body torque message name
        # 
        self.dyn_pressure_limit = 450

    def reset(self, currentTime):
        # Nothing actually happens here -because we dont do anything
        return

    def updateState(self, currentTime):
        if( True == self.heat_shield_on):
            pop = ( self.popMsg().deviceCmd > 0 ) 
            if( True == pop ):
                self.heat_shield_on = False 
            pass
        else:
            rho = self.atmMsg().neutralDensity
            v = np.linalg.norm( self.pvtMsg().v_BN_N )
            q = 0.5 * rho * v * v
            if( q > self.dyn_pressure_limit ):
                
                print("The satellite burnt up in the atmosphere")
                raise BurnUpError
        return


