
from re import S
from gnuradio import blocks
from gnuradio import gr
from gnuradio import network
from gnuradio import analog, digital, network,filter


import numpy as np
from gnuradio.filter import firdes
from gnuradio.fft import window
import socket
import custom_blocks as cb
import json
import time
import bit_checker

class Receiver( gr.top_block ):
    # A gnu radio top block class that makes the receiver
    def __init__( self , file , data_file):
        gr.top_block.__init__(self, "Rxr", catch_exceptions=False)



        Fs = 200000
        # variables
        self.validate(file)
        constellation = self.constellations[ self.config["constellation"] ]
        # 
        decim = self.config["decim"]
        filter_band = self.config["filter"]
        sps = self.config["samples_per_symbol"] / decim 
        freq_shift = -(self.config["frequency"] -2.1e6)
        nsymbols = np.power( 2 , constellation["bits"])
        nfilts = self.config["taps"]
        lpf =  firdes.low_pass(1, Fs, filter_band, 1000, window.WIN_HAMMING, 6.76)
        rrc_0 = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), 0.35, nfilts)
        print("Receiver Config")
        print("-----------")
        print("Sample Freq: {}".format(Fs ) )
        print("Frequency Shift: {}".format(freq_shift))
        print("Decimation: {}".format(decim))
        print("Filter Width (HZ): {}".format( filter_band))
        print("Samples per symbol (post-decim): {}".format( sps ))
        print("Constellation: {}".format( self.config["constellation"]))
        print("Differential Decocde: {} with {} modulus".format( self.config["diff_encoding"], nsymbols ))
        print("------------------\n\n")
        print("\n", flush=True)
        # possible blocks?
        self.diff_encode["ON"] = digital.diff_decoder_bb(nsymbols, digital.DIFF_DIFFERENTIAL)
        ######### blocks 
        #self.src = network.tcp_source.tcp_source(itemsize=gr.sizeof_gr_complex*1,addr=ip,port=port,server=False)
        self.src  = blocks.file_source(gr.sizeof_gr_complex*1, data_file, False, 0, 0)
        self.freqshift = blocks.rotator_cc(2.0*np.pi*freq_shift/Fs)
        self.filter = filter.fft_filter_ccc(decim, lpf, 1)
        self.sync = digital.pfb_clock_sync_ccf(sps, 6.28/100, rrc_0, nfilts, nfilts/2, 1.5, 1)
                    
        self.decode = digital.constellation_decoder_cb(constellation["obj"])
        self.diff_decode = self.diff_encode[ self.config["diff_encoding"]]
        self.repacker = blocks.repack_bits_bb( constellation["bits"], 8, "", False, gr.GR_MSB_FIRST)
        self.file_sink = blocks.file_sink(gr.sizeof_char*1, 'decoded.txt', False)



        ######## connections
        self.connect( (self.src,0) , (self.freqshift,0))
        self.connect( (self.freqshift,0) , (self.filter,0))
        self.connect( (self.filter,0), (self.sync,0))
        self.connect( (self.sync,0) , (self.decode,0))
        self.connect( (self.decode,0) , (self.diff_decode,0))
        self.connect( (self.diff_decode,0) , (self.repacker,0))
        self.connect( (self.repacker,0) , (self.file_sink,0))

    def validate( self , file ):
        # load the file to a dictionary
        f = open( file , "rt")
        data = json.load( f )
        f.close()
        self.config = data 
        # validate 
        self.constellations = dict()
        self.constellations["BPSK"] = {"bits":1 , "obj": digital.constellation_bpsk().base() } 
        self.constellations["QPSK"] = {"bits":2 , "obj": digital.constellation_qpsk().base() }
        self.constellations["8PSK"] = {"bits":3 , "obj": digital.constellation_8psk().base() }
        self.constellations["16QAM"] = {"bits":4, "obj": digital.constellation_16qam().base() }
        #
                # on/off for differential encoding
        self.diff_encode = dict()
        self.diff_encode["ON"] = 0
        self.diff_encode["OFF"] = cb.pass_thru( np.byte ) 

def run_rx( rx_config , ip, port):
    # Get the bytes and toss them in a file
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    data = s.recv( int(1024*1024*1.6) , socket.MSG_WAITALL)# get 2M
    s.close()
    f = open("data.dat",'wb')
    f.write( data )
    f.close()
    rx = Receiver( file=rx_config, data_file="data.dat")
    rx.start()
    print("RX running", flush=True)
    time.sleep( 30 )
    print("Trying to kill gnu radio", flush=True)
    rx.stop()
    print("RX stopped", flush=True)
    print("Samples processed", flush=True)
    print("Trying to find your flag", flush=True)
    bit_checker.find_offset( "decoded.txt", "flag")
    print("Done", flush=True)
if __name__ == "__main__":
    run_rx( 'qpsk.json', "127.0.0.1", 8001)
    bit_checker.find_offset( file="decoded.txt", find_text="flag")