from flask import Flask, request, jsonify
import os, json

app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

DATA_FILE = os.path.join(DATA_DIR, 'data.json')

@app.route('/data', methods=['GET'])
def get_data():
    if not os.path.exists(DATA_FILE):
        return jsonify({})
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            return jsonify(data)
        except Exception:
            return jsonify({})

@app.route('/save', methods=['POST'])
def save_data():
    try:
        payload = request.get_json(force=True)
    except Exception:
        return jsonify({'error': 'invalid json'}), 400
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
