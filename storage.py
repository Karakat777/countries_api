import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "countries.json")

def load():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save(countries):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(countries, f, indent=2, ensure_ascii=False)
