from flask import Flask, jsonify
from routes import countries_bp

app = Flask(__name__)

app.register_blueprint(countries_bp)

@app.route("/", methods=["GET"])
def welcome():

    return jsonify({
        "message": "Countries API",
        "version": "1.0",
        "author":  "Karakat",
        "group":   "SE-2507",
        "student_id": 45
    }), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)