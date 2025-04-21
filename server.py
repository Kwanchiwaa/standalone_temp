from flask import Flask, request, jsonify, render_template
import psycopg2
from datetime import datetime
import os

app = Flask(__name__)

# PostgreSQL connection
db_url = os.getenv("DATABASE_URL")
conn = psycopg2.connect(db_url)
cur = conn.cursor()

# สร้าง table ถ้ายังไม่มี
cur.execute("""
CREATE TABLE IF NOT EXISTS sensor_data (
    id SERIAL PRIMARY KEY,
    temperature FLOAT,
    humidity FLOAT,
    pm25 FLOAT,
    created_at TIMESTAMP
)
""")
conn.commit()

@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.get_json()
    created_at = datetime.utcnow()
    cur.execute("""
        INSERT INTO sensor_data (temperature, humidity, pm25, created_at)
        VALUES (%s, %s, %s, %s)
    """, (data['temperature'], data['humidity'], data['pm25'], created_at))
    conn.commit()
    return jsonify({"message": "Data uploaded successfully!"})

@app.route('/api/latest')
def latest_data():
    cur.execute("SELECT temperature, humidity, pm25 FROM sensor_data ORDER BY created_at DESC LIMIT 1")
    row = cur.fetchone()
    if row:
        return jsonify({"temperature": row[0], "humidity": row[1], "pm25": row[2]})
    else:
        return jsonify({"temperature": "--", "humidity": "--", "pm25": "--"})

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


