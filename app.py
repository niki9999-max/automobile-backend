from flask import Flask
from flask_cors import CORS
from routes.customers import customers_bp
from routes.stock import stock_bp
from routes.dashboard import dashboard_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(customers_bp)
app.register_blueprint(stock_bp)
app.register_blueprint(dashboard_bp)

@app.route("/")
def home():
    return {"status": "Automobile backend running"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
