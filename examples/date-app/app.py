from flask import Flask
from flask_cors import CORS

from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/date', methods=['GET'])
def get_current_date():
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return {'current_date': current_date}
