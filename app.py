from flask import Flask, render_template
from flask_cors import CORS
import os
from db import get_db # Import the database connection

from routes.customers import customers_bp
# from routes.stock import stock_bp       
# from routes.dashboard import dashboard_bp 

app = Flask(__name__)
CORS(app)

app.register_blueprint(customers_bp)

@app.route('/')
def home():
    return render_template('index.html')

# --- AUTOMATIC DATABASE FIXER ---
# This runs once when the server starts
def fix_database():
    try:
        with app.app_context():
            db = get_db()
            cur = db.cursor()
            # Try to add the column. If it exists, it will just fail silently.
            cur.execute("ALTER TABLE customers ADD COLUMN due_amount DECIMAL(10,2) DEFAULT 0.00")
            db.commit()
            print("SUCCESS: Database updated automatically!")
            cur.close()
            db.close()
    except Exception as e:
        print(f"Database check: {e}")

# Run the fix immediately
fix_database()
# --------------------------------

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)