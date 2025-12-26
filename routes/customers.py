from flask import Blueprint, request, jsonify
from db import get_db

customers_bp = Blueprint("customers", __name__)

@customers_bp.route("/customers", methods=["GET"])
def get_customers():
    db = get_db()
    cur = db.cursor(dictionary=True)
    
    # We now select due_amount as well
    cur.execute("SELECT id, name, email, phone, due_amount FROM customers")
    data = cur.fetchall()
    
    cur.close()
    db.close()
    return jsonify(data)

@customers_bp.route("/customers", methods=["POST"])
def add_customer():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    due_amount = data.get("due_amount", 0) # Default to 0 if empty

    if not name or not phone:
        return jsonify({"error": "Name and Phone are required"}), 400

    db = get_db()
    cur = db.cursor()

    try:
        cur.execute(
            "INSERT INTO customers (name, email, phone, due_amount) VALUES (%s, %s, %s, %s)",
            (name, email, phone, due_amount)
        )
        db.commit()
        return jsonify({"message": "Customer added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        db.close()