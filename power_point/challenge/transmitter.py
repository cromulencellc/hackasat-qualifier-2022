#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Do You GNU
# GNU Radio version: 3.10.1.1

from gnuradio import blocks
from gnuradio import gr
from gnuradio import network
from gnuradio import analog, digital

import data_file
from custom_blocks import *

import sys
import signal


class PowerPoint(gr.top_block):

    def __init__(self , source_port , sink_port , source_ip):
        gr.top_block.__init__(self, "PowerPoint", catch_exceptions=False)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1024
        self.qpsk_0 = qpsk_0 = digital.constellation_qpsk().base()
        self.n = 1024
        self.samps_per_symbol = 10
        self.if_freq = 0

        self.source_ip = source_ip
        self.source_port = source_port
        self.sink_port = sink_port
        ##################################################
        # Blocks
        self.tcp_sink = tcp_sink_1( sink_port , np.float64 ) 
        self.cmd_src = antenna_cmd_src(source_port)
        self.power = pointing_model(282 ,300)
        self.repeat_power = blocks.repeat(gr.sizeof_float*2,self.n)
        self.debug = pass_thru()
        # Databit section
        self.data_bits = blocks.file_source(1, 'databits.bin', False, 0, 0)
        self.unpacker = blocks.repack_bits_bb(8, 2, "", True, gr.GR_LSB_FIRST)
        self.qpsk_encoder = digital.constellation_encoder_bc(qpsk_0)
        self.repeat_bits = blocks.repeat(gr.sizeof_float*2, self.samps_per_symbol)
        # combiner section 
        self.mult = blocks.multiply_vcc(1)
        ##################################################
        # Connections
        ##################################################
        self.connect( (self.cmd_src,0) , (self.power,0))
        self.connect( (self.cmd_src,1) , (self.power,1))
        self.connect( (self.power,0) , (self.repeat_power,0))
        
        self.connect( (self.data_bits,0), (self.unpacker,0))

        self.connect( (self.unpacker,0), (self.qpsk_encoder,0))
        self.connect( (self.qpsk_encoder ,0) , (self.repeat_bits,0))

        self.connect( (self.repeat_power,0), (self.mult,0))
        self.connect( (self.repeat_bits,0), (self.mult,1))

        self.connect( (self.mult,0), (self.debug,0))
        self.connect( (self.debug,0), (self.tcp_sink,0))
        

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate


def transmitter_main(source_port, sink_port , source_ip):

    tb = PowerPoint(source_port=source_port, sink_port=sink_port , source_ip=source_ip)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    data_file.make_databit_file( "databits.bin", 800 , 4 , "flag{FlagyMcFlagTheFlag}")
    transmitter_main(source_port=12000,sink_port=12001,source_ip="127.0.0.1")
