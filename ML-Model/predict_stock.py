import numpy as np
import pandas as pd
import joblib
import yfinance as yf
import argparse
import sys

# ----------------------
# Allowed sectors
# ----------------------
VALID_SECTORS = {
    "Tech", "Health", "Finance", "Industry", "Energy",
    "Communication", "Consumables", "Materials",
    "Services", "Real_Estate", "Utilities"
}

# ----------------------
# Argument parsing
# ----------------------
parser = argparse.ArgumentParser(description="Predict stock return")
parser.add_argument("ticker", type=str, help="Ticker symbol (e.g. AMD)")
parser.add_argument("sector", type=str, help="Sector (e.g. Tech)")

args = parser.parse_args()

ticker_name = args.ticker.upper()
ticker_type = args.sector
ticker_type = ticker_type.replace(" ", "_")

# ----------------------
# Validate sector
# ----------------------
if ticker_type not in VALID_SECTORS:
    print(f"[ERROR] Invalid sector '{ticker_type}'")
    print(f"Valid options: {', '.join(sorted(VALID_SECTORS))}")
    sys.exit(1)

# ----------------------
# Load model + metadata
# ----------------------
try:
    train_df = pd.read_csv("./data_processed.csv")
    X_columns = train_df.drop(columns=['Target_30Day']).columns
    type_columns = [col for col in X_columns if col.startswith("Type_")]

    model = joblib.load('./model.pkl')
except Exception as e:
    print(f"[FATAL] Failed to load model or data: {e}")
    sys.exit(1)

# ----------------------
# Fetch stock data
# ----------------------
try:
    ticker = yf.Ticker(ticker_name)
    df = ticker.history(period="200d")

    if df.empty:
        print(f"[ERROR] No data found for ticker '{ticker_name}'")
        sys.exit(1)

except Exception as e:
    print(f"[ERROR] Failed to fetch data for '{ticker_name}': {e}")
    sys.exit(1)

# ----------------------
# Validate data length
# ----------------------
close_prices = df['Close'].values

if len(close_prices) < 130:
    print(f"[ERROR] Not enough historical data for '{ticker_name}' (need 130+ days)")
    sys.exit(1)

# ----------------------
# Feature engineering
# ----------------------
try:
    current_index = len(close_prices) - 1

    prices_window = close_prices[current_index-100:current_index]
    current_price = close_prices[current_index]

    # Date feature
    target_date = df.index[current_index]
    day_of_year = target_date.timetuple().tm_yday
    date_cyclic = np.cos(2 * np.pi * day_of_year / 366.0)

    # Returns
    returns = np.diff(prices_window) / prices_window[:-1]
    volatility = np.std(returns)
    mean_return = np.mean(returns)

    row_dict = {
        "Date_Cyclic": date_cyclic,
        "Volatility": volatility,
        "Mean_Return": mean_return
    }

    for i in range(len(returns)):
        row_dict[f"Return{i}"] = returns[i]

    # One-hot encode sector
    chosen_type = f"Type_{ticker_type}"

    for col in type_columns:
        row_dict[col] = 1 if col == chosen_type else 0

    new_df = pd.DataFrame([row_dict])[X_columns]

except Exception as e:
    print(f"[ERROR] Feature engineering failed: {e}")
    sys.exit(1)

# ----------------------
# Prediction
# ----------------------
try:
    predicted_return = model.predict(new_df)[0]
    predicted_price = current_price * (1 + predicted_return)

    print("\n===== RESULT =====")
    print(f"Ticker: {ticker_name}")
    print(f"Sector: {ticker_type}")
    print(f"Current Price: {current_price:.2f}")
    print(f"Predicted Return (30d): {predicted_return:.4f}")
    print(f"Predicted Price (30d): {predicted_price:.2f}")

except Exception as e:
    print(f"[ERROR] Prediction failed: {e}")
    sys.exit(1)