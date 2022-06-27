# This file contains all the custom blocks used by the trasnmitter flowgraph


from gnuradio import blocks
from gnuradio import gr
from gnuradio import analog, digital, network,filter
import pmt
import scipy.signal as sig
import numpy as np
import socket
import os


class pass_thru( gr.sync_block ):
    # This is a pass through block that can be used when you want something to be "OFF"
    def __init__( self , dtype ):
        gr.sync_block.__init__(self , name="pass thru" , in_sig= [dtype], out_sig=[dtype])
    def work( self , input_items , output_items ):
        output_items[0][:] = input_items[0]
        return len( output_items[0])

class tcp_sink_1( gr.basic_block):
    # This is a custom TCP sink block
    # - The TCP connection is a SERVER and waits for clients to connect
    # - The block only sends fixed size transactions of 1024 in length
    def __init__(self, port, type , transaction_size=1024):
        self.N = transaction_size
        gr.basic_block.__init__(self, name="custom_tcp" , in_sig=[ type ] , out_sig=None )
        service_host = os.getenv("SERVICE_HOST" , "localhost")
        service_port = os.getenv("SERVICE_PORT" , port)
        print("Connect via TCP on {}:{} to get samples".format( service_host, service_port), flush=True)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', port))
        self.sock.listen( 1 )
        target, address =  self.sock.accept() 

        self.target = target
        print("Client connected" , flush=True)
    def general_work( self , input_items, output_items):
        available = len(input_items[0])
        # If there are enough samples available send them
        # Otherwise do nothing
        if( available >= self.N ):
            data = input_items[0][:self.N]
            self.target.send(data)
            self.consume( 0 , self.N )
            return self.N
        else:
            return 0

class BandLimitedNoise:
    # This block creates some band limited noise centered at a certain frequency.
    # "Band limiting" is accomplished by creating noise at a cetain variance and then passing it through a low pass filter
    # This filtered noise is then frequency shifted to the desired frequency
    # This leaves some very low power noise out of the specified band
    def __init__( self ,  Fs , amplitude , frequency, width, cutoff_width=1000):
        # Create a filter with N taps
        # Bigger N results in sharper cutoffs in frequency domain
        # @param Fs: Sample rate at which to generate the noise (Hz)
        # @param amplitude: Noise variance 
        # @param frequency: Center frequency of the noise (Hz)
        # @param width: Single sided bandwidth of the noise (Hz)
        # @param cutoff_width: How quickly should the filter cutoff (Hz) 
    
        N=512
        filter_taps = sig.firwin( numtaps=N , fs=Fs ,cutoff=width ,width=cutoff_width)
        # Build the blocks
        self.noise = analog.noise_source_c(analog.GR_GAUSSIAN, amplitude , 0)
        self.low_pass = filter.fft_filter_ccc(1, filter_taps, 1)
        self.low_pass.declare_sample_delay(0)
        self.freq_shift = blocks.rotator_cc(2.0*np.pi*frequency/Fs)
    def connect( self, top , connect_to ):     
        # @param top: The top block which all these blocks get implemented in
        # @param conncet_to: Connect the tail end of these blocks to this 
        # Connect the blocks together and then connect them to the outside world
        top.connect((self.noise,0) , (self.low_pass,0))
        top.connect((self.low_pass,0) , (self.freq_shift,0))
        top.connect((self.freq_shift,0), connect_to )
