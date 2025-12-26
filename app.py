from flask import Flask, render_template
from flask_cors import CORS
import os
from db import get_db

# Import Routes
from routes.customers import customers_bp
from routes.stock import stock_bp  # <-- NEW: Imported Stock

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(customers_bp)
app.register_blueprint(stock_bp)   # <-- NEW: Registered Stock

@app.route('/')
def home():
    return render_template('index.html')

# --- AUTOMATIC DATABASE SETUP ---
def setup_database():
    try:
        with app.app_context():
            db = get_db()
            cur = db.cursor()
            
            # 1. Create Customers Table (if not exists)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    email VARCHAR(255),
                    phone VARCHAR(20),
                    due_amount DECIMAL(10,2) DEFAULT 0.00
                )
            """)
            
            # 2. Create Stock Table (if not exists)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS stock (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    item_name VARCHAR(255),
                    quantity INT,
                    price DECIMAL(10,2)
                )
            """)
            
            db.commit()
            print("SUCCESS: Database tables checked/created!")
            cur.close()
            db.close()
    except Exception as e:
        print(f"Database setup error: {e}")

# Run setup immediately
setup_database()
# --------------------------------

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)