import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv("data.csv")
new_data = []

# Process rows into history[day - 100 : current day], 30 day out price, percent return, type
for i in range(100, len(df) - 30):
    # Get the current row
    row = df.iloc[i]
    
    # We use Cosine of the year progress so that december is next to january
    date_obj = pd.to_datetime(row.Date)
    day_of_year = date_obj.dayofyear
    cyclical_date = np.cos(2 * np.pi * day_of_year / 366.0)

    # Get the stock history and calculate percent return
    prices = df.iloc[i-100 : i]['Close'].values
    returns = np.diff(prices) / prices[:-1]
    
    future_val = df.iloc[i+30]['Close']
    current_val = row.Close
    percent_return = (future_val - current_val) / current_val
    percent_return = np.clip(percent_return, -0.5, 0.5)

    volatility = np.std(returns)
    mean_return = np.mean(returns)
    
    # Add to the new row
    new_row = [cyclical_date, volatility, mean_return] + returns.tolist() + [percent_return, row.Type]
    new_data.append(new_row)

# Create dataframe and heeaders
return_headers = [f"Return{j}" for j in range(99)]

headers = (
    ["Date_Cyclic", "Volatility", "Mean_Return"] +
    return_headers +
    ["Target_30Day", "Type"]
)

new_df = pd.DataFrame(new_data, columns=headers)

# One hot encoding for type
new_df = pd.get_dummies(new_df, columns=['Type'], prefix='Type')

# Export
new_df.to_csv("./data_processed.csv", index=False)
print(f"File saved with {len(new_df.columns)} columns and {len(new_df)} rows.")