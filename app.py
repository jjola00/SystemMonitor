# 1. app.py
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from datetime import datetime, timedelta
from supabase import create_client
from flask_cors import CORS
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

supabase = create_client(supabase_url, supabase_key)

def save_metrics(data):
    response = supabase.table("metrics").insert(data).execute()
    return response

def get_metrics_history(start_date=None, end_date=None):
    query = supabase.table("metrics").select("*")
    
    if start_date:
        query = query.gte("timestamp", start_date)
    if end_date:
        query = query.lte("timestamp", end_date)
    
    response = query.execute()
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
    try:
        # Get query parameters for date filtering
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Fetch history with optional date filters
        history = get_metrics_history(start_date, end_date)
        
        # Return the history along with the data sent to the database
        return jsonify({"history": history, "message": "Data retrieved successfully"}), 200
    except Exception as e:
        print(f"Error in /history endpoint: {e}")  # Log the error
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True)