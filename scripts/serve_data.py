#!/usr/bin/env python3
"""
Simple HTTP server to serve deployment data
This can be used to host the JSON data locally if needed.
"""

from flask import Flask, jsonify, send_file
from flask_cors import CORS
import json
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

DATA_FILE = Path('data/deployments.json')

@app.route('/api/deployments')
def get_deployments():
    """Serve deployment data as JSON API."""
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        return jsonify(data), 200
    except FileNotFoundError:
        return jsonify({"error": "Deployments file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON in deployments file"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/deployments.json')
def get_deployments_file():
    """Serve raw JSON file."""
    try:
        return send_file(DATA_FILE, mimetype='application/json')
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Deployment Data API"
    }), 200

@app.route('/')
def index():
    """Root endpoint with API information."""
    return jsonify({
        "service": "Deployment Data API",
        "endpoints": {
            "/api/deployments": "Get deployments as JSON",
            "/deployments.json": "Get raw JSON file",
            "/health": "Health check"
        }
    }), 200

if __name__ == '__main__':
    print("=" * 60)
    print("Starting Deployment Data Server")
    print("=" * 60)
    print(f"Data file: {DATA_FILE.absolute()}")
    print("Server: http://0.0.0.0:8080")
    print("Endpoints:")
    print("  - http://localhost:8080/api/deployments")
    print("  - http://localhost:8080/deployments.json")
    print("  - http://localhost:8080/health")
    print("=" * 60)
    
    # Run on all interfaces, port 8080
    app.run(host='0.0.0.0', port=8080, debug=False)
