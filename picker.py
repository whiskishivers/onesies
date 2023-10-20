#!/usr/bin/python3

import csv
import random

# Reads a csv file with watchstander name and watch count columns.
# Output is in selection order.
# Prioritizes lower watch counts for selection.

def get_score(n, highest):
	return highest + 1 - n

# Put watchstanders and watch counts into lists
ws = []
c = []
with open('book1.csv','r') as f:
	reader = csv.reader(f.readlines())
	for row in reader:
		ws.append(f"{row[0].ljust(15)} {row[1]}")
		c.append(int(row[1]))

# Score priority
highest = max(c)
scores = [get_score(i, highest) for i in c]

# Make selections
ws_count = len(ws)
selected = []
while len(selected) < ws_count:
	pick = random.sample(ws, k=1, counts=scores)[0]
	idx = ws.index(pick)
	del ws[idx]
	del c[idx]
	del scores[idx]
	selected.append(pick)
	print(pick)

