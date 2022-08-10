#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Rds Bpsk Limesdr File Source
# Generated: Sun Sep 19 09:44:15 2021
##################################################


from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import limesdr
import math


class RDS_BPSK_LimeSDR_File_Source(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Rds Bpsk Limesdr File Source")

        ##################################################
        # Variables
        ##################################################
        self.tx_gain = tx_gain = 60
        self.tx_frequency = tx_frequency = 106500000
        self.tx_channel = tx_channel = 0
        self.stereo_gain = stereo_gain = .3
        self.sample_rate = sample_rate = 380000
        self.rds_gain = rds_gain = .5
        self.pilot_gain = pilot_gain = .3
        self.outbuffer = outbuffer = 10
        self.notes = notes = "Replays RDS data on repeat supplied from a file. No audio is added."
        self.input_gain = input_gain = .3
        self.fm_max_dev = fm_max_dev = 80000
        self.filepath = filepath = "/home/user/FISSURE/Crafted Packets/rdsA2.bin"

        ##################################################
        # Blocks
        ##################################################
        self.low_pass_filter_0 = filter.interp_fir_filter_fff(1, firdes.low_pass(
        	1, sample_rate, 2.5e3, .5e3, firdes.WIN_HAMMING, 6.76))
        (self.low_pass_filter_0).set_max_output_buffer(10)
        self.limesdr_sink_0 = limesdr.sink('', int(tx_channel), '', '')
        self.limesdr_sink_0.set_sample_rate(sample_rate)
        self.limesdr_sink_0.set_center_freq(tx_frequency, 0)
        self.limesdr_sink_0.set_bandwidth(5e6,0)
        self.limesdr_sink_0.set_gain(int(tx_gain),0)
        self.limesdr_sink_0.set_antenna(255,0)
        self.limesdr_sink_0.calibrate(5e6, 0)

        self.gr_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(2)
        (self.gr_unpack_k_bits_bb_0).set_max_output_buffer(10)
        self.gr_sub_xx_0 = blocks.sub_ff(1)
        self.gr_sig_source_x_0_1 = analog.sig_source_f(sample_rate, analog.GR_SIN_WAVE, 19e3, 1, 0)
        self.gr_sig_source_x_0_0 = analog.sig_source_f(sample_rate, analog.GR_SIN_WAVE, 57e3, 1, 0)
        self.gr_sig_source_x_0 = analog.sig_source_f(sample_rate, analog.GR_SIN_WAVE, 38e3, 1, 0)
        self.gr_multiply_xx_1 = blocks.multiply_vff(1)
        self.gr_multiply_xx_0 = blocks.multiply_vff(1)
        (self.gr_multiply_xx_0).set_max_output_buffer(10)
        self.gr_map_bb_1 = digital.map_bb(([1,2]))
        (self.gr_map_bb_1).set_max_output_buffer(10)
        self.gr_map_bb_0 = digital.map_bb(([-1,1]))
        (self.gr_map_bb_0).set_max_output_buffer(10)
        self.gr_frequency_modulator_fc_0 = analog.frequency_modulator_fc(2*math.pi*fm_max_dev/sample_rate)
        (self.gr_frequency_modulator_fc_0).set_max_output_buffer(10)
        self.gr_diff_encoder_bb_0 = digital.diff_encoder_bb(2)
        (self.gr_diff_encoder_bb_0).set_max_output_buffer(10)
        self.gr_char_to_float_0 = blocks.char_to_float(1, 1)
        (self.gr_char_to_float_0).set_max_output_buffer(10)
        self.gr_add_xx_1 = blocks.add_vff(1)
        (self.gr_add_xx_1).set_max_output_buffer(10)
        self.gr_add_xx_0 = blocks.add_vff(1)
        self.fractional_resampler_xx_0_0_0 = filter.fractional_resampler_cc(0, (sample_rate/10000)/100.0)
        self.fractional_resampler_xx_0_0 = filter.fractional_resampler_ff(0, 44.1/(sample_rate/1000))
        self.fractional_resampler_xx_0 = filter.fractional_resampler_ff(0, 44.1/(sample_rate/1000))
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, 160)
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_float*1)
        self.blocks_multiply_const_vxx_0_1 = blocks.multiply_const_vff((input_gain, ))
        self.blocks_multiply_const_vxx_0_0_1 = blocks.multiply_const_vff((pilot_gain, ))
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vff((rds_gain, ))
        (self.blocks_multiply_const_vxx_0_0).set_max_output_buffer(10)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((input_gain, ))
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, filepath, True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.fractional_resampler_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.gr_add_xx_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0_1, 0), (self.gr_add_xx_1, 1))
        self.connect((self.blocks_multiply_const_vxx_0_1, 0), (self.fractional_resampler_xx_0_0, 0))
        self.connect((self.blocks_null_source_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_null_source_0, 0), (self.blocks_multiply_const_vxx_0_1, 0))
        self.connect((self.blocks_repeat_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.gr_diff_encoder_bb_0, 0))
        self.connect((self.fractional_resampler_xx_0, 0), (self.gr_add_xx_0, 0))
        self.connect((self.fractional_resampler_xx_0, 0), (self.gr_sub_xx_0, 0))
        self.connect((self.fractional_resampler_xx_0_0, 0), (self.gr_add_xx_0, 1))
        self.connect((self.fractional_resampler_xx_0_0, 0), (self.gr_sub_xx_0, 1))
        self.connect((self.fractional_resampler_xx_0_0_0, 0), (self.limesdr_sink_0, 0))
        self.connect((self.gr_add_xx_0, 0), (self.gr_add_xx_1, 3))
        self.connect((self.gr_add_xx_1, 0), (self.gr_frequency_modulator_fc_0, 0))
        self.connect((self.gr_char_to_float_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.gr_diff_encoder_bb_0, 0), (self.gr_map_bb_1, 0))
        self.connect((self.gr_frequency_modulator_fc_0, 0), (self.fractional_resampler_xx_0_0_0, 0))
        self.connect((self.gr_map_bb_0, 0), (self.gr_char_to_float_0, 0))
        self.connect((self.gr_map_bb_1, 0), (self.gr_unpack_k_bits_bb_0, 0))
        self.connect((self.gr_multiply_xx_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.gr_multiply_xx_1, 0), (self.gr_add_xx_1, 2))
        self.connect((self.gr_sig_source_x_0, 0), (self.gr_multiply_xx_1, 0))
        self.connect((self.gr_sig_source_x_0_0, 0), (self.gr_multiply_xx_0, 0))
        self.connect((self.gr_sig_source_x_0_1, 0), (self.blocks_multiply_const_vxx_0_0_1, 0))
        self.connect((self.gr_sub_xx_0, 0), (self.gr_multiply_xx_1, 1))
        self.connect((self.gr_unpack_k_bits_bb_0, 0), (self.gr_map_bb_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.gr_multiply_xx_0, 1))

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.limesdr_sink_0.set_gain(int(self.tx_gain),0)
        self.limesdr_sink_0.set_gain(int(self.tx_gain),1)

    def get_tx_frequency(self):
        return self.tx_frequency

    def set_tx_frequency(self, tx_frequency):
        self.tx_frequency = tx_frequency
        self.limesdr_sink_0.set_center_freq(self.tx_frequency, 0)

    def get_tx_channel(self):
        return self.tx_channel

    def set_tx_channel(self, tx_channel):
        self.tx_channel = tx_channel

    def get_stereo_gain(self):
        return self.stereo_gain

    def set_stereo_gain(self, stereo_gain):
        self.stereo_gain = stereo_gain

    def get_sample_rate(self):
        return self.sample_rate

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.sample_rate, 2.5e3, .5e3, firdes.WIN_HAMMING, 6.76))
        self.gr_sig_source_x_0_1.set_sampling_freq(self.sample_rate)
        self.gr_sig_source_x_0_0.set_sampling_freq(self.sample_rate)
        self.gr_sig_source_x_0.set_sampling_freq(self.sample_rate)
        self.gr_frequency_modulator_fc_0.set_sensitivity(2*math.pi*self.fm_max_dev/self.sample_rate)
        self.fractional_resampler_xx_0_0_0.set_resamp_ratio((self.sample_rate/10000)/100.0)
        self.fractional_resampler_xx_0_0.set_resamp_ratio(44.1/(self.sample_rate/1000))
        self.fractional_resampler_xx_0.set_resamp_ratio(44.1/(self.sample_rate/1000))

    def get_rds_gain(self):
        return self.rds_gain

    def set_rds_gain(self, rds_gain):
        self.rds_gain = rds_gain
        self.blocks_multiply_const_vxx_0_0.set_k((self.rds_gain, ))

    def get_pilot_gain(self):
        return self.pilot_gain

    def set_pilot_gain(self, pilot_gain):
        self.pilot_gain = pilot_gain
        self.blocks_multiply_const_vxx_0_0_1.set_k((self.pilot_gain, ))

    def get_outbuffer(self):
        return self.outbuffer

    def set_outbuffer(self, outbuffer):
        self.outbuffer = outbuffer

    def get_notes(self):
        return self.notes

    def set_notes(self, notes):
        self.notes = notes

    def get_input_gain(self):
        return self.input_gain

    def set_input_gain(self, input_gain):
        self.input_gain = input_gain
        self.blocks_multiply_const_vxx_0_1.set_k((self.input_gain, ))
        self.blocks_multiply_const_vxx_0.set_k((self.input_gain, ))

    def get_fm_max_dev(self):
        return self.fm_max_dev

    def set_fm_max_dev(self, fm_max_dev):
        self.fm_max_dev = fm_max_dev
        self.gr_frequency_modulator_fc_0.set_sensitivity(2*math.pi*self.fm_max_dev/self.sample_rate)

    def get_filepath(self):
        return self.filepath

    def set_filepath(self, filepath):
        self.filepath = filepath
        self.blocks_file_source_0.open(self.filepath, True)


def main(top_block_cls=RDS_BPSK_LimeSDR_File_Source, options=None):

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()