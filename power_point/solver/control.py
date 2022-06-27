import socket 
import time
import struct
import zmq
import numpy as np
import matplotlib.pyplot as plt

class controller:
    def __init__(self , x0, Kp, Ki):
        self.K = Kp
        self.Ki = Ki
        self.x = x0 
        self.y= 0
        self.integral=0
        self.x_last = None
        self.y_last = None
    def update( self, x, y):
        self.x=  x
        self.y = y 
        if( self.y_last == None ):
            # do nothing
            x_corr = 0
            pass 
        else:
            # 
            dx = self.x - self.x_last
            dy = self.y - self.y_last 
            self.integral = self.integral+ dy * dx
            x_corr = self.K * dx * dy + ( self.integral ) * self.Ki
            

        self.x_last = self.x
        self.y_last = self.y

        return x_corr


class power_max:
    def __init__( self, x0 , y0 , K , Ki ):
        
        self.x_control = controller( x0 , K, Ki )
        self.y_control = controller( y0 , K , Ki )
        
        self.a = 1
        self.n = 4
        self.dt  = 2*np.pi / self.n
        self.x0  = x0 
        self.y0 = y0
        self.x = 0
        self.y = 0
        self.count = 0
        self.p_history = []
        self.x_history = []
        self.y_history = []
        

    def update( self ,  P ):
        
        self.x_history.append( self.x)
        self.y_history.append( self.y)
        self.p_history.append( P )
        if( self.count  >  self.n ):
            dx = self.x_control.update( self.x , P )
            dy = self.y_control.update( self.y , P )
        else:
            dx = 0
            dy = 0
        self.x0 = self.x0 + dx 
        self.y0 = self.y0 + dy 
        
        cx = self.a * np.cos( self.count * self.dt )
        cy = self.a * np.sin( self.count * self.dt )
        self.x = self.x0 + cx
        self.y = self.y0 + cy  
        self.count = self.count+1 
        
        return [self.x,self.y]
    def plot( self ):
        plt.figure( 1 )
        plt.plot( self.x_history )
        plt.plot( self.y_history )
        plt.figure( 2 )
        plt.plot( self.p_history)
        plt.show()
def send_az_el( sock , az , el ):
    outMsg = "{},{}\n".format(az,el)
    data = outMsg.encode('utf-8')
    sock.send( data )
def control_antenna( host , port , max_transactions):
    time.sleep(2)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    az0 = 12
    el0 = 22
    control =  power_max( az0 , el0 , 0.001 , 0.0001)
    context = zmq.Context()
    z_socket  =  context.socket(zmq.PULL)
    z_socket.connect("tcp://localhost:5555")
    poller = zmq.Poller()
    poller.register( z_socket)
    
    send_az_el( s  , az0 , el0 )
    

    # waiting for data
    msg_count = 0 
    last_msg = time.time()
    N = 1024
    timeout = 15
    print("Power,Az,El")
    for k in range( N*max_transactions ):
        #print("Pollingg?")
        socks = dict( poller.poll(100))
        if( ( z_socket in socks ) and ( socks[z_socket] == zmq.POLLIN ) ):
            # we got a message!
            #print("Hey a message!")
            message = z_socket.recv( )
            power = struct.unpack('>f',message[-4:])
            msg_count = msg_count  + 1 
            run_control = (msg_count >= N )
        else:
            # we didnt get a message
            current_time = time.time()
            run_control = ( current_time - last_msg )  > timeout
        
        
        
        if( run_control ):
            msg_count = 0
            out = control.update( power[0] )
            print("{},{},{}".format(power[0], out[0],out[1]) , flush=True)         


            send_az_el( s  , out[0] , out[1] )
            last_msg = time.time()
    time.sleep(5)
    print("Looking for flag")
    f = open('out.txt')
    data = f.read()
    ind = data.find( "flag{")
    print("{}".format( data[ind:] ),flush=True)

    #control.plot()    
    print("Exiting")


if __name__ == "__main__":
    print("Running a simple socket")
    control_antenna( "127.0.0.1" , 12000, 285 )
    