


# ── List of field names every POST body must include
REQUIRED_FIELDS = ["name", "population", "capital", "year"]


def validate_country(data, partial=False):
    """
    Validate a dictionary of country field values.

    Parameters:
        data    (dict) — the JSON body received from the client
        partial (bool) — if True, skip "required field" checks (used by PUT
                         so that clients can update just one field at a time)

    Returns:
        str | None — an error message string if validation fails,
                     or None if all provided values are acceptable.

    Task 3 (POST): partial=False  → checks both presence and value rules
    Task 4 (PUT):  partial=True   → checks only value rules for sent fields
    """

    # ── 1. Required-field presence check (POST only)
    if not partial:
        for field in REQUIRED_FIELDS:
            if field not in data:
                # Task 3: return 400 Bad Request if any required field missing
                return f"Missing required field: {field}"

    # ── 2. Value-level checks (apply whenever the field is present)

    # name: must be a non-empty string
    if "name" in data:
        if not isinstance(data["name"], str) or not data["name"].strip():
            return "Field 'name' must be a non-empty string"

    # population: must be an integer between 1 and 2,000,000,000
    if "population" in data:
        pop = data["population"]
        if not isinstance(pop, int) or isinstance(pop, bool):
            return "Field 'population' must be an integer"
        if not (1 <= pop <= 2_000_000_000):
            return "Field 'population' must be between 1 and 2,000,000,000"

    # capital: must be a non-empty string
    if "capital" in data:
        if not isinstance(data["capital"], str) or not data["capital"].strip():
            return "Field 'capital' must be a non-empty string"

    # year: must be an integer (independence year — no upper/lower bound set
    # in the spec, but we ensure it's actually a number, not a float/bool)
    if "year" in data:
        yr = data["year"]
        if not isinstance(yr, int) or isinstance(yr, bool):
            return "Field 'year' must be an integer"

    # All checks passed
    return None
