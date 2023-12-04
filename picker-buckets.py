#!/usr/bin/python3

import csv
from random import choices
from statistics import median

"""
Made to assist in watchbill creation. Reads a csv file that includes a
header row. Column 0 must be Name and Column 1 must be points. Splits
watchstanders by median points, then randomly picks based on the defined
ratio and points. Lower scores are more likely to be selected before
higher scores.
Creates a new csv file with the rows in order of selection.
"""

# Selection ratio low to high
PICK_RATIO = (5, 1)


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
        return 1 / (self.points + 1)


def read_csv(file_path: str):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        header_row = next(reader)
        watchstanders = [Watchstander(i) for i in reader]
    return header_row, watchstanders


def make_selection(watchstanders, pick_ratio):
    median_score = median([i.points for i in watchstanders])
    # Split low and high points
    low_bucket, high_bucket = [], []
    for i in watchstanders:
        if i.points < median_score:
            low_bucket.append(i)
        else:
            high_bucket.append(i)

    selected = []
    while len(low_bucket) + len(high_bucket) > 0:
        for bucket, ratio in [(low_bucket, pick_ratio[0]), (high_bucket, pick_ratio[1])]:
            try:
                for _ in range(ratio):
                    pick = choices(bucket, weights=[w.weight for w in bucket])[0]
                    del bucket[bucket.index(pick)]
                    selected.append(pick)
            except IndexError:
                continue

    return selected, median_score


def save_csv(file_path: str, header_row: list, selected: list) -> None:
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header_row)
        writer.writerows([i.row for i in selected])


def main():
    input_file = 'book1.csv'
    output_file = 'selected.csv'

    header_row, watchstanders = read_csv(input_file)
    selected, med_score = make_selection(watchstanders, PICK_RATIO)

    print("---Selection Order---")
    print('\n'.join(map(str, selected)))
    print(f"Median: {med_score}")
    print(f"Count: {len(watchstanders)}")

    save_csv(output_file, header_row, selected)
    print("Output saved to", output_file)


if __name__ == "__main__":
    main()
