import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pickle

# Load earthquake data
earthquake_data = pd.read_csv('newseismodata.csv')

# Split data into training and testing sets
X = earthquake_data[['Lat', 'Long']]
y = earthquake_data['Magnitude']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# Train random forest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Evaluate model performance
y_pred = rf_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
#print('Mean squared error:', mse)
#print('R-squared:', r2)

#random forest
# Predict the magnitude of a new earthquake

# new_earthquake = [[35.6895, 139.6917,10]]   // make sure the number of inputs are same as parameters defined i.e. "depth"
# predicted_magnitude = rf_model.predict(new_earthquake)
# print("Predicted Magnitude:", predicted_magnitude)

# Save model as a pickle file
with open('rf_model.pkl', 'wb') as f:
    pickle.dump(rf_model, f)
