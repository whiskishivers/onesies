#!/usr/bin/python3

import argparse
import json

"""
Creates a Kibana filter for matching one field to
many values from one or more text files.
Originally for zeek logs, but the field name can be modified.
"""

parser = argparse.ArgumentParser(
    description="Create a Kibana filter for matching a field to values in lines from text files."
)
parser.add_argument("--field", default="related.ip", help="The field to match (default: related.ip)")
parser.add_argument("filepath", nargs="+", help="Path to the text file")
args = parser.parse_args()

all_lines = set()
phrases = []
for path in args.filepath:
    with open(path, 'r') as f:
        all_lines.update(i.strip() for i in f.readlines())

for line in all_lines:
    phrases.append({"match_phrase": {args.field: line}})

qry = {"query": {
    "bool": {
        "should": phrases,
        "minimum_should_match": 1  # is this default?
    }
}}

print(json.dumps(qry))
