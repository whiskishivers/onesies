#!/usr/bin/python3

import csv
import random

# Randomly picks watchstanders from a csv file with name and points columns.
# Lower points are more likely to be selected.
# Output is in selection order.

class Watchstander:
	def __init__(self, name, points):
		self.name = name
		self.points = points
	
	def __str__(self):
		return f"{self.name.ljust(15)} {self.points}"

def weigh_in(n, highscore):
	return highscore - n + 1

# Read file, make list
watchstanders = []
with open('book1.csv','r') as f:
	f.readline() # skip header row
	reader = csv.reader(f.readlines())
	for row in reader:
		watchstanders.append(Watchstander(row[0],int(row[1])))

selected = []
while len(watchstanders) > 0:
	# Calculate relative weights, make selection
	highscore = max([w.points for w in watchstanders])
	weights = [weigh_in(w.points, highscore) for w in watchstanders]
	pick = random.choices(watchstanders, weights=weights)[0]
	idx = watchstanders.index(pick)
	selected.append(pick)
	
	print(pick)
	del watchstanders[idx]
	del weights[idx]
