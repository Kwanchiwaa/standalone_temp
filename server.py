from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# เชื่อมต่อ MongoDB
# แทนที่ <username> และ <password> ด้วยข้อมูลจริง
client = MongoClient("mongodb+srv://s6501023611010:<password>@kwanchiwa.pkf77cz.mongodb.net/?retryWrites=true&w=majority&appName=Kwanchiwa")
db = client["air_quality"]
collection = db["sensor_data"]

@app.route('/upload', methods=['POST'])
def upload_data():
    # รับข้อมูลจากผู้ใช้ในรูปแบบ JSON
    data = request.get_json()

    # เพิ่ม timestamp เป็น datetime object
    data['created_at'] = datetime.utcnow()

    # บันทึกข้อมูลลง MongoDB
    collection.insert_one(data)

    return jsonify({"message": "Data uploaded successfully!"})

@app.route('/dashboard')
def dashboard():
    # ดึงข้อมูลจาก MongoDB
    data = list(collection.find().sort('created_at', -1).limit(10))  # รับ 10 ข้อมูลล่าสุด

    # เปลี่ยน ObjectId ของ MongoDB เป็น string
    for entry in data:
        entry['_id'] = str(entry['_id'])

    return render_template("dashboard.html", data=data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

