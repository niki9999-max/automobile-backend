from flask import Blueprint, request, jsonify
from db import get_db

stock_bp = Blueprint("stock", __name__)

@stock_bp.route("/stock", methods=["GET"])
def get_stock():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM stock")
    data = cur.fetchall()
    cur.close()
    db.close()
    return jsonify(data)

@stock_bp.route("/stock", methods=["POST"])
def add_stock():
    data = request.json
    item_name = data.get("item_name")
    quantity = data.get("quantity")
    price = data.get("price")

    if not item_name:
        return jsonify({"error": "Item Name required"}), 400

    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("INSERT INTO stock (item_name, quantity, price) VALUES (%s, %s, %s)", 
                    (item_name, quantity, price))
        db.commit()
        return jsonify({"message": "Saved"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        db.close()

# --- NEW: EDIT STOCK ---
@stock_bp.route("/stock/<int:id>", methods=["PUT"])
def update_stock(id):
    data = request.json
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("""
            UPDATE stock 
            SET item_name=%s, quantity=%s, price=%s 
            WHERE id=%s
        """, (data['item_name'], data['quantity'], data['price'], id))
        db.commit()
        return jsonify({"message": "Updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        db.close()

# --- NEW: DELETE STOCK ---
@stock_bp.route("/stock/<int:id>", methods=["DELETE"])
def delete_stock(id):
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("DELETE FROM stock WHERE id=%s", (id,))
        db.commit()
        return jsonify({"message": "Deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        db.close()