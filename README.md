
Introduction
============

This project is inspired from https://github.com/funoverip/gr-cc1111/ project
GNU Radio blocks to handle CC1100 based packet format (header, CRC16). Whitening is coded but not use in decoder.

Provide the following GNU Radio blocks:
- "Packet Decoder (CC1100)" : Decode CC11xx formatted packets from a GR flow graph, and send payload to gr.myqueue_out().

Author
======
- Nicolas Hans
- http://domotique.nicohans.fr

Status
======
- Beta version
- Tested on GNURadio 3.7.4

Documentation
=============
- TODO
- Some more explanations on origin project can be found here: http://funoverip.net/2014/07/gnu-radio-cc1111-packets-encoderdecoder-blocks/
- See testing-scripts/* as complete examples (ribo sniffer)

Prerequisites
=============
On debian :


Installation
============

```
cd src/gr-cc1100
mkdir build
cd build
cmake ../
make 
sudo make install
```

