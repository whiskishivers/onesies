#!/usr/bin/python3

import argparse
import json
from collections import defaultdict
from subprocess import Popen, PIPE

""" Read PCAP file containing OSPF Router LSAs and summarize them """

parser = argparse.ArgumentParser(
    description="Summarize links found in OSPF link state advertisements."
)
parser.add_argument("filename", help="pcap file path")
parser.add_argument("--tshark", default="/usr/bin/tshark", help="path to tshark binary (default: /usr/bin/tshark)")
args = parser.parse_args()

# Read pcap, pipe to tshark, get json
with open(args.filename, "rb") as f:
    with Popen([args.tshark, "-r-", "-Tjson", "-Y", "ospf.lsa.number_of_links gt 0 and ospf.lsa eq 1"], stdin=PIPE,
               stdout=PIPE) as p:
        r = p.communicate(input=f.read())
packets = json.loads(r[0])

link_labels = {"1": ("1 PTP    ", "Neighbor:", "Router IP:  "),
               "2": ("2 Transit", "Link ID: ", "Link Data:  "),
               "3": ("3 Stub   ", "Network: ", "Mask:       "),
               "4": ("4 Virtual", "Link ID: ", "Link Data:  ")
               }
lsa_type_field_names = ["ospf.lsa.router.linktype", "ospf.lsa.router.linkid", "ospf.lsa.router.linkdata"]
entries = defaultdict(set)
counter = 0

# Parse update packets for links
for pkt in packets:
    try:
        lsa_update = pkt["_source"]["layers"]["ospf"]["LS Update Packet"]
        for lsa_type, lsa_type_fields in lsa_update.items():
            if lsa_type.startswith("LSA-type "):
                router_id = lsa_type_fields["ospf.lsa.id"]
                for field, v in lsa_type_fields.items():
                    if field.startswith("Type:"):
                        data = tuple([v[i] for i in lsa_type_field_names])
                        entries[router_id].add(data)
                        counter += 1
    except:
        print("error")
        continue

# Output
print(f"Summary of {len(packets)} packets and {counter} updates.")
for k, v in entries.items():
    print(f"Router: {k}")
    for line in sorted(v):
        type_id, link_id, link_data = line
        label = link_labels[type_id]
        star = ""
        if type_id in "1" and link_id in entries.keys():
            star = "*"
        print(f" {label[0]} {label[1]} {str(link_id + star).ljust(15)} {label[2]} {link_data}")
