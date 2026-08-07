from flask import Flask, request, jsonify
import os, json

try:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    GOOGLE_APIS_AVAILABLE = True
except ImportError:
    GOOGLE_APIS_AVAILABLE = False

app = Flask(__name__)
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)
DATA_FILE = os.path.join(DATA_DIR, 'data.json')

SHEET_ID = os.environ.get('GOOGLE_SHEET_ID', '').strip()
SHEET_RANGE = os.environ.get('GOOGLE_SHEET_RANGE', 'Sheet1!A1').strip()
SERVICE_ACCOUNT_FILE = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', os.path.join(BASE_DIR, 'credentials', 'service_account.json'))
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


def get_sheets_service():
    if not GOOGLE_APIS_AVAILABLE or not SHEET_ID:
        return None
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        return None
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('sheets', 'v4', credentials=creds, cache_discovery=False)


def load_sheet_data():
    svc = get_sheets_service()
    if not svc:
        return None
    try:
        result = svc.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=SHEET_RANGE).execute()
        values = result.get('values', [])
        if not values or not values[0]:
            return {}
        text = values[0][0]
        return json.loads(text) if text else {}
    except Exception as e:
        print('Google Sheets load error:', e)
        return None


def save_sheet_data(payload):
    svc = get_sheets_service()
    if not svc:
        return False
    body = {'values': [[json.dumps(payload, ensure_ascii=False)]]}
    try:
        svc.spreadsheets().values().update(
            spreadsheetId=SHEET_ID,
            range=SHEET_RANGE,
            valueInputOption='RAW',
            body=body
        ).execute()
        return True
    except Exception as e:
        print('Google Sheets save error:', e)
        return False


def load_local_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except Exception:
            return {}


def save_local_data(payload):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


@app.route('/data', methods=['GET'])
def get_data():
    sheet_data = load_sheet_data()
    if sheet_data is not None:
        return jsonify(sheet_data)
    return jsonify(load_local_data())


@app.route('/save', methods=['POST'])
def save_data():
    try:
        payload = request.get_json(force=True)
    except Exception:
        return jsonify({'error': 'invalid json'}), 400
    if save_sheet_data(payload):
        return jsonify({'ok': True})
    try:
        save_local_data(payload)
        return jsonify({'ok': True, 'fallback': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
