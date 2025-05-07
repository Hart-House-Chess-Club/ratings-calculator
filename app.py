from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Ensure src is in path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.ratings_service import calculate_rating

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the Visualization Tool API!'})

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {"example_key": "example_value"}
    return jsonify(data)

@app.route('/api/predict_rating', methods=['POST'])
def predict_rating():
    data = request.json
    try:
        result = calculate_rating(
            cfc_id=int(data['cfc_id']),
            n_games=int(data['n_games']),
            ratings_list=[int(r) for r in data['ratings_list']],
            wins=int(data['wins']),
            losses=int(data['losses']),
            draws=int(data['draws']),
            current_rating=int(data['current_rating']),
            all_time_high=int(data['all_time_high']),
            rating_type=int(data['rating_type']),
            quick_tourney=int(data['quick_tourney'])
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)