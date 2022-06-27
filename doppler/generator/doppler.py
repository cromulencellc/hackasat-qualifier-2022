#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: doppler.grc
# GNU Radio version: 3.10.1.1

from gnuradio import analog
from gnuradio import blocks
import math
import numpy
import pmt
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq




class doppler(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "doppler.grc", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 10
        self.nfilts = nfilts = 32
        self.baud_rate = baud_rate = 1200
        self.transition_width = transition_width = baud_rate/sps
        self.samp_rate = samp_rate = baud_rate*100
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), 0.35, 11*sps*nfilts)
        self.qpsk = qpsk = digital.constellation_rect([0.707+0.707j, -0.707+0.707j, -0.707-0.707j, 0.707-0.707j], [0, 1, 2, 3],
        4, 2, 2, 1, 1).base()
        self.path_loss = path_loss = 0
        self.hdr_2 = hdr_2 = digital.header_format_default("00011010110011111111110000011101",0, 2)
        self.hdr_1 = hdr_1 = digital.header_format_default("00010001000100010001000100010001",0, 2)
        self.freq_shift = freq_shift = 0
        self.arity = arity = 4

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_sub_msg_source_0_0 = zeromq.sub_msg_source('tcp://127.0.0.1:5556', 100, False)
        self.zeromq_sub_msg_source_0 = zeromq.sub_msg_source('tcp://127.0.0.1:5555', 100, False)
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                baud_rate*2.2,
                transition_width,
                window.WIN_HAMMING,
                6.76))
        self.digital_protocol_formatter_bb_0_0_0_0 = digital.protocol_formatter_bb(hdr_2, "packet_len")
        self.digital_protocol_formatter_bb_0_0_0 = digital.protocol_formatter_bb(hdr_1, "packet_len")
        self.digital_diff_encoder_bb_0 = digital.diff_encoder_bb(4, digital.DIFF_DIFFERENTIAL)
        self.digital_crc32_bb_0_1 = digital.crc32_bb(False, "packet_len", True)
        self.digital_crc32_bb_0 = digital.crc32_bb(False, "packet_len", True)
        self.digital_constellation_encoder_bc_0 = digital.constellation_encoder_bc(qpsk)
        self.blocks_vector_source_x_0_0 = blocks.vector_source_b([0x55], True, 1, [])
        self.blocks_tagged_stream_mux_0_0_0_1_1 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len', 0)
        self.blocks_tagged_stream_mux_0_0_0_1_0_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len', 0)
        self.blocks_tagged_stream_mux_0_0_0_1_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len', 0)
        self.blocks_tagged_stream_mux_0_0_0_1 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len', 0)
        self.blocks_stream_to_tagged_stream_0_2 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 20, "packet_len")
        self.blocks_stream_to_tagged_stream_0_0_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 38*1, "packet_len")
        self.blocks_stream_to_tagged_stream_0_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 44*1, "packet_len")
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 100, "packet_len")
        self.blocks_stream_mux_0_0 = blocks.stream_mux(gr.sizeof_char*1, (100,500*(156*2+70)))
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_char*1, (156*2, 70))
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_gr_complex*1, int(samp_rate/baud_rate))
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(8, 2, "", False, gr.GR_LSB_FIRST)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(path_loss)
        self.blocks_msgpair_to_var_0_0 = blocks.msg_pair_to_var(self.set_path_loss)
        self.blocks_msgpair_to_var_0 = blocks.msg_pair_to_var(self.set_freq_shift)
        self.blocks_head_0_0 = blocks.head(gr.sizeof_char*1, 750)
        self.blocks_freqshift_cc_0 = blocks.rotator_cc(2.0*math.pi*freq_shift/samp_rate)
        self.blocks_file_source_0_1 = blocks.file_source(gr.sizeof_char*1, 'flag.txt', True, 0, 0)
        self.blocks_file_source_0_1.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0_0_0 = blocks.file_source(gr.sizeof_char*1, 'pkt_there_b_a_flag.txt', True, 0, 0)
        self.blocks_file_source_0_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_char*1, 'pkt_not_the_data.txt', True, 0, 0)
        self.blocks_file_source_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, 'sat_downlink_120ksps.iq', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 255, 1000))), True)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, .001, 0)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.blocks_msgpair_to_var_0, 'inpair'))
        self.msg_connect((self.zeromq_sub_msg_source_0_0, 'out'), (self.blocks_msgpair_to_var_0_0, 'inpair'))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_stream_to_tagged_stream_0_0, 0))
        self.connect((self.blocks_file_source_0_0_0, 0), (self.blocks_stream_to_tagged_stream_0_0_0, 0))
        self.connect((self.blocks_file_source_0_1, 0), (self.blocks_head_0_0, 0))
        self.connect((self.blocks_freqshift_cc_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_head_0_0, 0), (self.blocks_stream_to_tagged_stream_0_2, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_freqshift_cc_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_diff_encoder_bb_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.blocks_stream_mux_0, 0), (self.blocks_stream_mux_0_0, 1))
        self.connect((self.blocks_stream_mux_0_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_tagged_stream_mux_0_0_0_1_0, 1))
        self.connect((self.blocks_stream_to_tagged_stream_0_0, 0), (self.blocks_tagged_stream_mux_0_0_0_1_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_0_0, 0), (self.blocks_tagged_stream_mux_0_0_0_1_0_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_2, 0), (self.blocks_tagged_stream_mux_0_0_0_1_0_0, 1))
        self.connect((self.blocks_tagged_stream_mux_0_0_0_1, 0), (self.blocks_stream_mux_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0_0_0_1_0, 0), (self.digital_crc32_bb_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0_0_0_1_0_0, 0), (self.digital_crc32_bb_0_1, 0))
        self.connect((self.blocks_tagged_stream_mux_0_0_0_1_1, 0), (self.blocks_stream_mux_0, 1))
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.blocks_stream_mux_0_0, 0))
        self.connect((self.digital_constellation_encoder_bc_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.digital_crc32_bb_0, 0), (self.blocks_tagged_stream_mux_0_0_0_1, 1))
        self.connect((self.digital_crc32_bb_0, 0), (self.digital_protocol_formatter_bb_0_0_0, 0))
        self.connect((self.digital_crc32_bb_0_1, 0), (self.blocks_tagged_stream_mux_0_0_0_1_1, 1))
        self.connect((self.digital_crc32_bb_0_1, 0), (self.digital_protocol_formatter_bb_0_0_0_0, 0))
        self.connect((self.digital_diff_encoder_bb_0, 0), (self.digital_constellation_encoder_bc_0, 0))
        self.connect((self.digital_protocol_formatter_bb_0_0_0, 0), (self.blocks_tagged_stream_mux_0_0_0_1, 0))
        self.connect((self.digital_protocol_formatter_bb_0_0_0_0, 0), (self.blocks_tagged_stream_mux_0_0_0_1_1, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))


    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), 0.35, 11*self.sps*self.nfilts))
        self.set_transition_width(self.baud_rate/self.sps)

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), 0.35, 11*self.sps*self.nfilts))

    def get_baud_rate(self):
        return self.baud_rate

    def set_baud_rate(self, baud_rate):
        self.baud_rate = baud_rate
        self.set_samp_rate(self.baud_rate*100)
        self.set_transition_width(self.baud_rate/self.sps)
        self.blocks_repeat_0.set_interpolation(int(self.samp_rate/self.baud_rate))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, self.baud_rate*2.2, self.transition_width, window.WIN_HAMMING, 6.76))

    def get_transition_width(self):
        return self.transition_width

    def set_transition_width(self, transition_width):
        self.transition_width = transition_width
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, self.baud_rate*2.2, self.transition_width, window.WIN_HAMMING, 6.76))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_freqshift_cc_0.set_phase_inc(2.0*math.pi*self.freq_shift/self.samp_rate)
        self.blocks_repeat_0.set_interpolation(int(self.samp_rate/self.baud_rate))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, self.baud_rate*2.2, self.transition_width, window.WIN_HAMMING, 6.76))

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps

    def get_qpsk(self):
        return self.qpsk

    def set_qpsk(self, qpsk):
        self.qpsk = qpsk

    def get_path_loss(self):
        return self.path_loss

    def set_path_loss(self, path_loss):
        self.path_loss = path_loss
        self.blocks_multiply_const_vxx_0.set_k(self.path_loss)

    def get_hdr_2(self):
        return self.hdr_2

    def set_hdr_2(self, hdr_2):
        self.hdr_2 = hdr_2

    def get_hdr_1(self):
        return self.hdr_1

    def set_hdr_1(self, hdr_1):
        self.hdr_1 = hdr_1

    def get_freq_shift(self):
        return self.freq_shift

    def set_freq_shift(self, freq_shift):
        self.freq_shift = freq_shift
        self.blocks_freqshift_cc_0.set_phase_inc(2.0*math.pi*self.freq_shift/self.samp_rate)

    def get_arity(self):
        return self.arity

    def set_arity(self, arity):
        self.arity = arity




def main(top_block_cls=doppler, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