class QpskJammer:
    # This block creates a QPSK transmitter that will transmit a band limited signal at a certain frequency
    def __init__( self , file , Fs,  amplitude , frequency , samples_per_symbol, width ):
        # @param file: The data bits are in this file path
        # @param Fs: Sampling frequency at which to make samples (Hz)
        # @param amplitude: Amplitude of the signal 
        # @param frequency: Center the signal at this frequency (Hz)
        # @param samples_per_symbol: How many samples are there in on PSK/QAM symbol. symbol rate = Fs/samples_per_symbol
        # @param width: Single sided bandwith at which to filter the signal (Hz)

        # Create a filter with N taps - bigger N means sharper cutoff
        N=512
        filter_taps = sig.firwin( numtaps=N , fs=Fs ,cutoff=width)
        # Its a QPSK jammer so we can just pick qpsk!
        qpsk =  digital.constellation_qpsk().base()
        # Read data from a file
        # Repeat is set to False so transmission stops when we are out of data
        # This single False setting is what enforces the length of the challenge
        self.src = blocks.file_source(gr.sizeof_char*1, file, False ) 
        self.src.set_begin_tag(pmt.PMT_NIL)
        # unpack - differential encode and put data into a symbol
        self.repacker = blocks.repack_bits_bb(8, 2, "", False, gr.GR_MSB_FIRST)
        self.diff_encode = digital.diff_encoder_bb( 4 , digital.DIFF_DIFFERENTIAL)
        self.encoder = digital.constellation_encoder_bc(qpsk)
        # Scale to the proper amplitude
        self.scale = blocks.multiply_const_cc(amplitude)
        # Repeat so that we have the right number of samples per symbol
        self.repeat = blocks.repeat(gr.sizeof_gr_complex*1, samples_per_symbol )
        # filter and frequency shift
        self.low_pass = filter.fft_filter_ccc(1, filter_taps, 1)
        self.low_pass.declare_sample_delay(0)        
        self.freqshift_cc = blocks.rotator_cc(2.0*np.pi*frequency/Fs)
    def connect( self , top , connect_to ):
        # @param top: The top block which all these blocks get implemented in
        # @param conncet_to: Connect the tail end of these blocks to this 
        # Connect the blocks together and then connect them to the outside world
        top.connect( (self.src,0) , ( self.repacker,0) ) 
        top.connect( (self.repacker,0) , ( self.diff_encode,0) ) 
        top.connect( (self.diff_encode,0) , (self.encoder,0))
        top.connect( (self.encoder,0) , ( self.scale,0) ) 
        top.connect( (self.scale,0) , ( self.repeat,0) ) 
        top.connect( (self.repeat,0), (self.low_pass,0))
        top.connect( (self.low_pass,0), (self.freqshift_cc,0))
        top.connect( (self.freqshift_cc,0), connect_to)

