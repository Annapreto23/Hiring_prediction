from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model
model_filename = 'model/random_forest_model.pkl'
model = joblib.load(model_filename)

@app.route('/')
def home():
    return "Welcome to the Hiring Prediction API!"

@app.route('/predict', methods=['POST'])
def predict():
    # Get JSON data from the request
    data = request.get_json()

    # Create DataFrame for new data
    new_data = pd.DataFrame([data])

    # Make prediction
    prediction = model.predict(new_data)

    # Return the prediction result
    return jsonify({
        'Prediction': 'Hired' if prediction[0] == 1 else 'Not Hired'
    })

if __name__ == '__main__':
    app.run(debug=True)
