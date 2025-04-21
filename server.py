from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient, ASCENDING
from datetime import datetime
import os

app = Flask(__name__)

# MongoDB connection
mongo_url = "mongodb+srv://..."
client = MongoClient(mongo_url)
db = client["air_quality"]
collection = db["sensor_data"]

# TTL index
if "created_at_1" not in collection.index_information():
    collection.create_index([("created_at", ASCENDING)], expireAfterSeconds=2592000)

@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.get_json()
    data['created_at'] = datetime.utcnow()
    collection.insert_one(data)
    return jsonify({"message": "Data uploaded successfully!"})

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

# ✅ เพิ่มตรงนี้
@app.route('/api/latest')
def latest_data():
    latest = collection.find_one(sort=[("created_at", -1)])
    if latest:
        return jsonify({
            "temperature": latest.get("temperature", "--"),
            "humidity": latest.get("humidity", "--"),
            "pm25": latest.get("pm25", "--")
        })
    else:
        return jsonify({"temperature": "--", "humidity": "--", "pm25": "--"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


