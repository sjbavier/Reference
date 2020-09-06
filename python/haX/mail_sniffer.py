#!/usr/bin/python3

from scapy.all import *

# out packet callback
def packet_callback(packet):
    print(packet.show())

# fire up our sniffer
sniff(prn=packet_callback,count=10)
