from flask import Blueprint, jsonify
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
