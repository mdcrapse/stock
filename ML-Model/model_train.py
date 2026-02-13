import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

df = pd.read_csv("./data_processed.csv")

# Pick out our training and prediction data
X = df.drop(columns=['Avg'])
y = df['Avg']

# 30 / 70 train / test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train and test the model
model = xgb.XGBRegressor(
    objective='reg:squarederror', 
    n_estimators=100, 
    random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Score the model
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

# Print the scores
print(f'RMSE: {rmse:.3f}')
print(f'R2: {r2:.3f}')

param_grid = {
    'max_depth': [3, 6, 9],
    'learning_rate': [0.01, 0.1, 0.2],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0]
}

grid_search = GridSearchCV(
    estimator=model, param_grid=param_grid, cv=3, n_jobs=-1, verbose=1
)

grid_search.fit(X_train, y_train)

# Print the best parameters and best score
print("Best parameters:", grid_search.best_params_)
print(f"Best score: {grid_search.best_score_}")

# Save the model for better use later
best_model = grid_search.best_estimator_
best_model.save_model('model.json')