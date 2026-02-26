import pandas as pd
import numpy as np
import yfinance as yf

stock_list= ["AAPL", "GOOG", "MSFT", "AMZN"]

ticker = yf.Ticker('ADTB')
df = ticker.history(period="100d")

new_data = []

# Get the average price
df['avg_cost'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    

for _,row in df.iterrows():
    # Isolate the month and day
    date = row.date.split('-')
    month_raw = float(date[1])
    day_raw = float(date[2].split()[0])

    # Turn them into cyclical sin values so the ML algorithm can understand it better
    month_normalized = month_raw / 12
    day_normalized = day_raw / 31

    new_row = []
    new_row.append(month_normalized)
    new_row.append(day_normalized)

    normalization_min = 9999999999
    normalization_max = 0

    unnormalized_averages = []

    # Get the data for the last 100 days
    for x in range(100):
        inverse_x = 100 - x
        iloc_minus_x = df.index.get_loc(row.name) - inverse_x

        # Break for bounds
        if(iloc_minus_x < 0):
            break

        cur_avg = df.iloc[iloc_minus_x].avg_cost

        if(cur_avg < normalization_min):
            normalization_min = cur_avg

        if(cur_avg > normalization_max):
            normalization_max = cur_avg

        unnormalized_averages.append(cur_avg)

    # Calculate the normalization of the unnormalized averages and add them to new row
    for avg in unnormalized_averages:
        normalized_avg = (avg - normalization_min) / (normalization_max - normalization_min)
        new_row.append(normalized_avg)

    # Get the data 30 days into the future
    iloc_plus_thirty = df.index.get_loc(row.name) + 30

    # Break for bounds
    if(iloc_plus_thirty >= len(df) - 1):
        break

    # Normalize the thirty day look ahead
    raw_thirty_day = df.iloc[iloc_plus_thirty].avg_cost
    normalized_thirty_day = (raw_thirty_day - normalization_min) / (normalization_max - normalization_min)
    new_row.append(normalized_thirty_day)

    # Add the values to the new data
    new_data.append(new_row)


# Convert the new data into a dataframe
new_df = pd.DataFrame(new_data)
new_df.dropna(inplace=True)

headers = []
for column in new_df:
    match column:
        case 0:
            headers.append("Month")
        case 1:
            headers.append("Day")
        case 102:
            headers.append("30Day")
        case _:
            headers.append("Hist" + str(column - 1))

new_df.to_csv("./data_processed.csv", index=False, header=headers)