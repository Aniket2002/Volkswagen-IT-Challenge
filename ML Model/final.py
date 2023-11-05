import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load the dataset
df = pd.read_csv("station_day.csv")

# Define the columns to drop
columns_to_drop = [
    "StationId", "Date", "PM2.5", "PM10", "Toluene", "Xylene", "O3", "NH3", "AQI_Bucket", "AQI"
]

# Drop specified columns
df = df.drop(columns=columns_to_drop)

# Fill missing values with column means
df = df.fillna(df.mean())

# Create a function to analyze rows
def analyze_row(row):
    if row['CO'] < row['NOx'] < row['Benzene']:
        return 0
    elif row['CO'] > row['NOx'] < row['Benzene']:
        return 1
    elif row['CO'] < row['NOx'] > row['Benzene']:
        return 2
    elif row['CO'] > row['NOx'] > row['Benzene']:
        return 3
    else:
        return 1

# Add the "analysis" column
df['analysis'] = df.apply(analyze_row, axis=1)

# Save the preprocessed data to a CSV
df.to_csv("final_dataset.csv")

# Split the dataset into features (X) and the target variable (y)
X = df.drop('analysis', axis=1)
y = df['analysis']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create an XGBoost classifier
model = xgb.XGBClassifier(objective="multi:softmax", num_classes=4)

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model's accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Serialize and save the model
joblib.dump(model, 'model.pkl')
