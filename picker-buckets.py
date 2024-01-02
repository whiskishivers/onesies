#!/usr/bin/python3

import csv
from random import choices
from statistics import median

"""
Assists watchbill creation. Reads a csv file with "Name", "Points", and "Notes"
fields at minimum. Creates low and high groups based on the median score then
randomly selects watchstanders in each group, preferring lower scores first.
Saves a new csv file in selection order.
"""


class Watchstander:
    def __init__(self, csvrow):
        self.row = csvrow

    def __str__(self):
        return f"{self.name.ljust(15)} {str(self.points).rjust(3)}  {self.notes}"

    @property
    def name(self):
        return self.row["Name"]

    @property
    def notes(self):
        return self.row["Notes"]

    @property
    def points(self):
        return int(self.row["Points"])

    @property
    def weight(self):
        """The inverse of points."""
        if self.points < 0:
            return 1.0
        return 1 / (self.points + 1)


def read_csv(file_path: str):
    """Reads rows, returns list of Watchstander objects."""
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        watchstanders = [Watchstander(row) for row in reader]
    return watchstanders


def make_selection(watchstanders):
    """Returns new selection lists and the median score."""
    median_score = median([i.points for i in watchstanders])
    low_bucket, high_bucket = [], []
    weights = [i.weight for i in watchstanders]

    while len(watchstanders):
        idx = choices(range(len(watchstanders)), weights=weights)[0]
        pick = watchstanders[idx]
        if pick.points < median_score:
            low_bucket.append(pick)
        else:
            high_bucket.append(pick)
        del watchstanders[idx]
        del weights[idx]

    return low_bucket, high_bucket, median_score


def save_csv(file_path: str, selected: list) -> None:
    """Create new csv file."""
    fieldnames = selected[0].row.keys()
    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows([i.row for i in selected])


def main():
    input_file = 'book1.csv'
    output_file = 'selected.csv'

    watchstanders = read_csv(input_file)
    low_bucket, high_bucket, med_score = make_selection(watchstanders)
    selection_list = low_bucket + high_bucket

    print(f"---{len(low_bucket)} Below Median---")
    print('\n'.join(map(str, low_bucket)))
    print(f"---{len(high_bucket)} Above Median---")
    print('\n'.join(map(str, high_bucket)))
    print("---")
    print(f"Count: {len(selection_list)}")
    print(f"Median score: {med_score}")

    save_csv(output_file, selection_list)

    print(f'Output saved to {output_file}')


if __name__ == "__main__":
    main()
