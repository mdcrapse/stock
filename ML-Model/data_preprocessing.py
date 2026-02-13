import pandas as pd
import numpy as np

df = pd.read_csv("./NIFTY_500_day.csv")
new_data = []

# Process data to include month as a sin function and day as a sin function
for _, row in df.iterrows():
    # Pick out data
    open_cost = row.open
    high_cost = row.high
    low_cost = row.low
    close_cost = row.close
    
    # Average the costs out
    avg_cost = (open_cost + high_cost + low_cost + close_cost) / 4

    # Isolate the month and day
    date = row.date.split('-')
    month_raw = float(date[1])
    day_raw = float(date[2].split()[0])

    # Turn them into cyclical sin values so the ML algorithm can understand it better
    month_normalized = month_raw / 12
    day_normalized = day_raw / 31

    # Add the values to the new data
    new_data.append([month_normalized, day_normalized, open_cost, high_cost, low_cost, close_cost, avg_cost])

# Convert the new data into a dataframe
new_df = pd.DataFrame(new_data)

new_df.to_csv("./data_processed.csv")