class ConfigTransmitter:
    # This class is a dictionary configurable transmitter
    def __init__( self, file, Fs, config):
        # @param file: Data bit file
        # @param Fs: Sample rate (Hz)
        # @param config: configuration dictionary 
        opts=  ["amplitude","frequency","constellation","samples_per_symbol","diff_encoding"]
        self.options = dict() 
        for opt in opts: 
            self.options[opt] = 0
        self.config = config
        # Hard code a center frequency in Hz
        self.base_freq = 2000000
        self.Fs = Fs
        self.validate( )
        
        bits_per_symbol = self.constellations[ self.config["constellation"] ]["bits"]
        constellation_object = self.constellations[ self.config["constellation"] ]["obj"]
        freq = self.config["frequency"] - self.base_freq - Fs/2


        self.src = blocks.file_source( gr.sizeof_char*1 , file , True )
        self.src.set_begin_tag(pmt.PMT_NIL)

        self.repacker = blocks.repack_bits_bb( 8 , bits_per_symbol , "" , False, gr.GR_MSB_FIRST)
        self.encoder = digital.constellation_encoder_bc( constellation_object )
        self.diff_encoder = self.diff_encode[ self.config["diff_encoding"]]
        self.scale = blocks.multiply_const_cc( self.config["amplitude"])
        self.repeat = blocks.repeat(gr.sizeof_gr_complex*1, self.config["samples_per_symbol"] )
        self.freqshift = blocks.rotator_cc(2.0*np.pi*freq/Fs)
        
        

    def get_opts(self):
        return self.options
        
    def connect( self, top , connect_to ):
        top.connect( (self.src,0) , (self.repacker,0) )
        top.connect( (self.repacker,0) , (self.diff_encoder,0) )
        top.connect( (self.diff_encoder,0) , (self.encoder,0) )
        top.connect( (self.encoder,0) , (self.scale,0) )
        top.connect( (self.scale,0) , (self.repeat,0) )
        top.connect( (self.repeat,0), (self.freqshift,0))
        top.connect( (self.freqshift,0),  connect_to )

    def validate( self ):
        # This method validates that the inputs are ok and that there are no extraneous inputs
        expected_cfg = list( self.options.keys( )  )
        self.constellations = dict()
        # available psk types 
        self.constellations["BPSK"] = {"bits":1 , "obj": digital.constellation_bpsk().base() } 
        self.constellations["QPSK"] = {"bits":2 , "obj": digital.constellation_qpsk().base() }
        self.constellations["8PSK"] = {"bits":3 , "obj": digital.constellation_8psk().base() }
        self.constellations["16QAM"] = {"bits":4, "obj": digital.constellation_16qam().base() }
        # on/off for differential encoding
        self.diff_encode = dict()
        self.diff_encode["ON"] =0
        self.diff_encode["OFF"] = pass_thru( np.byte ) 

        # Make sure that all the keys that we expect to have are in the dictionary
        for key in expected_cfg:
            present = key in self.config 
            if( not present ):
                print("bad configuration sent")
                print("missing key {}".format( key ))
                raise( ValueError )
        # Make sure there arent any keys that we DONT expect to have
        for key in self.config:
            present = key in expected_cfg 
            if( not present ):
                print("bad configuration sent")
                print("unrecognized key sent {}".format( key ))
                raise(ValueError)
        # Check the bounds on a bunch of values
        print("Transmitter Configuration")
        print("--------------")
        print("Sample rate: {}".format(self.Fs))
        self.clamp("amplitude", 0 , 1000 )
        self.clamp("frequency", 2000000 , 2200000 )
        self.clamp("samples_per_symbol", 0 , 10000000 )
        self.in_group("constellation", list(self.constellations.keys()) )
        self.in_group("diff_encoding" , list(self.diff_encode.keys()) )
        print("---------------")
        print("RX Front End Configuration")
        print("---------------")
        print("Frequency: {}".format( self.base_freq + self.Fs/2))
        print("A/D Sampling Frequency: {}".format( self.Fs ))
        print("---------------")
        # setup the blocks that are dependent on valid configuration 
        bits =  self.constellations[ self.config["constellation"] ]["bits"]
        nsymbols = np.power(2,bits)
        # differential encoding will automatically default to the modules corresponding to number of symbols
        self.diff_encode["ON"] = digital.diff_encoder_bb( nsymbols, digital.DIFF_DIFFERENTIAL)
        pass
        
         
    def clamp( self , key , min , max ):
        # A helper method that will take a specific key out of the dictionary and apply min/max clamping
        # @param key: which key do you want to clamp
        # @parm min: minimum allowable value
        # @param max: maximim allowable value

        value = self.config[key]
        if( value < min ):
            print("Value for {} out of range - clamping to {}".format(key,min))
            self.config[key] = min
        if( value > max ):
            print("Value for {} out of range - clamping to {}".format(key,max))
            self.config[key] = max
        print("{}: {}".format(key,self.config[key]))
    def in_group( self, key , group ):
        # A helper method that takes a specific key out of the dictioanry and makes sure its in a group
        # Raises an exception if it fails
        # @param key: Which key do you want to check
        # @parma group: A list of acceptable options
        value = self.config[key]
        
        present = value in group
        if( not present ):
            print("You gave a value of {} for {} that is not valid please pick one in {}".format(value,key,group))
            raise(ValueError)
        print("{}: {}".format(key,value))