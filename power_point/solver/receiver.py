
from gnuradio import blocks
from gnuradio import gr
from gnuradio import network
from gnuradio import analog, digital
from gnuradio import gr, pdu
from gnuradio import network
from gnuradio import pdu
from gnuradio import zeromq


import sys 
import signal
class Receiver(gr.top_block):

    def __init__(self , sample_ip, sample_port  ):
        gr.top_block.__init__(self, "Receiver", catch_exceptions=False)


        ##################################################
        # Variables
        ##################################################
        self.constellation = qpsk = digital.constellation_qpsk().base()
        samples_per_symbol = 10 
        agc_reference = 100 
        zmq_address = 'tcp://*:5555'
        zmq_timeout = 100 # ms 
        self.sample_port = sample_port
        self.sample_ip  = sample_ip
        ##################################################
        # Blocks
        ##################################################
        self.sample_source = network.tcp_source.tcp_source(itemsize=gr.sizeof_gr_complex*1,addr=sample_ip,port=sample_port,server=False)

        # power calculation
        self.mag = blocks.complex_to_mag(1)
        self.tagger = blocks.stream_to_tagged_stream(gr.sizeof_float, 1, 1, "packet_len")
        self.pdu_gen = pdu.tagged_stream_to_pdu(gr.types.float_t, 'packet_len')
        self.pdu_split = pdu.pdu_split(False)
        self.zmq_sink = zeromq.push_msg_sink(zmq_address, zmq_timeout, True)

        # symbol decoding
        self.agc = analog.feedforward_agc_cc(1, agc_reference)
        self.symbol_sync = digital.symbol_sync_cc(
            digital.TED_MUELLER_AND_MULLER,
            samples_per_symbol,
            0.045,
            1.0,
            1.0,
            1.5,
            1,
            self.constellation,
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.decoder = digital.constellation_decoder_cb( self.constellation)

        self.repacker = blocks.repack_bits_bb(2, 8, "", True, gr.GR_LSB_FIRST)
        self.file_sink = blocks.file_sink(gr.sizeof_char*1, 'out.txt', False)
        self.file_sink.set_unbuffered(True)


        ##################################################
        # Connections
        ##################################################
        # magnitude 
        self.connect((self.sample_source, 0), (self.mag, 0))
        self.connect((self.mag, 0), (self.tagger, 0))
        self.connect((self.tagger, 0), (self.pdu_gen, 0))
        self.msg_connect((self.pdu_gen, 'pdus'), (self.pdu_split, 'pdu'))
        self.msg_connect((self.pdu_split, 'vec'), (self.zmq_sink, 'in'))

        # decoder
        self.connect((self.sample_source, 0), (self.agc, 0))
        self.connect((self.agc, 0), (self.symbol_sync, 0))
        self.connect((self.symbol_sync, 0), (self.decoder, 0))
        self.connect((self.decoder, 0), (self.repacker, 0))
        self.connect((self.repacker, 0), (self.file_sink, 0))
def receiver_main( sample_ip , sample_port ):
    tb = Receiver(sample_ip,sample_port)


    tb.start()

    return tb
def stop_flowgraph( flowgraph ):
    flowgraph.stop()
    flowgraph.wait()
if __name__ == "__main__":
    receiver_main(sample_ip="127.0.0.1" , sample_port=12001)