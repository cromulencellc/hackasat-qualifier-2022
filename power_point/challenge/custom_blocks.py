from re import L
from gnuradio import gr
import numpy as np
import time
import os
import socket
import signal
from target import linear_target
class AntennaCmdError( Exception ):
    pass
class antenna_cmd_src( gr.basic_block ):
    def __init__( self , port  ):
        gr.basic_block.__init__(self, name="antenna_src" , in_sig=None  , out_sig=[np.float32,np.float32] )
        print( "Antenna pointing server: Waiting for client to connect", flush=True)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', port))
        self.sock.listen( 1 )
        target, address =  self.sock.accept() 
        self.target = target
        print("Antenna pointing server: Client connected" , flush=True)
    def validate( self , instr ):
        return instr
    def general_work( self , input_items, output_items):
        inMsg = self.target.recv( 1024 )
        try:
            inStr = inMsg.decode("utf-8")
            inStr = self.validate( inStr )
            print("Got {}".format( inStr))
            cmds = inStr.split(",") 
            az=  np.float32( cmds[0] ) 
            el=  np.float32( cmds[1] )
            output_items[0][0] = az
            output_items[1][0] = el
            return 1
        except AntennaCmdError: 
            print("Invalid antenna CMD ")
        except: 
            print("Antenna command poorly formed. ")
        return 0
class tcp_sink_1( gr.basic_block):
    def __init__(self, port, type):
        gr.basic_block.__init__(self, name="custom_tcp" , in_sig=[ type ] , out_sig=None )
        print("Sample server: Waiting for client connection", flush=True)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', port))
        self.sock.listen( 1 )
        target, address =  self.sock.accept() 

        self.target = target
        print("Sample Server: Client connected" , flush=True)
    def general_work( self , input_items, output_items):
        N =1024
        available = len(input_items[0])
        time.sleep(1)
        if( available >= N ):
            data = input_items[0][:N]
            self.target.send(data)
            self.consume( 0 , N )
            print("Sending {} samples over TCP/IP".format( len(data)), flush=True)
            return N
        else:
            return 0
class pass_thru( gr.sync_block ):
    def __init__(self  ):
        gr.sync_block.__init__(self, name="pass_thru" , in_sig=[ np.float64] , out_sig=[np.float64] )
        self.count = 0 
    def work( self , input_items , output_items ):

        output_items[0][:] = input_items[0]
        return len( output_items[0])


class pointing_model( gr.basic_block ):
    def __init__(self , max_amplitude , limit ):
        gr.basic_block.__init__(self, name="simple custom" , in_sig=[np.float32, np.float32] , out_sig=[np.complex64] )
        self.count = 0 
        self.az_model = linear_target( 10.0 , 0.0)
        self.el_model = linear_target( 20.0 ,0.0 )

        self.bw = np.deg2rad(5.0)
        self.max_amplitude =max_amplitude
   
        self.count = 0
        self.limit = limit
    def tx_motion( self ):
        if( self.count == 55 ):
            self.az_model.set_dx(0.1 )
            self.el_model.set_dx(-0.1 )
        if( self.count == 155 ):
            self.az_model.set_dx(0.0)
            self.el_model.set_dx(0.0)
        if( self.count == 200 ):
            self.az_model.set_dx( -.05 )
            self.el_model.set_dx( 0 )
        if( self.count == 225 ):
            self.el_model.set_dx( 0 )
            self.az_model.set_dx( 0 )
        el  =  self.el_model.update()
        az  =  self.az_model.update()
        el_rad = np.deg2rad( el )
        az_rad = np.deg2rad( az ) 
        kx = np.cos( el_rad )*np.cos( az_rad )
        ky = np.cos( el_rad )*np.sin( az_rad )
        kz = np.sin( el_rad )
        self.k = np.array( [ kx, ky,kz ])
    def general_work( self , input_items , output_items ):
        # user pointing 
        az_deg = input_items[0][0]
        el_deg = input_items[1][0]
        az = np.deg2rad(input_items[0][0])
        el = np.deg2rad(input_items[1][0])
        kx= np.cos(el)*np.cos(az )
        ky = np.cos(el )*np.sin(az)
        kz = np.sin(el)
        pointing = np.array( [ kx,ky,kz ])
        # physics pointing 
        self.tx_motion() 
        delta = np.arccos( np.dot( pointing, self.k))
        print("Command {} received from user  ".format( self.count ), flush=True)
        print("Pointing to  Az: {}  El: {}".format(az_deg,el_deg), flush=True)
        if( delta < self.bw ):
            #print("Tracking is ok {}".format( np.rad2deg(delta)))
            amplitude = self.max_amplitude * (1  - (delta/self.bw))
            pass
        else:
            print("Tracking lost")
            amplitude =  0.0
            if( self.count > self.limit ):
                print("You didn't maintain the connection...quitting", flush=True)
                #raise(ValueError)
                os.kill(os.getpid(), signal.SIGTERM)


    
        #print("Length {}".format( len(output_items[0])))

        output_items[0][:] = np.complex64( amplitude + 0j ) 
        self.count = self.count + 1 
        # consume the inputs 
        self.consume(0 , 1)
        self.consume(1 , 1)
        return len( output_items[0])