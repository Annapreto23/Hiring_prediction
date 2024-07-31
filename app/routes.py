from flask import render_template, request
from app import app
import joblib
import pandas as pd

# Load the trained model
model_filename = 'model/random_forest_model.pkl'
model = joblib.load(model_filename)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/predict', methods=['POST'])
def predict():
    print("Received data:", request.form)
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

    new_data = pd.DataFrame([data])
    prediction = model.predict(new_data)
    prediction_result = 'Hired' if prediction[0] == 1 else 'Not Hired'

    return render_template('result.html', result=prediction_result)

