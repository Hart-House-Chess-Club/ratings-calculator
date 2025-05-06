from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the Visualization Tool API!'})

@app.route('/api/data', methods=['GET'])
def get_data():
    # This is where you'd integrate with your tool
    data = {"example_key": "example_value"}  # Replace with actual data
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)