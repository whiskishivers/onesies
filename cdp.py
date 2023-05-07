#!/usr/bin/python3

import argparse
import os
from subprocess import Popen, PIPE

""" Print interesting device info found in cisco discovery protocol packets """

def printlines(iterable):
	for i in iterable:
		print(i)
	return

TSHARK = '/usr/bin/tshark'

parser = argparse.ArgumentParser(
    description = "Summarize ports found in CDP traffic."
)
parser.add_argument('pcappath', help = "PCAP file path.")
args = parser.parse_args()

path = args.pcappath

# tshark -r (file) -Y cdp -Tfields -e _ws.col.Info | sort -u
# tshark -r (file) -Y cdp -Tfields -e eth.src -e cdp.deviceid -e cdp.portid | sort -u

with open(path,'rb') as f:
    with Popen([TSHARK, '-r-', '-Ycdp', '-Tfields', '-eeth.src', '-ecdp.deviceid', '-ecdp.portid'], stdin=PIPE, stdout=PIPE) as p:
        r = p.communicate(input=f.read())
lines = list(set(r[0].decode('utf8').split('\n')))
lines.sort()
printlines(lines)

