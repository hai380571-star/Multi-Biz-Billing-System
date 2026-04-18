import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- Multi-Company Data (Initial Master) ---
# Yahan companies ka data save hoga. Prefix aur Counter invoice number manage karte hain.
companies = {
    "1": {
        "name": "Abdu's Biryani Point", 
        "addr": "Murshidabad", 
        "prefix": "ABP", 
        "counter": 101
    },
    "2": {
        "name": "Royal Palace Hotel", 
        "addr": "Pakur Border", 
        "prefix": "RPH", 
        "counter": 501
    }
}

# Current Active Business ID
active_id = "1"

@app.route('/')
def home():
    # Active company ki details nikalna
    co = companies[active_id]
    # Bill number format karna (e.g., ABP-101)
    bill_no = f"{co['prefix']}-{co['counter']}"
    return render_template('index.html', co=co, all_cos=companies, bill_no=bill_no, active_id=active_id)

@app.route('/switch', methods=['POST'])
def switch():
    global active_id
    active_id = request.json.get('id')
    return jsonify({"success": True})

@app.route('/create-company', methods=['POST'])
def create_co():
    data = request.json
    # Naya unique ID generate karna
    new_id = str(len(companies) + 1)
    companies[new_id] = {
        "name": data['name'],
        "addr": data['addr'],
        "prefix": data['prefix'].upper(),
        "counter": int(data['start'])
    }
    return jsonify({"success": True})

@app.route('/bill-done', methods=['POST'])
def bill_done():
    # Bill print hone ke baad counter badhana (Audit Logic)
    companies[active_id]['counter'] += 1
    new_no = f"{companies[active_id]['prefix']}-{companies[active_id]['counter']}"
    return jsonify({"new_no": new_no})

if __name__ == "__main__":
    # Render ke liye port configuration
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
