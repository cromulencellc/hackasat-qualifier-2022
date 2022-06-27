import socket
import numpy as np

class tcp_siggen:
    def __init__( self,samp_rate , freq , amp , noise_var , N ):
        # Create the phase of the sin wave at each samples
        t = np.arange(start=0,stop=N/samp_rate, step=1/samp_rate , dtype=np.complex64) 
        phase =  2* np.pi * freq * t
        # create a complex sin wave
        carrier = amp * np.exp( phase * 1j )
        # generate complex white(ish) gaussian noise with the right variance
        noise_dev = np.sqrt( noise_var )
        noise =  (noise_dev / np.sqrt(2))  * ( np.random.normal( 0 , 1, N ) + 1j*np.random.normal(0,1,N) ) 
        # add the sin wave and the noise together 
        self.signal = np.add( carrier , noise , dtype=np.complex64)
    def send( self, port ):
        print("Waiting for client connection", flush=True)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', port))
        self.sock.listen( 1 )
        target, address =  self.sock.accept() 

        self.target = target
        print("Client connected sending {} samples".format(len(self.signal)) , flush=True)
        
        self.target.send( self.signal )            