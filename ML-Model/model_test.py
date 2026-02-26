import numpy as np
import pandas as pd
import xgboost as xgb
import joblib
from datetime import date, datetime, timedelta
import yfinance as yf

# Get historical stock data
today = date.today()
hundred_days_ago = today - timedelta(days=100)

ticker = yf.Ticker('ADTB')
df = ticker.history(period="100d")

# Get the average price
df['avg_cost'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4

# Variables to store normalization values
unnormalized_averages = []
normalization_min = 9999999999
normalization_max = 0

# Find normalization values, append all averages to an array for normalization
for _,row in df.iterrows():
    if(row['avg_cost'] > normalization_max):
        normalization_max = row['avg_cost']

    if(row['avg_cost'] < normalization_min):
        normalization_min = row['avg_cost']

    unnormalized_averages.append(row['avg_cost'])

# Turn month and day into cyclical values for better context processing
month_raw = int(str(today).split('-')[1])
day_raw = int(str(today).split('-')[2])

month_normalized = month_raw / 12
day_normalized = day_raw / 31

# Build the row starting with day and month, then 100 days of normalized averages
new_row = []
new_row.append(month_normalized)
new_row.append(day_normalized)

for avg in unnormalized_averages:
    normalized_avg = (avg - normalization_min) / (normalization_max - normalization_min)
    new_row.append(normalized_avg)

new_data = [new_row]

# Convert the new data into a dataframe
new_df = pd.DataFrame(new_data)
new_df.dropna(inplace=True)

# Load the model
loaded_model = xgb.XGBRegressor()
loaded_model = joblib.load('./model.pk1')

# Make predictions and score
predictions = loaded_model.predict(new_df)

print(predictions)