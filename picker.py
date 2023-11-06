#!/usr/bin/python3

import csv
from random import choices
from statistics import median

"""
Randomly picks watchstanders from a csv file (with header row).
Column 0 must be name, column 1 must be points. Other columns are ignored.
Lower points are more likely to be selected.
"""

class Watchstander:
	def __init__(self, csvrow):	
		self.row = csvrow
		
	def __str__(self):
		return f"{self.name.ljust(15)} {str(self.points).rjust(3)}"
		
	@property
	def name(self):
		return self.row[0]

	@property
	def points(self):
		return int(self.row[1])

	@points.setter
	def points(self, n: int):
		self.row[1] = str(n)

	@property
	def weight(self):
		return max_score - self.points + 1


# Read file, make list
rows = []
with open('book1.csv', 'r') as f:
	reader = csv.reader(f.readlines())
	rows = [i for i in reader]
header_row = rows[0]
watchstanders = [Watchstander(i) for i in rows[1:]]
del rows

# quickmaths
points = [i.points for i in watchstanders]
min_score, max_score = min(points), max(points)
median_score = median(points)

print(f"Median score: {median_score}")
print(f"Spread:       {max_score - min_score}")
print("---")

selected = []
while len(watchstanders) > 0:
	pick = choices(watchstanders, weights=[w.weight for w in watchstanders])[0]
	del watchstanders[watchstanders.index(pick)]
	selected.append(pick)
	print(f"{pick} " + "." * int((pick.points / median_score)))

# Save new csv file in selection order
with open('selected.csv', 'w') as f:
	writer = csv.writer(f)
	writer.writerow(header_row)
	writer.writerows([i.row for i in selected])
	print("---")
	print("Output saved to selected.csv")
