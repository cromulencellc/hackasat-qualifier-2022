import zmq
import time 
import numpy as np
import struct
class pid:
    def __init__(self, Kp, Ki, Kd ):
        self.Ki = Ki
        self.Kp = Kp 
        self.Kd = Kd 
        self.integral = 0 
        self.last  = 0 
        self.count =  0
    def update( self , value ):
        if( self.count == 0 ):
             derivative  = 0
            # we need 1 iteration for the derivative to work
        else:    
            derivative  = self.Kd * (value - self.last)
        self.integral += self.Ki *value

        out = self.integral + ( self.Kp * value ) + derivative
        self.last = value
        self.count +=1
        return out 
class fsw():
    def __init__(self):
        self.mode = "reenter"
        self.engine_ctl = pid( Kp=.1 , Ki=0.01 , Kd=0.1)
        self.heat_vel_limit = 1
        self.pop_heat_shield = False
        self.pop_chute = False
        earth_radius = 13120
        target_altitude = 100
        self.peri_target = earth_radius + target_altitude 
        self.g_limit = 15
        pass
    def input_binary(self , message ): 
        
        if( len(message) != 7*4 ):
            print("Weird {}".format(len(message)))
        data = struct.unpack( "<7f", message)
        
        self.pos = np.array( data[0:3] )*(1.60934)
        self.vel = np.array( data[3:6]) *(1.60934)
        self.g_monitor = -np.array( data[6])
    def output_binary(self):
        command = list( self.thrust ) 
        chute = 1 if self.pop_chute else 0  
        shield =  1 if self.pop_heat_shield else 0 
        command.append(chute)
        command.append(shield)
        message = struct.pack("<fffii", *command )
        return message
    def run( self ):
        
        if( self.mode == "reenter" ):
            self.reenter()
            pass

        elif( self.mode == "wait_for_cool"):
            self.wait_cool()
        elif( self.mode == "wait_for_chute"):
            self.wait_chute()
            pass
        elif( self.mode == "land"):
            self.land()
            pass
        else:
            print("Bad mode")
            raise ValueError
    def reenter(self):
        mu= 2527105.1264
        h = np.cross( self.pos , self.vel )
        h_norm = np.linalg.norm( h )
        e_bar = ( np.cross( self.vel , h) / mu ) - ( self.pos / np.linalg.norm(self.pos))
        e =  np.linalg.norm( e_bar )
        p = h_norm * h_norm / mu 
        a = p * ( 1 - e*e )
        peri = a * ( 1 - e )        
        peri_error = peri- self.peri_target
        thrust_scalar  = self.engine_ctl.update( peri_error )
        direction =  - self.vel / np.linalg.norm(self.vel)
        # Outputs 
        self.thrust = thrust_scalar * direction
        print("Peri: {}".format( peri_error ) ) 
        if( np.abs( peri_error ) < 1 ):
            print("Manuever complete")
            self.mode = "wait_for_cool"
            self.thrust = [0,0,0]
    def wait_cool( self ):
        v_mag = np.linalg.norm( self.vel )
        if( v_mag < self.heat_vel_limit ):
            print( "Heat shield popped ")
            self.mode = "wait_for_chute"
            self.pop_heat_shield = True
    def wait_chute( self ):
        
        if( self.g_monitor  < self.g_limit  ):
            print("Chute deployed")
            self.pop_chute = True 
            self.mode = "land"
    def land( self ):
        self.pop_chute = False 
        pass
def run( state_port , thrust_port ):
    context = zmq.Context()
    zIn = context.socket(zmq.PULL)
    zIn.connect("tcp://localhost:{}".format( state_port ) )
    zOut = context.socket( zmq.PUSH)
    zOut.connect("tcp://localhost:{}".format( thrust_port ))

    sw = fsw()
    while(True):
        inMsg = zIn.recv( )
        sw.input_binary( inMsg )
        sw.run( )
        outMsg = sw.output_binary()
        zOut.send(outMsg)
if __name__ == "__main__":
    run(5001,5000)