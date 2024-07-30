import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib




# MySQL connection configuration
mysql_config = {
    'user': 'root',
    'password': 'philo',
    'host': 'localhost'
}
db_name = 'recruitment'

# Create a database connection engine
engine = create_engine(f"mysql+mysqlconnector://{mysql_config['user']}:{mysql_config['password']}@{mysql_config['host']}/{db_name}", echo=False)

# Read data from the database
query = "SELECT * FROM hiring_decisions;"
df = pd.read_sql(query, con=engine)

print(df.head())  # Display the first few rows for verification

# Data preprocessing
# Drop the 'id' column as it is not useful for modeling
df.drop(columns=['id'], inplace=True)

# Convert categorical variables to numeric
label_encoders = {}
for column in df.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

# Separate features and target variable
X = df.drop(columns=['HiringDecision'])
y = df['HiringDecision']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest model
rf = RandomForestClassifier(random_state=42)

# Set up the parameter grid to search for the best number of trees
param_grid = {
    'n_estimators': [10, 20, 30, 40, 50, 100, 200] 
}

# Perform grid search with cross-validation
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, scoring='accuracy', n_jobs=-1, verbose=1)
grid_search.fit(X_train, y_train)

# Get the best parameters and model
best_n_estimators = grid_search.best_params_['n_estimators']
best_rf = grid_search.best_estimator_

print(f"Best number of trees: {best_n_estimators}")

# Make predictions on the test set with the best model
y_pred = best_rf.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))


# Save the trained model
model_filename = 'random_forest_model.pkl'
joblib.dump(best_rf, model_filename)
print(f"Model saved to {model_filename}")
