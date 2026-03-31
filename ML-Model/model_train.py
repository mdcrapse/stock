import numpy as np
import pandas as pd
import xgboost as xgb
import joblib

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error

# Load data
df = pd.read_csv("./data_processed.csv")

df = df.replace([np.inf, -np.inf], np.nan) # Convert inf to NaN
df = df.dropna(subset=['Target_30Day'])    # Drop rows where target is missing

# Features and target
X = df.drop(columns=['Target_30Day'])
y = df['Target_30Day']

# Train/test split (70/30)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Base model
model = xgb.XGBRegressor(
    objective='reg:squarederror',
    random_state=42
)

# Expanded hyperparameter grid
param_grid = {
    'max_depth': [12, 15],
    'learning_rate': [0.15],
    'n_estimators': [500],
    'subsample': [1.0],
    'colsample_bytree': [0.6, 0.7]
}

# Grid search using MAE
grid_search = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    cv=3,
    scoring='neg_mean_absolute_error',
    n_jobs=-1,
    verbose=1
)

# Fit grid search
grid_search.fit(X_train, y_train)

# Best model
best_model = grid_search.best_estimator_

# Evaluate on test set
y_pred = best_model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)

# Print results
print("\nBest parameters:", grid_search.best_params_)
print(f"Cross-validated MAE: {-grid_search.best_score_:.4f}")
print(f"Test MAE: {mae:.4f}")

# Save model
joblib.dump(best_model, "./model.pkl")
joblib.dump(best_model, "../stocks/model.pkl")