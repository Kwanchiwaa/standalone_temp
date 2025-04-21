from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# เชื่อมต่อ MongoDB
client = MongoClient("mongodb+srv://<username>:<password>@cluster0.mongodb.net/test")
db = client["air_quality"]
collection = db["sensor_data"]

@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.get_json()

    # เพิ่ม timestamp เป็น datetime object
    data['created_at'] = datetime.utcnow()

    # บันทึกลง MongoDB
    collection.insert_one(data)

    return jsonify({"message": "Data uploaded successfully!"})

if __name__ == '__main__':
    app.run(debug=True)

