#!/usr/bin/python3

import argparse
import os
import json
from collections import defaultdict
from subprocess import Popen, PIPE
from pprint import pprint

""" Read PCAP file containing OSPF Router LSAs and summarize them """

TSHARK = '/usr/bin/tshark'


parser = argparse.ArgumentParser(
    prog ="OSPF LSA summarizer",
    description = "Summarize links found in OSPF packets from a PCAP file."
)
parser.add_argument('filename', help = "The path to the PCAP file.")
args = parser.parse_args()

path = args.filename


# Labels for Router lsa types
# (Type field, Link ID field, Link Data field)
linklabels = {"1": ("Type: PTP    ", "Neighbor ID:", "Router IP:  "),
              "2": ("Type: Transit", "Link ID:    ", "Link Data:  "),
              "3": ("Type: Stub   ", "Network:    ", "Mask:       "),
              "4": ("Type: Virtual", "Link ID:    ", "Link Data:  ")
}

fields = ["ospf.lsa.router.linktype","ospf.lsa.router.linkid", "ospf.lsa.router.linkdata"]

# Read pcap into memory, feed tshark, get jsonified OSPF LS Update packets
with open(path,'rb') as f:
    with Popen([TSHARK, '-r-', '-Tjson', '-Y', 'ospf.lsa.number_of_links gt 0 && ospf.lsa == 1'], stdin=PIPE, stdout=PIPE) as p:
        r = p.communicate(input=f.read())

pkts = json.loads(r[0])

entries = defaultdict(set)

# Parse packets, put Type field information into entries dictionary
for pkt in pkts:
    try:
        lsaupdate = pkt["_source"]["layers"]["ospf"]["LS Update Packet"]
        for lsatype,typefields in lsaupdate.items():
            if lsatype.startswith("LSA-type "):
                routerid = typefields["ospf.lsa.id"]
                print(f"==={lsatype}===")
                for field, v in typefields.items():
                    if field.startswith("Type:"):
                        data = tuple([v[i] for i in fields])
                        entries[routerid].add(data)
    except:
        continue

# Output
for k, v in entries.items():
    print(f"Router: {k}")
    for line in sorted(v):
        typeid, linkid, datafield = line
        labels = linklabels[typeid]
        star = ""
        if typeid in ("1") and linkid in entries.keys():
            star = "*"
        print(f"    {labels[0]} {labels[1]} {str(linkid + star).ljust(15)} {labels[2]} {datafield}")

