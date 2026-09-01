from flask import Flask, jsonify, request
import uuid
import re

app = Flask(__name__)

users = {}


@app.route("/")
def home():
    return jsonify({
        "message": "User CRUD REST API is running"
    })


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    name = data.get("name")
    email = data.get("email")
    age = data.get("age")

    if not name or not email or age is None:
        return jsonify({
            "error": "name, email and age are required"
        }), 400

    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return jsonify({
            "error": "Invalid email format"
        }), 400

    user_id = str(uuid.uuid4())

    users[user_id] = {
        "id": user_id,
        "name": name,
        "email": email,
        "age": age
    }

    return jsonify(users[user_id]), 201


@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(list(users.values())), 200


@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    return jsonify(users[user_id]), 200


@app.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    name = data.get("name")
    email = data.get("email")
    age = data.get("age")

    if not name or not email or age is None:
        return jsonify({
            "error": "name, email and age are required"
        }), 400

    users[user_id] = {
        "id": user_id,
        "name": name,
        "email": email,
        "age": age
    }

    return jsonify(users[user_id]), 200


@app.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    del users[user_id]

    return jsonify({
        "message": "User deleted successfully"
    }), 200


if __name__ == "__main__":
    app.run(debug=True)