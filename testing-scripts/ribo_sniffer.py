#!/usr/bin/env python
#=============================================================
# Securitas-Direct (Verisure) RF sniffer
# By Jerome Nokin (https://funoverip.net / @funoverip)
#=============================================================
#
# Usage: ribo_sniffer.py 
#
#
#=============================================================

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import cc1100
import math
import osmosdr

class grc_cc1100_ribo_receiver_2(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Ribo receiver")

        ##################################################
        # Variables
        ##################################################
        self.symbol_rate = symbol_rate = 2400
        self.samp_rate = samp_rate = 2000000
        self.rat_interop = rat_interop = 8
        self.rat_decim = rat_decim = 5
        self.firdes_transition_width = firdes_transition_width = 11000
        self.firdes_decim = firdes_decim = 4
        self.firdes_cutoff = firdes_cutoff = 11000
        self.samp_per_sym = samp_per_sym = ((samp_rate/2/firdes_decim)*rat_interop/rat_decim)/symbol_rate
        self.myqueue_out = myqueue_out = gr.msg_queue(2)
        self.frequency_shift = frequency_shift = 513000
        self.frequency_center = frequency_center = 868303000
        self.firdes_filter = firdes_filter = firdes.low_pass(1,samp_rate/2,firdes_cutoff,firdes_transition_width)
        self.fft_sp = fft_sp = 50000
        self.access_code = access_code = "10011011101011011001101110101101"

        ##################################################
        # Blocks
        ##################################################
        self.rtlsdr_source = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_source.set_sample_rate(samp_rate)
        self.rtlsdr_source.set_center_freq(frequency_center - frequency_shift, 0)
        self.rtlsdr_source.set_freq_corr(0, 0)
        self.rtlsdr_source.set_dc_offset_mode(0, 0)
        self.rtlsdr_source.set_iq_balance_mode(0, 0)
        self.rtlsdr_source.set_gain_mode(False, 0)
        self.rtlsdr_source.set_gain(10, 0)
        self.rtlsdr_source.set_if_gain(20, 0)
        self.rtlsdr_source.set_bb_gain(20, 0)
        self.rtlsdr_source.set_antenna("", 0)
        self.rtlsdr_source.set_bandwidth(0, 0)
          
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=rat_interop,
                decimation=rat_decim,
                taps=None,
                fractional_bw=None,
        )
        self.freq_xlating_fir_filter_xxx_1 = filter.freq_xlating_fir_filter_ccc(4, (firdes_filter), 0, samp_rate/2)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(2, (1, ), frequency_shift, samp_rate)
        self.digital_correlate_access_code_bb_0 = digital.correlate_access_code_bb(access_code, 0)
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(samp_per_sym*(1+0.0), 0.25*0.175*0.175, 0.5, 0.175, 0.005)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.cc1100_cc1100_packet_decoder_0 = cc1100.cc1100_packet_decoder(myqueue_out,False, True, False, False)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate/2,True)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_char*1)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(2)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.cc1100_cc1100_packet_decoder_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.digital_correlate_access_code_bb_0, 0))
        self.connect((self.digital_correlate_access_code_bb_0, 0), (self.cc1100_cc1100_packet_decoder_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_1, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.freq_xlating_fir_filter_xxx_1, 0))
        self.connect((self.rtlsdr_source, 0), (self.freq_xlating_fir_filter_xxx_0, 0))



    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.set_samp_per_sym(((self.samp_rate/2/self.firdes_decim)*self.rat_interop/self.rat_decim)/self.symbol_rate)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samp_per_sym(((self.samp_rate/2/self.firdes_decim)*self.rat_interop/self.rat_decim)/self.symbol_rate)
        self.set_firdes_filter(firdes.low_pass(1,self.samp_rate/2,self.firdes_cutoff,self.firdes_transition_width))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate/2)
        self.rtlsdr_source.set_sample_rate(self.samp_rate)

    def get_rat_interop(self):
        return self.rat_interop

    def set_rat_interop(self, rat_interop):
        self.rat_interop = rat_interop
        self.set_samp_per_sym(((self.samp_rate/2/self.firdes_decim)*self.rat_interop/self.rat_decim)/self.symbol_rate)

    def get_rat_decim(self):
        return self.rat_decim

    def set_rat_decim(self, rat_decim):
        self.rat_decim = rat_decim
        self.set_samp_per_sym(((self.samp_rate/2/self.firdes_decim)*self.rat_interop/self.rat_decim)/self.symbol_rate)

    def get_firdes_transition_width(self):
        return self.firdes_transition_width

    def set_firdes_transition_width(self, firdes_transition_width):
        self.firdes_transition_width = firdes_transition_width
        self.set_firdes_filter(firdes.low_pass(1,self.samp_rate/2,self.firdes_cutoff,self.firdes_transition_width))

    def get_firdes_decim(self):
        return self.firdes_decim

    def set_firdes_decim(self, firdes_decim):
        self.firdes_decim = firdes_decim
        self.set_samp_per_sym(((self.samp_rate/2/self.firdes_decim)*self.rat_interop/self.rat_decim)/self.symbol_rate)

    def get_firdes_cutoff(self):
        return self.firdes_cutoff

    def set_firdes_cutoff(self, firdes_cutoff):
        self.firdes_cutoff = firdes_cutoff
        self.set_firdes_filter(firdes.low_pass(1,self.samp_rate/2,self.firdes_cutoff,self.firdes_transition_width))

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym
        self.digital_clock_recovery_mm_xx_0.set_omega(self.samp_per_sym*(1+0.0))

    def get_myqueue_out(self):
        return self.myqueue_out

    def set_myqueue_out(self, myqueue_out):
        self.myqueue_out = myqueue_out

    def get_frequency_shift(self):
        return self.frequency_shift

    def set_frequency_shift(self, frequency_shift):
        self.frequency_shift = frequency_shift
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.frequency_shift)
        self.rtlsdr_source.set_center_freq(self.frequency_center - self.frequency_shift, 0)

    def get_frequency_center(self):
        return self.frequency_center

    def set_frequency_center(self, frequency_center):
        self.frequency_center = frequency_center
        self.rtlsdr_source.set_center_freq(self.frequency_center - self.frequency_shift, 0)

    def get_firdes_filter(self):
        return self.firdes_filter

    def set_firdes_filter(self, firdes_filter):
        self.firdes_filter = firdes_filter
        self.freq_xlating_fir_filter_xxx_1.set_taps((self.firdes_filter))

    def get_fft_sp(self):
        return self.fft_sp

    def set_fft_sp(self, fft_sp):
        self.fft_sp = fft_sp

    def get_access_code(self):
        return self.access_code

    def set_access_code(self, access_code):
        self.access_code = access_code



