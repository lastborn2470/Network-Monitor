import random

import requests
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Sample mock local inventory data (unchanged)
DEVICES = [
    {"ip": "192.168.1.1", "mac": "00:1A:2B:3C:4D:5E", "hostname": "Main-Router", "status": "Registered"},
    {"ip": "192.168.1.10", "mac": "A4:C3:F0:89:12:34", "hostname": "Admin-Laptop", "status": "Registered"},
    {"ip": "192.168.1.15", "mac": "B8:27:EB:45:67:89", "hostname": "Raspberry-Pi", "status": "Registered"},
    {"ip": "192.168.1.42", "mac": "DC:A6:32:11:22:33", "hostname": "Unknown-Device", "status": "Unknown/Guest"}
]

@app.route('/')
def home():
    with open("index.html", "r") as f:
        return render_template_string(f.read())

@app.route('/api/network-details', methods=['GET'])
def network_details():
    # Fetch public network details (Public IP, ISP, Location)
    try:
        # Use ipapi.co for detailed, reliable geolocation/ISP data
        res = requests.get('https://ipapi.co/json/', timeout=5)
        res.raise_for_status()
        data = res.json()
        return jsonify({
            "ip": data.get("ip", "102.89.17.238"),  # Mock if offline
            "isp": data.get("org", "MTN Nigeria Ltd"),
            "location": f"{data.get('city', 'Lagos')}, {data.get('country_name', 'NG')}"
        })
    except (requests.RequestException, ValueError):
        # Fallback for offline testing
        return jsonify({
            "ip": "102.89.17.238",
            "isp": "Local Subnet (Offline Mode)",
            "location": "Lagos, NG"
        })

@app.route('/api/scan', methods=['GET'])
def scan_network():
    return jsonify({"status": "success", "devices": DEVICES})

@app.route('/api/speedtest', methods=['GET'])
def speed_test():
    # Simulated speed test metrics mirroring typical Nigerian connectivity
    metrics = {
        "ping_ms_unloaded": random.randint(5, 12),
        "ping_ms_loaded": random.randint(25, 40),
        "download_mbps": round(random.uniform(6.5, 9.8), 1), # Large number
        "upload_mbps": round(random.uniform(4.0, 6.2), 1), # Smaller number
        "test_server": random.choice(["Lagos, NG", "Ojota, NG", "Ikeja, NG"])
    }
    return jsonify(metrics)

if __name__ == '__main__':
    print("Starting Professional Network Monitoring System...")
    print("Server running on http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)