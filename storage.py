import json
import os

# Path to the data file, relative to this file's location.
# Using os.path keeps it portable across operating systems.
DATA_FILE = os.path.join(os.path.dirname(__file__), "countries.json")


def load():

    # Task 2 requirement: if no records exist yet, return [] not an error
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)   # parse JSON array → Python list
        except json.JSONDecodeError:
            # File exists but contains invalid JSON → treat as empty
            return []


def save(countries):

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(countries, f, indent=2, ensure_ascii=False)
