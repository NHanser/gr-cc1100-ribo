/* -*- c++ -*- */

#define CC1100_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "cc1100_swig_doc.i"

%{
#include "cc1100/cc1100_packet_decoder.h"
%}


%include "cc1100/cc1100_packet_decoder.h"
GR_SWIG_BLOCK_MAGIC2(cc1100, cc1100_packet_decoder);