import ctypes
import sys
import datetime
import argparse
#from grc.ribo_receiver      import ribo_receiver
from threading              import Thread
from binascii               import hexlify, unhexlify
from time                   import sleep
import signal
import sys
 
# Colors
def pink(t):    return '\033[95m' + t + '\033[0m'
def blue(t):    return '\033[94m' + t + '\033[0m'
def yellow(t):  return '\033[93m' + t + '\033[0m'
def green(t):   return '\033[92m' + t + '\033[0m'
def red(t):     return '\033[91m' + t + '\033[0m'
 
# Thread dedicated to GNU Radio flowgraph
class flowgraph_thread(Thread):
    def __init__(self, flowgraph):
        Thread.__init__(self)
        self.setDaemon(1)
        self._flowgraph = flowgraph
 
    def run(self):
        self._flowgraph.start()
    #print "FFT Closed/Killed"
  
# Generate timestamp
def get_time():
    current_time = datetime.datetime.now().time()
    return current_time.isoformat()
 
# Print out frames to stdout
def dump_frame(frame,f):
 
    # Dissecting frame
    pkt_len = hexlify(frame[0:1])
    src_id  = hexlify(frame[1:2])
    dst_id  = hexlify(frame[2:4])
    unkn1   = hexlify(frame[4:8])
    unkn2   = hexlify(frame[9:10])
    cons    = hexlify(frame[10:11])
    temp    = hexlify(frame[11:12])

    consVal = int(cons,16);
    decim = consVal & 0x03;
    consVal >>= 2;
    consFloat = consVal + 0.25*decim;

    tempVal = int(temp,16);
    decim = tempVal & 0x03;
    tempVal >>= 2;
    tempFloat = tempVal + 0.25*decim;
	
 
    # Print out the frame
    print "[%s] %s %s %s %s %s %s %s (consigne : %f C | thermostat : %f C)" % (get_time(), pkt_len, green(src_id), red(dst_id), blue(unkn1), unkn2, pink(cons), yellow(temp),consFloat, tempFloat)
    f.write("[%s] %s %s %s %s %s %s %s (consigne : %f C | thermostat : %f C)\n" % (get_time(), pkt_len, green(src_id), red(dst_id), blue(unkn1), unkn2, pink(cons), yellow(temp),consFloat, tempFloat))
    f.flush()


# rf object
flowgraph = ''

def signal_handler(signal, frame):
	global flowgraph
        print('You pressed Ctrl+C!')
	flowgraph.stop()
	f.close()
        sys.exit(0)
 
# Main entry point
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('logfile', metavar='logfile',
                    help='Where logs will be append')
	args = parser.parse_args()
	f = open(args.logfile,'a')
	signal.signal(signal.SIGINT, signal_handler)
	try:
		# Initializing GNU Radio flowgraph
		flowgraph = grc_cc1100_ribo_receiver_2()
		flowgraph.start()
		# Some additional output
		print "[%s] Starting flowgraph" % get_time()
		f.write("[%s] Starting flowgraph\n" % get_time())
		f.flush()
		while True:
			frame = flowgraph.myqueue_out.delete_head().to_string()
			dump_frame(frame,f)
  
		# print "[%s] Exiting" % (get_time())
	except KeyboardInterrupt:
		print("W: interrupt received, proceeding")
