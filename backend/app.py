from flask import Flask, render_template_string, jsonify
from flask_cors import CORS
import os
from config import config
from database import init_db
from routes import register_blueprints

app = Flask(__name__)

config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

CORS(app)

init_db()

register_blueprints(app)

@app.route('/api/health')
def health():
    return {"status": "ok", "message": "SRMSS Backend Running"}

@app.route('/')
def root():
    return {
        "name": "SRMSS - Smart Road Transport Depot System",
        "version": "1.0.0",
        "status": "Backend API",
        "endpoints": "/api/*"
    }

if __name__ == '__main__':
    app.run(debug=True, port=5000)