#!/usr/bin/python3

import csv
import random

# Randomly picks watchstanders from a csv file with name and points columns.
# Lower points are more likely to be selected.
# Output is in selection order.


def get_score(n, highest):
	# Subtract points from the highest in the pool. Adds one to prevent scores of zero.
	return highest - n + 1

# Read file, put names and points into seperate lists
watchstanders = []
points = []
with open('book1.csv','r') as f:
	reader = csv.reader(f.readlines())
	for row in reader:
		watchstanders.append(f"{row[1].ljust(4)}{row[0]}")
		points.append(int(row[1]))

# Calculate scores and make selections
highest = max(points)
scores = [get_score(i, highest) for i in points]
ws_count = len(watchstanders)
selected = []
while len(selected) < ws_count:
	pick = random.sample(watchstanders, k=1, counts=scores)[0]
	idx = watchstanders.index(pick)
	for i in watchstanders, points, scores:
		del i[idx]
	selected.append(pick)
	print(pick)
