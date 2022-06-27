import json 

from gnuradio import blocks
from gnuradio import gr
from gnuradio import network
from gnuradio import analog, digital, network,filter
import pmt
import scipy.signal as sig
import custom_blocks as cb
import numpy as np
import json

class Transmitter(gr.top_block):
    # A gnu radio top block class that has all the things we want to transmit in it
    def __init__(self, cfg , port ):
        gr.top_block.__init__(self, "SpaceJam", catch_exceptions=False)
        # constants
        Fs = 200000
        noise_wall = 100000
        # Create a few instances of band limited noise
        self.noise1 = cb.BandLimitedNoise( Fs=Fs , amplitude=noise_wall , frequency=55000 ,  width=5000 )
        self.noise2 = cb.BandLimitedNoise( Fs=Fs , amplitude=noise_wall , frequency=90000 ,  width=20000 )
        self.noise3 = cb.BandLimitedNoise( Fs=Fs , amplitude=noise_wall , frequency=-55000,  width=5000 )
        self.noise4 = cb.BandLimitedNoise( Fs=Fs , amplitude=noise_wall/20 , frequency=-75000,  width=20000 )
        self.noise5 = cb.BandLimitedNoise( Fs=Fs , amplitude=noise_wall/1000 , frequency=65000,  width=10000 )

        # add a really loud transmitter that is outputting the text to the spacejam theme song
        self.spacejam = cb.QpskJammer( file="spacejam_music.m4a",Fs=Fs, frequency=0 , amplitude=noise_wall,  samples_per_symbol=10, width=50000 )
        # Create the flag transmitter
        self.user = cb.ConfigTransmitter( file="flag.txt", Fs=Fs ,config=cfg )
        #
        self.add = blocks.add_vcc(1)
        self.tcp_out=  cb.tcp_sink_1( port=port , type=np.complex64 )

        # connect stuff up
        self.spacejam.connect( self,  (self.add,0))
        self.user.connect( self , (self.add,1))

        self.noise1.connect( self,  (self.add,2))
        self.noise2.connect( self,  (self.add,3))
        self.noise3.connect( self,  (self.add,4))
        self.noise4.connect( self,  (self.add,5))
        self.noise5.connect( self, (self.add,6))

        self.connect( (self.add,0), (self.tcp_out))

def run_transmitter( config ,port):
    # A helper function to create and run the transmitter
    tb = Transmitter( config, port )     
    tb.start()
    # The transmitter has started -when the user enters some text stop it
    try:
        input('Type any text to quit: ')
    except EOFError:
        pass
    # Be snarky
    print("See you space cowboy....")
    tb.stop()
    tb.wait()
    



if __name__ == "__main__":
    f = open("base_cfg.json" , "rt")
    data = json.load( f )
    f.close()
    run_transmitter( data ,8001) 