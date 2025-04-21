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

@app.route("/dashboard")
def dashboard():
    html = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Air Quality Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
  <h1>Real-time Air Quality Dashboard</h1>

  <canvas id="temperatureChart" width="400" height="200"></canvas>
  <canvas id="humidityChart" width="400" height="200"></canvas>
  <canvas id="pm25Chart" width="400" height="200"></canvas>

  <script>
    const tempData = [];
    const humidityData = [];
    const pm25Data = [];
    const timestamps = [];

    async function fetchData() {
      const response = await fetch("https://your-render-api-url/data");
      const data = await response.json();

      // ล้างข้อมูลเก่า
      if (timestamps.length >= 30) {
        timestamps.shift();
        tempData.shift();
        humidityData.shift();
        pm25Data.shift();
      }

      // เพิ่มข้อมูลใหม่
      data.forEach(entry => {
        timestamps.push(entry.timestamp);
        tempData.push(entry.temperature);
        humidityData.push(entry.humidity);
        pm25Data.push(entry.pm25);
      });

      updateCharts();
    }

    function updateCharts() {
      temperatureChart.update();
      humidityChart.update();
      pm25Chart.update();
    }

    // สร้าง Chart.js สำหรับแสดงกราฟ
    const temperatureChart = new Chart(document.getElementById('temperatureChart'), {
      type: 'line',
      data: {
        labels: timestamps,
        datasets: [{
          label: 'Temperature (°C)',
          data: tempData,
          borderColor: 'red',
          fill: false
        }]
      }
    });

    const humidityChart = new Chart(document.getElementById('humidityChart'), {
      type: 'line',
      data: {
        labels: timestamps,
        datasets: [{
          label: 'Humidity (%)',
          data: humidityData,
          borderColor: 'blue',
          fill: false
        }]
      }
    });

    const pm25Chart = new Chart(document.getElementById('pm25Chart'), {
      type: 'line',
      data: {
        labels: timestamps,
        datasets: [{
          label: 'PM2.5 (µg/m³)',
          data: pm25Data,
          borderColor: 'green',
          fill: false
        }]
      }
    });

    // เรียกฟังก์ชัน fetchData ทุกๆ 60 วินาที
    setInterval(fetchData, 60000);
    fetchData();  // เรียกครั้งแรก
  </script>
</body>
</html>
