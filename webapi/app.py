# webapi/app.py
from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

@app.route("/")
def index():
    conn = psycopg2.connect(
        dbname="azizik89db",
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"],
        host="db-service",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify({
        "database": "azizik89db",
        "tables": tables
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

