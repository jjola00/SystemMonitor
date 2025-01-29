# 1. app.py
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from datetime import datetime
from supabase import create_client
import os

load_dotenv() # Load environment variables from .env file

app = Flask(__name__)

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

supabase = create_client(supabase_url, supabase_key)

def save_metrics(data):
    response = supabase.table("metrics").insert(data).execute()
    return response

def get_metrics_history():
    response = supabase.table("metrics").select("*").execute()
    return response.data

# Route to test inserting metrics and retrieving history
@app.route('/test', methods=['GET'])
def test_metrics():
    # Test data for metrics
    test_data = [
        {"device_name": "Device_1", "metric_name": "CPU Usage", "value": 25.6, "timestamp": datetime.now().isoformat()},
        {"device_name": "Device_1", "metric_name": "RAM Usage", "value": 45.3, "timestamp": datetime.now().isoformat()},
        {"device_name": "Device_2", "metric_name": "CPU Usage", "value": 72.1, "timestamp": datetime.now().isoformat()},
    ]

    # Insert test data into Supabase
    for data in test_data:
        save_metrics(data)

    # Fetch and return all metric history
    history = get_metrics_history()
    print("Metrics History:", history)  # Print history to terminal for debugging
    return jsonify({"message": "Test metrics inserted successfully", "history": history})

@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.json
    device_name = data.get('device_name')
    metrics = data.get('metrics')

    # Save metrics to the database
    for metric, value in metrics.items():
        metric_data = {
            "device_name": device_name,
            "metric_name": metric,
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        save_metrics(metric_data)

    return jsonify({"message": "Data saved to database"}), 200

@app.route('/history', methods=['GET'])
def get_history():
    history = get_metrics_history()
    return jsonify(history), 200

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)