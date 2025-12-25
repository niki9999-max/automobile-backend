from flask import Blueprint, jsonify
from db import get_db

customers_bp = Blueprint("customers", __name__)

@customers_bp.route("/customers", methods=["GET"])
def get_customers():
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("SELECT * FROM customers")
    data = cur.fetchall()

    cur.close()
    db.close()

    return jsonify(data), 200


@customers_bp.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
    data = cur.fetchone()

    cur.close()
    db.close()

    if not data:
        return jsonify({"error": "Customer not found"}), 404

    return jsonify(data), 200


@customers_bp.route("/customers/count", methods=["GET"])
def customers_count():
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT COUNT(*) FROM customers")
    count = cur.fetchone()[0]

    cur.close()
    db.close()

    return jsonify({"count": count}), 200
from flask import request

@customers_bp.route("/customers", methods=["POST"])
def create_customer():
    data = request.json

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s)",
        (name, email, phone)
    )

    db.commit()
    cur.close()
    db.close()

    return jsonify({"message": "Customer added successfully"}), 201
