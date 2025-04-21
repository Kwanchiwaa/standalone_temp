from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# เชื่อมต่อ MongoDB
client = MongoClient("mongodb+srv://<username>:<password>@cluster0.mongodb.net/test")
db = client["air_quality"]
collection = db["sensor_data"]

@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.get_json()
    data['created_at'] = datetime.utcnow()
    collection.insert_one(data)
    return jsonify({"message": "Data uploaded successfully!"})

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
