import joblib
import pandas as pd

# Load the trained model
model_filename = 'random_forest_model.pkl'
model = joblib.load(model_filename)

# Function to get user input and make a prediction
def get_user_input():
    # Collect user inputs
    age = int(input("Enter Age (20-50): "))
    gender = int(input("Enter Gender (0 for Male, 1 for Female): "))
    education_level = int(input("Enter Education Level (1: Bachelor's Type 1, 2: Bachelor's Type 2, 3: Master's, 4: PhD): "))
    experience_years = int(input("Enter Years of Experience (0-15): "))
    previous_companies = int(input("Enter Number of Previous Companies Worked (1-5): "))
    distance_from_company = float(input("Enter Distance from Company (1-50 km): "))
    interview_score = int(input("Enter Interview Score (0-100): "))
    skill_score = int(input("Enter Skill Score (0-100): "))
    personality_score = int(input("Enter Personality Score (0-100): "))
    recruitment_strategy = int(input("Enter Recruitment Strategy (1: Aggressive, 2: Moderate, 3: Conservative): "))

    # Create DataFrame for new data
    new_data = pd.DataFrame({
        'Age': [age],
        'Gender': [gender],
        'EducationLevel': [education_level],
        'ExperienceYears': [experience_years],
        'PreviousCompanies': [previous_companies],
        'DistanceFromCompany': [distance_from_company],
        'InterviewScore': [interview_score],
        'SkillScore': [skill_score],
        'PersonalityScore': [personality_score],
        'RecruitmentStrategy': [recruitment_strategy]
    })

    return new_data

def main():
    # Get new data from the user
    new_data = get_user_input()

    # Make prediction
    prediction = model.predict(new_data)
    print("Prediction for new data:", "Hired" if prediction[0] == 1 else "Not Hired")

if __name__ == "__main__":
    main()
