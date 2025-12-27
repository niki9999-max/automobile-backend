from flask import Blueprint, request, jsonify
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

@customers_bp.route("/customers", methods=["POST"])
def add_customer():
    data = request.json
    name = data.get("name")
    phone = data.get("phone")
    due_amount = data.get("due_amount", 0)

    if not name or not phone:
        return jsonify({"error": "Name and Phone required"}), 400

    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("INSERT INTO customers (name, email, phone, due_amount) VALUES (%s, %s, %s, %s)", 
                    (name, "no-email", phone, due_amount))
        db.commit()
        return jsonify({"message": "Saved"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        db.close()

# --- NEW: EDIT CUSTOMER ---
@customers_bp.route("/customers/<int:id>", methods=["PUT"])
def update_customer(id):
    data = request.json
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("""
            UPDATE customers 
            SET name=%s, phone=%s, due_amount=%s 
            WHERE id=%s
        """, (data['name'], data['phone'], data['due_amount'], id))
        db.commit()
        return jsonify({"message": "Updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        db.close()

# --- NEW: DELETE CUSTOMER ---
@customers_bp.route("/customers/<int:id>", methods=["DELETE"])
def delete_customer(id):
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("DELETE FROM customers WHERE id=%s", (id,))
        db.commit()
        return jsonify({"message": "Deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        db.close()