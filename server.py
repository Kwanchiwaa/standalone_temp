from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient, ASCENDING
from datetime import datetime
import os

app = Flask(__name__)

# MongoDB connection
mongo_url = "mongodb+srv://s6501023611010:0949797333@kwanchiwa.pkf77cz.mongodb.net/?retryWrites=true&w=majority&appName=Kwanchiwa"
client = MongoClient(mongo_url)
db = client["air_quality"]
collection = db["sensor_data"]

# สร้าง TTL index ถ้ายังไม่มี (ลบข้อมูลเมื่อเกิน 30 วัน)
if "created_at_1" not in collection.index_information():
    collection.create_index([("created_at", ASCENDING)], expireAfterSeconds=2592000)  # 30 วัน = 2592000 วิ

@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.get_json()
    data['created_at'] = datetime.utcnow()  # ใส่เวลา
    collection.insert_one(data)
    return jsonify({"message": "Data uploaded successfully!"})

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

