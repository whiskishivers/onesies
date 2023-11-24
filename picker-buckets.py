#!/usr/bin/python3

import csv
from random import choices
from statistics import median
from itertools import zip_longest

"""
Made to assist in watchbill creation. Reads a csv file that includes a
header row. Column 0 must be Name and Column 1 must be points. Splits
watchstanders by median points, then randomly picks based on the defined
ratio and the amount of points a watchstander has. Lower scores are more
likely to be selected before higher scores.

Creates a new csv file with the rows in order by selection.
"""

# Low:high pick ratio: x,y
# Pick x low group members before y high group members.
pick_ratio = 5,1

class Watchstander:
	def __init__(self, csvrow: list):	
		self.row = csvrow
	def __str__(self):
		return f"{self.name.ljust(15)} {str(self.points).rjust(3)}"	
	@property
	def name(self):
		return self.row[0]
	@property
	def points(self):
		return int(self.row[1])
	@property
	def weight(self):
		return max_score - self.points + 1

# Make list
rows = []
with open('book1.csv', 'r') as f:
	reader = csv.reader(f.readlines())
	rows = list(reader)
header_row = rows[0]
watchstanders = [Watchstander(i) for i in rows[1:]]

# Make groups
points = [i.points for i in watchstanders]
max_score, median_score = max(points), median(points)
low_bucket = [i for i in watchstanders if i.points < median_score]
high_bucket = [i for i in watchstanders if i.points >= median_score]

# Make selections
print("---Selection Order---")
selected = []
while len(low_bucket) + len(high_bucket) > 0:
	for bucket, ratio in ((low_bucket, pick_ratio[0]), (high_bucket, pick_ratio[1])):
		try:
			for _ in range(ratio):
				pick = choices(bucket, weights=[w.weight for w in bucket])[0]
				del bucket[bucket.index(pick)]
				selected.append(pick)
				print(pick)
		except IndexError:
			continue
# Save selection order
with open('selected.csv', 'w') as f:
	writer = csv.writer(f)
	writer.writerow(header_row)
	writer.writerows([i.row for i in selected])
print("Output saved to selected.csv")
