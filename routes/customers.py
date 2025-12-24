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

    return jsonify(data)
@customers_bp.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
    data = cur.fetchone()

    cur.close()
    db.close()

    return jsonify(data)
@customers_bp.route("/customers/count", methods=["GET"])
def customers_count():
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT COUNT(*) FROM customers")
    count = cur.fetchone()[0]

    cur.close()
    db.close()

    return jsonify({"count": count})
