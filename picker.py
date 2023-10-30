#!/usr/bin/python3

import csv
import random

"""
Randomly picks watchstanders from a csv file. Column 0 is name, column 1 is points.
Watchstanders with lower points are more likely to be picked. Output is in selection order.
"""

def weigh_in(n, highscore):
	return highscore - n + 1

# Read file, make list
watchstanders = []
with open('book1.csv', 'r') as f:
	reader = csv.reader(f.readlines())
	for row in reader:
		watchstanders.append(row)

# Skip row header
row_header = None
if "name" in watchstanders[0][0].lower():
	row_header = watchstanders[0]
	del watchstanders[0]

# Make selections
points = [int(w[1]) for w in watchstanders]
highscore = max(points)
weights = [weigh_in(i, highscore) for i in points]
selected = []
while len(watchstanders) > 0:
	pick = random.choices(watchstanders, weights=weights)[0]
	idx = watchstanders.index(pick)
	selected.append(pick)
	
	print(f"{pick[0]}")
	del watchstanders[idx]
	del weights[idx]
	
# Save results
with open('selected.csv', 'w') as f:
	writer = csv.writer(f)
	if row_header is not None:
		writer.writerow(row_header)
	writer.writerows(selected)
print("Selection saved to selected.csv")
