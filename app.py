from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the Visualization Tool API!'})

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {"example_key": "example_value"}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)