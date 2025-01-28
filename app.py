# 1. app.py
from flask import Flask, request, jsonify
from datetime import datetime
from supabase import create_client
import os

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