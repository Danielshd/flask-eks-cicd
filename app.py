"""Small Flask service used to demo a CI/CD pipeline: Docker -> Trivy -> Helm -> AWS EKS."""

import os

import mysql.connector
from flask import Flask, jsonify

app = Flask(__name__)


def get_db_connection():
    """Open a MySQL connection from environment variables (no credentials in code)."""
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        user=os.getenv("DB_USER", "app"),
        password=os.environ["DB_PASSWORD"],
        database=os.getenv("DB_NAME", "app"),
    )


@app.route("/")
def home():
    return "Flask app running on Kubernetes!"


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/users")
def users():
    if not os.getenv("DB_HOST"):
        return jsonify(error="database not configured"), 503
    db = get_db_connection()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT id, name FROM users;")
        return jsonify([{"id": row[0], "name": row[1]} for row in cursor.fetchall()])
    finally:
        db.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
