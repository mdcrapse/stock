import numpy as np
import pandas as pd
import xgboost as xgb
import joblib
from sklearn.metrics import mean_squared_error, r2_score

# Pick out our training and prediction data
df = pd.read_csv("./data_processed.csv")
X = df.drop(columns=['30Day'])
y = df['30Day']

# Load the model
loaded_model = xgb.XGBRegressor()
loaded_model = joblib.load('./model.pk1')

# Make predictions and score
predictions = loaded_model.predict(X)
rmse = np.sqrt(mean_squared_error(y, predictions))
r2 = r2_score(y, predictions)

# Print results
print(f'RMSE: {rmse:.3f}')
print(f'R²: {r2:.3f}')