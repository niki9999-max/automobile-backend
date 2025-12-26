from flask import Flask, render_template
from flask_cors import CORS
import os

# Import Routes
from routes.customers import customers_bp
# from routes.stock import stock_bp       <-- Commented out for safety
# from routes.dashboard import dashboard_bp <-- Commented out for safety

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(customers_bp)
# app.register_blueprint(stock_bp)        <-- Commented out for safety
# app.register_blueprint(dashboard_bp)    <-- Commented out for safety

# --- THIS CONNECTS YOUR HTML FILE ---
@app.route('/')
def home():
    return render_template('index.html')
# ------------------------------------

if __name__ == '__main__':
    # Required for Railway
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)