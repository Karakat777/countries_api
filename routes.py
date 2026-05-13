from flask import Blueprint, jsonify, request
from storage import load, save
from validation import validate_country

countries_bp = Blueprint("countries", __name__)

@countries_bp.route("/countries", methods=["GET"])
def get_all_countries():

    countries = load()

    capital_filter = request.args.get("capital")
    min_pop_filter = request.args.get("min_pop")

    if capital_filter:
        countries = [
            c for c in countries
            if c["capital"].lower() == capital_filter.lower()
        ]

    if min_pop_filter:
        try:
            min_pop = int(min_pop_filter)
        except ValueError:
            return jsonify({"error": "min_pop must be an integer"}), 400
        countries = [c for c in countries if c["population"] >= min_pop]

    return jsonify({"countries": countries}), 200


@countries_bp.route("/countries/<int:country_id>", methods=["GET"])
def get_country(country_id):

    countries = load()

    for country in countries:
        if country["id"] == country_id:
            return jsonify({"country": country}), 200

    return jsonify({"error": f"Country with id {country_id} not found"}), 404


@countries_bp.route("/countries", methods=["POST"])
def create_country():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    error = validate_country(data, partial=False)
    if error:
        return jsonify({"error": error}), 400

    countries = load()

    new_id = max((c["id"] for c in countries), default=0) + 1

    new_country = {
        "id":         new_id,
        "name":       data["name"].strip(),
        "population": data["population"],
        "capital":    data["capital"].strip(),
        "year":       data["year"]
    }

    countries.append(new_country)
    save(countries)

    return jsonify({"message": "Country created", "country": new_country}), 201


@countries_bp.route("/countries/<int:country_id>", methods=["PUT"])
def update_country(country_id):

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    error = validate_country(data, partial=True)
    if error:
        return jsonify({"error": error}), 400

    countries = load()

    for country in countries:
        if country["id"] == country_id:

            if "name" in data:
                country["name"] = data["name"].strip()
            if "population" in data:
                country["population"] = data["population"]
            if "capital" in data:
                country["capital"] = data["capital"].strip()
            if "year" in data:
                country["year"] = data["year"]

            save(countries)
            return jsonify({"message": "Country updated", "country": country}), 200

    return jsonify({"error": f"Country with id {country_id} not found"}), 404


@countries_bp.route("/countries/<int:country_id>", methods=["DELETE"])
def delete_country(country_id):

    countries = load()

    for index, country in enumerate(countries):
        if country["id"] == country_id:
            countries.pop(index)
            save(countries)
            return jsonify({
                "message": f"Country with id {country_id} deleted successfully"
            }), 200

    return jsonify({"error": f"Country with id {country_id} not found"}), 404
