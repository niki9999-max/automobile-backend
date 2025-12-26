from flask import Flask, render_template
from flask_cors import CORS
import os

# Import Routes
from routes.customers import customers_bp
# from routes.stock import stock_bp       
# from routes.dashboard import dashboard_bp 

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(customers_bp)
# app.register_blueprint(stock_bp)        
# app.register_blueprint(dashboard_bp)    

# --- THIS CONNECTS YOUR HTML FILE ---
@app.route('/')
def home():
    return render_template('index.html')

# --- DATABASE FIXER (Required for Due Amount) ---
@app.route('/fix-db')
def fix_db():
    from db import get_db
    db = get_db()
    cur = db.cursor()
    try:
        # This adds the 'due_amount' column to your table
        cur.execute("ALTER TABLE customers ADD COLUMN due_amount DECIMAL(10,2) DEFAULT 0.00")
        db.commit()
        return "<h1>Success! Database Updated. Go back to Dashboard.</h1>"
    except Exception as e:
        return f"<h1>Database Status: {e} (If it says 'Duplicate column', it is already fixed!)</h1>"
# ------------------------------------------------

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)