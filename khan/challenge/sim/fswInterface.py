import zmq 
from Basilisk.utilities import simulationArchTypes
from Basilisk.architecture import messaging
import struct
import numpy as np
class NavIntrface( simulationArchTypes.PythonModelClass):
    """
    An interface that allows communication of navigation data from the sim to the flight software

     _________                _________
    |         |              |         |
    |  Sim    |  == ZMQ ==>  |  FSW    |
    |_________|              |_________|

    This interface is a basilisk simulation model and satisfies the BASILISK (SIM) side of the ZMQ contract
    """
    def __init__(self ,port, modelName, modelActive=True, modelPriority=-1):
        super(NavIntrface, self).__init__(modelName, modelActive, modelPriority)
        self.context = zmq.Context()
        self.zSocket = self.context.socket(zmq.PUSH)
        addr = "tcp://*:{}".format(port)
        self.zSocket.bind(addr)
        # Input message sturcture
        self.inMsg = messaging.SCStatesMsgReader()

        # Output messages
        # 


    def reset(self, currentTime):

        return

    def updateState(self, currentTime):
       

        msg = self.inMsg()
        # Lol - the sensor uses freedom units (miles and miles/sec) :(
        pos = np.array( msg.r_BN_N ) / ( 1000.0 * 1.60934) 
        vel =  np.array(msg.v_BN_N ) / ( 1000.0 * 1.60934)
        accel =  np.array( msg.nonConservativeAccelpntB_B ) 
        # oops someone installed this thing upside down! because all our force in this problem is anti-velocity
        # lulz!
        g_sensor =   -np.linalg.norm( accel   ) 
        
        out = [ pos[0],pos[1],pos[2] , vel[0],vel[1],vel[2], g_sensor]

        data = struct.pack( "<7f" , *out)
        self.zSocket.send( data )
        return
class EngineInterface(simulationArchTypes.PythonModelClass):
    """
    An interface that allows control of the engine in the simulation from "detached" FSW by use of ZMQ

     _________                _________
    |         |              |         |
    |  FSW    |  == ZMQ ==>  |  Sim    |
    |_________|              |_________|

    This interface is a basilisk simulation model and satisfies the BASILISK (SIM) side of the ZMQ contract
    """
    def __init__(self ,port, modelName, modelActive=True, modelPriority=-1):
        super(EngineInterface, self).__init__(modelName, modelActive, modelPriority)
        self.context = zmq.Context()
        self.zSocket = self.context.socket(zmq.PULL)
        addr = "tcp://*:{}".format(port)
        self.zSocket.bind(addr)
        # Input message sturcture


        # Output messages
        self.forceCmdMsg = messaging.CmdForceInertialMsg()
        self.chuteCmdMsg = messaging.DeviceCmdMsg()
        self.shieldCmdMsg = messaging.DeviceCmdMsg()

        # 


    def reset(self, currentTime):

        return

    def updateState(self, currentTime):

        message = self.zSocket.recv()
        
        if( len(message) != (4*5) ):
            print("That doesnt look right?! {}".format(len(message)))
        unpacked = struct.unpack( '<fffii' , message )
        payload = messaging.CmdForceInertialMsgPayload()
        chutePayload = messaging.DeviceCmdMsgPayload()
        shieldPayload = messaging.DeviceCmdMsgPayload()
        payload.forceRequestInertial = unpacked[0:3] 
        chutePayload.deviceCmd = unpacked[3]
        shieldPayload.deviceCmd = unpacked[4]
        self.forceCmdMsg.write(payload, currentTime, self.moduleID)
        self.chuteCmdMsg.write(chutePayload, currentTime, self.moduleID) 
        self.shieldCmdMsg.write(shieldPayload , currentTime, self.moduleID)


        return