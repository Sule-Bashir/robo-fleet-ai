from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import random
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Simple Vultr info
VULTR_IP = "45.63.4.225"

# Robots data
robots = [
    {"id": 1, "name": "Alpha-Bot", "status": "idle", "battery": 100, "location": "Zone-A", "task": "Ready", "type": "Picker", "speed": "2.5 m/s"},
    {"id": 2, "name": "Beta-Bot", "status": "working", "battery": 75, "location": "Zone-B", "task": "Moving items", "type": "Mover", "speed": "3.0 m/s"},
    {"id": 3, "name": "Gamma-Bot", "status": "charging", "battery": 25, "location": "Charging", "task": "Charging", "type": "Loader", "speed": "1.8 m/s"},
    {"id": 4, "name": "Delta-Bot", "status": "maintenance", "battery": 90, "location": "Workshop", "task": "Calibration", "type": "Inspector", "speed": "1.5 m/s"}
]

simulation = {"running": False, "items": 2450, "energy": 5.2}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/robots')
def get_robots():
    for r in robots:
        if r["status"] == "working":
            r["battery"] = max(5, r["battery"] - random.randint(0, 3))
        elif r["status"] == "charging":
            r["battery"] = min(100, r["battery"] + random.randint(5, 20))

        if r["battery"] < 20 and r["status"] != "charging":
            r["status"] = "maintenance"
            r["task"] = "Low battery"

    return jsonify(robots)

# ADD THIS ENDPOINT FOR MAP
@app.route('/api/warehouse/map')
def get_warehouse_map():
    grid = []
    for row in range(10):
        row_cells = []
        for col in range(10):
            cell_type = random.choice(['shelf', 'aisle', 'charging', 'empty'])
            item_count = random.randint(0, 10) if cell_type == 'shelf' else 0
            has_robot = random.random() < 0.1  # 10% chance

            row_cells.append({
                "id": f"{chr(65+row)}{col+1}",
                "type": cell_type,
                "items": item_count,
                "robot": has_robot,
                "vultr_coordinated": True
            })
        grid.append(row_cells)

    return jsonify({
        "grid": grid,
        "vultr_backend": VULTR_IP,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/vultr')
def vultr_info():
    return jsonify({
        "backend": "Vultr Cloud",
        "ip": VULTR_IP,
        "port": 5000,
        "status": "Production Ready",
        "hackathon": "Compliant"
    })

@app.route('/api/test')
def test():
    return jsonify({
        "message": "RoboFleet AI - Vultr Backend",
        "vultr": VULTR_IP,
        "time": datetime.now().isoformat()
    })

# ADD AI COMMAND ENDPOINT
@app.route('/api/ai/command', methods=['POST'])
def ai_command():
    data = request.json
    command = data.get('command', '').strip()

    if 'battery' in command.lower():
        response = "🔋 **AI Battery Report:** All robots operational via Vultr."
    elif 'optimize' in command.lower():
        response = "🔄 **AI Route Optimization:** Routes optimized via Vultr."
    elif 'emergency' in command.lower():
        response = "🚨 **EMERGENCY STOP:** All robots halted via Vultr."
    else:
        response = "🤖 **AI Processing:** Command analyzed on Vultr backend."

    return jsonify({
        "success": True,
        "response": response,
        "vultr_processed": True
    })

if __name__ == '__main__':
    print("🤖 RoboFleet AI Starting...")
    app.run(host='0.0.0.0', port=5000)
