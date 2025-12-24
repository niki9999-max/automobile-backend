from flask import Blueprint, jsonify
from db import get_db

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard/summary")
def dashboard_summary():
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT SUM(pending_amount) FROM customers")
    total_pending = cur.fetchone()[0] or 0

    cur.execute("SELECT COUNT(*) FROM customers WHERE pending_amount > 0")
    pending_customers = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM stock WHERE quantity <= min_quantity")
    low_stock = cur.fetchone()[0]

    cur.close()
    db.close()

    return jsonify({
        "total_pending": total_pending,
        "pending_customers": pending_customers,
        "low_stock": low_stock
    })
