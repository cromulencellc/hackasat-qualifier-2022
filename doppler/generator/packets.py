#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: packets
# Author: dev
# GNU Radio version: 3.10.1.1

from gnuradio import blocks
import numpy
import pmt
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation




class packets(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "packets", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 9600
        self.hdr_2 = hdr_2 = digital.header_format_default("00011010110011111111110000011101",0, 2)
        self.hdr_1 = hdr_1 = digital.header_format_default("00010001000100010001000100010001",0, 2)

        ##################################################
        # Blocks
        ##################################################
        self.digital_protocol_formatter_bb_0_0_0_0 = digital.protocol_formatter_bb(hdr_2, "packet_len")
        self.digital_protocol_formatter_bb_0_0_0 = digital.protocol_formatter_bb(hdr_1, "packet_len")
        self.digital_crc32_bb_0_1 = digital.crc32_bb(False, "packet_len", True)
        self.digital_crc32_bb_0_0_0 = digital.crc32_bb(True, "packet_len", True)
        self.digital_crc32_bb_0 = digital.crc32_bb(False, "packet_len", True)
        self.digital_correlate_access_code_xx_ts_0 = digital.correlate_access_code_bb_ts("00011010110011111111110000011101",
          0, 'packet_len')
        self.blocks_vector_source_x_0_0 = blocks.vector_source_b([0x55]*100, True, 1, [])
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_tagged_stream_mux_0_0_0_1_1 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len', 0)
        self.blocks_tagged_stream_mux_0_0_0_1_0_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len', 0)
        self.blocks_tagged_stream_mux_0_0_0_1_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len', 0)
        self.blocks_tagged_stream_mux_0_0_0_1 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len', 0)
        self.blocks_tagged_stream_mux_0_0_0_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len', 0)
        self.blocks_tagged_stream_multiply_length_0_0 = blocks.tagged_stream_multiply_length(gr.sizeof_char*1, 'packet_len', 1/8)
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_char * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_stream_to_tagged_stream_0_2 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 4, "packet_len")
        self.blocks_stream_to_tagged_stream_0_1 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 100, "packet_len")
        self.blocks_stream_to_tagged_stream_0_0_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 38*1, "packet_len")
        self.blocks_stream_to_tagged_stream_0_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 44*1, "packet_len")
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 100, "packet_len")
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_char*1, (156, 54))
        self.blocks_pack_k_bits_bb_0_0 = blocks.pack_k_bits_bb(8)
        self.blocks_head_0_0 = blocks.head(gr.sizeof_char*1, 4*3)
        self.blocks_file_source_0_1 = blocks.file_source(gr.sizeof_char*1, 'flag.txt', True, 0, 0)
        self.blocks_file_source_0_1.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0_0_0 = blocks.file_source(gr.sizeof_char*1, 'pkt_there_b_a_flag.txt', True, 0, 0)
        self.blocks_file_source_0_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_char*1, 'pkt_not_the_data.txt', True, 0, 0)
        self.blocks_file_source_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, 'out.bin', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 255, 1000))), True)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_stream_to_tagged_stream_0_0, 0))
        self.connect((self.blocks_file_source_0_0_0, 0), (self.blocks_stream_to_tagged_stream_0_0_0, 0))
        self.connect((self.blocks_file_source_0_1, 0), (self.blocks_head_0_0, 0))
        self.connect((self.blocks_head_0_0, 0), (self.blocks_stream_to_tagged_stream_0_2, 0))
        self.connect((self.blocks_pack_k_bits_bb_0_0, 0), (self.blocks_tagged_stream_multiply_length_0_0, 0))
        self.connect((self.blocks_stream_mux_0, 0), (self.blocks_tagged_stream_mux_0_0_0_0, 1))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_tagged_stream_mux_0_0_0_1_0, 1))
        self.connect((self.blocks_stream_to_tagged_stream_0_0, 0), (self.blocks_tagged_stream_mux_0_0_0_1_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_0_0, 0), (self.blocks_tagged_stream_mux_0_0_0_1_0_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_1, 0), (self.blocks_tagged_stream_mux_0_0_0_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_2, 0), (self.blocks_tagged_stream_mux_0_0_0_1_0_0, 1))
        self.connect((self.blocks_tag_gate_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0_0, 0), (self.digital_crc32_bb_0_0_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0_0_0_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0_0_0_1, 0), (self.blocks_stream_mux_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0_0_0_1_0, 0), (self.digital_crc32_bb_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0_0_0_1_0_0, 0), (self.digital_crc32_bb_0_1, 0))
        self.connect((self.blocks_tagged_stream_mux_0_0_0_1_1, 0), (self.blocks_stream_mux_0, 1))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.digital_correlate_access_code_xx_ts_0, 0))
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.blocks_stream_to_tagged_stream_0_1, 0))
        self.connect((self.digital_correlate_access_code_xx_ts_0, 0), (self.blocks_pack_k_bits_bb_0_0, 0))
        self.connect((self.digital_crc32_bb_0, 0), (self.blocks_tagged_stream_mux_0_0_0_1, 1))
        self.connect((self.digital_crc32_bb_0, 0), (self.digital_protocol_formatter_bb_0_0_0, 0))
        self.connect((self.digital_crc32_bb_0_0_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.digital_crc32_bb_0_1, 0), (self.blocks_tagged_stream_mux_0_0_0_1_1, 1))
        self.connect((self.digital_crc32_bb_0_1, 0), (self.digital_protocol_formatter_bb_0_0_0_0, 0))
        self.connect((self.digital_protocol_formatter_bb_0_0_0, 0), (self.blocks_tagged_stream_mux_0_0_0_1, 0))
        self.connect((self.digital_protocol_formatter_bb_0_0_0_0, 0), (self.blocks_tagged_stream_mux_0_0_0_1_1, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_hdr_2(self):
        return self.hdr_2

    def set_hdr_2(self, hdr_2):
        self.hdr_2 = hdr_2

    def get_hdr_1(self):
        return self.hdr_1

    def set_hdr_1(self, hdr_1):
        self.hdr_1 = hdr_1




def main(top_block_cls=packets, options=None):
    tb = top_block_cls()

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
    main()
