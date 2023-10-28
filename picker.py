#!/usr/bin/python3

import csv
import random

"""
Randomly picks watchstanders from a csv file where column 0 is name, column 1 is points.
Watchstanders with lower points are more likely to be picked. Output is in selection order.
"""

def weigh_in(n, highscore):
	return highscore - n + 1

# Read file, make list
watchstanders = []
with open('book1.csv','r') as f:
	f.readline() # skip header row
	reader = csv.reader(f.readlines())
	for row in reader:
		watchstanders.append(row)

points = [int(w[1]) for w in watchstanders]
highscore = max(points)
weights = [weigh_in(i, highscore) for i in points]
selected = []
while len(watchstanders) > 0:
	pick = random.choices(watchstanders, weights=weights)[0]
	idx = watchstanders.index(pick)
	del watchstanders[idx]
	del weights[idx]
	
	selected.append(pick)
	print(f"{pick[0]}")
