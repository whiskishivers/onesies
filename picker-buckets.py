import csv
import random
from statistics import median
from dataclasses import dataclass
from typing import List


@dataclass
class Watchstander:
    name: str
    points: int
    notes: str
    shift_pref: str
    original_row: dict
    status: str = ""  # above or below median

    @property
    def weight(self) -> float:
        """Higher points = Higher chance of being picked early (to be flipped to the bottom)."""
        return float(self.points + 1)


def read_watchstanders(file_path: str) -> List[Watchstander]:
    watchstanders = []
    try:
        with open(file_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                watchstanders.append(Watchstander(
                    name=row.get("Name", "Unknown"),
                    points=int(row.get("Points", 0)),
                    notes=row.get("Notes", ""),
                    shift_pref=row.get("Shift Preference", ""),
                    original_row=row
                ))
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return []
    return watchstanders


def perform_weighted_selection(pool: List[Watchstander]) -> List[Watchstander]:
    if not pool:
        return []

    med_score = median(w.points for w in pool)
    temp_pool = pool[:]
    picked_high_to_low = []

    # 1. Pick based on raw score (Higher score = Picked sooner)
    while temp_pool:
        weights = [w.weight for w in temp_pool]
        pick = random.choices(temp_pool, weights=weights, k=1)[0]

        # Tag the status based on the median
        if pick.points >= med_score:
            pick.status = "Above"
        else:
            pick.status = "Below"

        picked_high_to_low.append(pick)
        temp_pool.remove(pick)

    # 2. Flip the list so low-point people are at the top
    return list(reversed(picked_high_to_low))


def main():
    INPUT_FILE = 'book1.csv'

    roster = read_watchstanders(INPUT_FILE)
    if not roster:
        return

    # Combined list with status tags
    final_list = perform_weighted_selection(roster)

    # Calculate median just for the display header
    med = median(w.points for w in roster)

    print(f"\n--- Unified Watchbill (Median: {med}) ---")
    fmt = "{:<18} | {:>3} | {:<8} | {:<15} | {}"
    print(fmt.format("Name", "Pts", "Status", "Shift Pref", "Notes"))
    print("-" * 75)

    for p in final_list:
        print(fmt.format(p.name, p.points, p.status, p.shift_pref, p.notes))


if __name__ == "__main__":
    main()