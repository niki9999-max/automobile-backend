from flask import Blueprint, request, jsonify
from db import get_db

stock_bp = Blueprint("stock", __name__)

# Get all stock items
@stock_bp.route("/stock", methods=["GET"])
def get_stock():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM stock")
    data = cur.fetchall()
    cur.close()
    db.close()
    return jsonify(data)

# Add new stock item
@stock_bp.route("/stock", methods=["POST"])
def add_stock():
    data = request.json
    item_name = data.get("item_name")
    quantity = data.get("quantity")
    price = data.get("price")

    if not item_name:
        return jsonify({"error": "Item Name is required"}), 400

    db = get_db()
    cur = db.cursor()
    try:
        cur.execute(
            "INSERT INTO stock (item_name, quantity, price) VALUES (%s, %s, %s)",
            (item_name, quantity, price)
        )
        db.commit()
        return jsonify({"message": "Stock added!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        db.close()