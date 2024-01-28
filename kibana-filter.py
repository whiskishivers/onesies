#!/usr/bin/python3

import argparse
import json

"""
Creates a Kibana filter that matches one field to many values in text files.
"""

parser = argparse.ArgumentParser(
    description="Creates a Kibana filter that matches one field to many values in text files.",
    epilog="Text files must have one field value per line. Duplicate lines are ignored."
)
parser.add_argument("--field", default="related.ip", help="field to match (default: related.ip)")
parser.add_argument("--pretty", action="store_true", help="format output for readability")
parser.add_argument("filepath", nargs="+", help="text file to read values from")
args = parser.parse_args()

all_lines = set()
phrases = []

for p in args.filepath:
    with open(p, 'r') as f:
        all_lines.update(i.strip() for i in f.readlines())

query = {"query": {"bool": {"should": [], "minimum_should_match": 1}}}

for line in all_lines:
    query["query"]["bool"]["should"].append({"match_phrase": {args.field: line}})

indent = None
if args.pretty:
    indent = 1
print(json.dumps(query, indent=indent))
