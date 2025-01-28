from flask import Flask, render_template, jsonify
import metrics_collector
import requests

app = Flask(__name__)

# Endpoint to fetch live data
@app.route('/api/live-data')
def live_data():
    pc_metrics = metrics_collector.get_pc_metrics()
    third_party_metrics = metrics_collector.get_third_party_metrics()
    return jsonify({"pc_metrics": pc_metrics, "third_party_metrics": third_party_metrics})

# Dashboard UI
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
