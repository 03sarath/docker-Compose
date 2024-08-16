from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Define the URL for the Flask API (ML model container)
ML_MODEL_URL = "http://ml-model:9696/predict"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Check if the request contains JSON data
        if request.is_json:
            candidate = request.get_json()
        else:
            return jsonify({"error": "Request must be JSON"}), 400

        # Make the API call with the candidate data
        response = requests.post(url=ML_MODEL_URL, json=candidate)

        if response.status_code == 200:
            result = response.json()
            return jsonify(result)
        else:
            return jsonify({"error": f'Error in prediction, status code: {response.status_code}'}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
