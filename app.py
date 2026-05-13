
from flask import Flask, jsonify
from routes import countries_bp  # Import the blueprint that holds all /countries routes

# ── Flask App Initialization (Task 1)
app = Flask(__name__)

# Register the blueprint under the root prefix.
# All country endpoints defined in routes.py will be accessible via /countries
app.register_blueprint(countries_bp)


# ── Welcome Route (Task 1)
@app.route("/", methods=["GET"])
def welcome():

    return jsonify({
        "message": "Countries API",
        "version": "1.0",
        "author":  "Karakat",
        "group":   "SE-2507",
        "student_id": 45
    }), 200


# ── Run the Development Server (Task 1)
if __name__ == "__main__":
    # debug=True  → auto-reloads on code changes; turn off in production
    # host="0.0.0.0" → makes the server reachable from other machines / internet
    # port=5000   → default Flask port
    app.run(debug=True, host="0.0.0.0", port=5001)