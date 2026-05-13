from flask import Blueprint, jsonify, request
from storage import load, save
from validation import validate_country
# Blueprint groups all /countries routes; registered in app.py
countries_bp = Blueprint("countries", __name__)


# Task 2 + Task 6: GET /countries
# Returns ALL countries, optionally filtered by query parameters.

@countries_bp.route("/countries", methods=["GET"])
def get_all_countries():

    countries = load()  # read all records from countries.json

    # ── Task 6: read optional query parameters ────────────────────────────
    # request.args.get() returns None if the parameter is absent,
    # so we can safely check with an if statement.
    capital_filter = request.args.get("capital")   # e.g. ?capital=Astana
    min_pop_filter = request.args.get("min_pop")   # e.g. ?min_pop=1000000

    # ── Task 6: apply capital filter ─────────────────────────────────────
    if capital_filter:
        # Case-insensitive comparison so "astana" matches "Astana"
        countries = [
            c for c in countries
            if c["capital"].lower() == capital_filter.lower()
        ]

    # ── Task 6: apply minimum population filter ───────────────────────────
    if min_pop_filter:
        try:
            min_pop = int(min_pop_filter)
        except ValueError:
            # Client passed a non-numeric value → 400 Bad Request
            return jsonify({"error": "min_pop must be an integer"}), 400
        countries = [c for c in countries if c["population"] >= min_pop]

    # Return 200 OK with the (possibly filtered) list
    return jsonify({"countries": countries}), 200



# Task 2: GET /countries/<id>
# Returns a single country record by its unique ID.

@countries_bp.route("/countries/<int:country_id>", methods=["GET"])
def get_country(country_id):

    countries = load()

    # Linear search through the list to find the matching record
    for country in countries:
        if country["id"] == country_id:
            return jsonify({"country": country}), 200

    # ID not found → 404 as required by Task 2
    return jsonify({"error": f"Country with id {country_id} not found"}), 404



# Task 3: POST /countries
# Creates a new country record and saves it to the JSON file.

@countries_bp.route("/countries", methods=["POST"])
def create_country():

    # request.get_json() parses the incoming JSON body into a Python dict.
    # Returns None if the Content-Type is wrong or body is not valid JSON.
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    # ── Validate all required fields (Task 3 validation requirement) ──────
    error = validate_country(data, partial=False)
    if error:
        return jsonify({"error": error}), 400

    countries = load()

    # ── Auto-generate unique ID
    # If the list is empty, start at 1; otherwise take max(existing ids) + 1.
    # This guarantees IDs are always unique and monotonically increasing.
    new_id = max((c["id"] for c in countries), default=0) + 1

    # ── Build the new record
    new_country = {
        "id":         new_id,
        "name":       data["name"].strip(),
        "population": data["population"],
        "capital":    data["capital"].strip(),
        "year":       data["year"]
    }

    countries.append(new_country)
    save(countries)   # persist to countries.json (Task 3 requirement)

    return jsonify({"message": "Country created", "country": new_country}), 201



# Task 4: PUT /countries/<id>
# Updates an existing country record (partial update allowed).

@countries_bp.route("/countries/<int:country_id>", methods=["PUT"])
def update_country(country_id):

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    # ── Validate provided fields (partial=True skips "required" checks) ───
    error = validate_country(data, partial=True)
    if error:
        return jsonify({"error": error}), 400

    countries = load()

    # Find the record to update
    for country in countries:
        if country["id"] == country_id:

            # ── Apply partial update
            # Only overwrite keys that the client actually sent.
            # .strip() removes accidental leading/trailing whitespace from strings.
            if "name" in data:
                country["name"] = data["name"].strip()
            if "population" in data:
                country["population"] = data["population"]
            if "capital" in data:
                country["capital"] = data["capital"].strip()
            if "year" in data:
                country["year"] = data["year"]

            save(countries)   # persist the updated list (Task 4 requirement)
            return jsonify({"message": "Country updated", "country": country}), 200

    # ID not found → 404 as required by Task 4
    return jsonify({"error": f"Country with id {country_id} not found"}), 404

# Task 5: DELETE /countries/<id>
# Removes a country record by ID from the JSON file.

@countries_bp.route("/countries/<int:country_id>", methods=["DELETE"])
def delete_country(country_id):

    countries = load()

    # Find the index of the record to delete
    for index, country in enumerate(countries):
        if country["id"] == country_id:
            countries.pop(index)          # remove the record from the list
            save(countries)               # persist the shorter list (Task 5)
            return jsonify({
                "message": f"Country with id {country_id} deleted successfully"
            }), 200

    # ID not found → 404 as required by Task 5
    return jsonify({"error": f"Country with id {country_id} not found"}), 404
