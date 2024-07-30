from flask import Flask, request, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model
model_filename = 'Hiring_prediction/model/random_forest_model.pkl'
model = joblib.load(model_filename)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form')
def form():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve form data
    data = {
        'Age': float(request.form['Age']),
        'Gender': int(request.form['Gender']),
        'EducationLevel': int(request.form['EducationLevel']),
        'ExperienceYears': float(request.form['ExperienceYears']),
        'PreviousCompanies': float(request.form['PreviousCompanies']),
        'DistanceFromCompany': float(request.form['DistanceFromCompany']),
        'InterviewScore': float(request.form['InterviewScore']),
        'SkillScore': float(request.form['SkillScore']),
        'PersonalityScore': float(request.form['PersonalityScore']),
        'RecruitmentStrategy': int(request.form['RecruitmentStrategy'])
    }

    # Create DataFrame for new data
    new_data = pd.DataFrame([data])

    # Make prediction
    prediction = model.predict(new_data)
    prediction_result = 'Hired' if prediction[0] == 1 else 'Not Hired'

    # Render the result in the template
    return render_template('result.html', result=prediction_result)

if __name__ == '__main__':
    app.run(debug=True)
