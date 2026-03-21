import numpy as np
import pandas as pd
import xgboost as xgb
import joblib
import yfinance as yf

# -------------------------------
# 📦 TICKERS
# -------------------------------
tickers_list = {
    "SAP": "Tech", "MSFT": "Tech", "IBM": "Tech", "NVDA": "Tech", "AAPL": "Tech",
    "VRTX": "Health", "ABT": "Health", "TAK": "Health", "ISRG": "Health", "HCA": "Health",
    "HDB": "Finance", "XXI": "Finance", "BLK": "Finance", "MS": "Finance", "V": "Finance",
    "GE": "Industry", "GEV": "Industry", "PWR": "Industry", "VRT": "Industry", "CTAS": "Industry",
    "COP": "Energy", "ENB": "Energy", "SLB": "Energy", "VLO": "Energy", "XOM": "Energy",
    "GOOGL": "Communication", "AMX": "Communication", "NFLX": "Communication", "APP": "Communication", "NTES": "Communication",
    "KHC": "Consumables", "EDU": "Consumables", "PG": "Consumables", "ADM": "Consumables", "KO": "Consumables",
    "LIN": "Materials", "NEM": "Materials", "BHP": "Materials", "MT": "Materials", "DOW": "Materials",
    "ORLY": "Services", "MCD": "Services", "CASY": "Services", "AMZN": "Services", "SGI": "Services",
    "CBRE": "Real_Estate", "NLY": "Real_Estate", "SPG": "Real_Estate", "AVB": "Real_Estate", "ARE": "Real_Estate",
    "NEE": "Utilities", "AXIA": "Utilities", "ATO": "Utilities", "AWK": "Utilities", "SRE": "Utilities"
}

# -------------------------------
# 📥 LOAD MODEL + STRUCTURE
# -------------------------------
train_df = pd.read_csv("./data_processed.csv")
X_columns = train_df.drop(columns=['Target_30Day']).columns
type_columns = [col for col in X_columns if col.startswith("Type_")]

model = joblib.load('./model.pkl')

# -------------------------------
# 📊 RESULTS STORAGE
# -------------------------------
results = []

# -------------------------------
# 🔁 LOOP THROUGH STOCKS
# -------------------------------
for ticker_name, ticker_type in tickers_list.items():
    try:
        ticker = yf.Ticker(ticker_name)
        df = ticker.history(period="200d")

        close_prices = df['Close'].values

        if len(close_prices) < 130:
            print(f"Skipping {ticker_name} (not enough data)")
            continue

        # Backtest index
        current_index = len(close_prices) - 31

        prices_window = close_prices[current_index-100:current_index]
        current_price = close_prices[current_index]
        actual_future_price = close_prices[current_index + 30]

        # Date feature
        target_date = df.index[current_index]
        day_of_year = target_date.timetuple().tm_yday
        date_cyclic = np.cos(2 * np.pi * day_of_year / 366.0)

        # Feature engineering
        returns = np.diff(prices_window) / prices_window[:-1]
        volatility = np.std(returns)
        mean_return = np.mean(returns)

        # Build row
        row_dict = {
            "Date_Cyclic": date_cyclic,
            "Volatility": volatility,
            "Mean_Return": mean_return
        }

        for i in range(len(returns)):
            row_dict[f"Return{i}"] = returns[i]

        # One-hot type
        chosen_type = f"Type_{ticker_type}"

        for col in type_columns:
            row_dict[col] = 1 if col == chosen_type else 0

        # DataFrame
        new_df = pd.DataFrame([row_dict])[X_columns]

        # Predict
        predicted_return = model.predict(new_df)[0]
        predicted_price = current_price * (1 + predicted_return)

        actual_return = (actual_future_price - current_price) / current_price
        error = abs(predicted_price - actual_future_price)

        results.append({
            "Ticker": ticker_name,
            "Type": ticker_type,
            "Actual Return": actual_return,
            "Predicted Return": predicted_return,
            "Price Error": error
        })

        print(f"{ticker_name}: Pred={predicted_return:.3f}, Actual={actual_return:.3f}, Error={error:.2f}")

    except Exception as e:
        print(f"Error with {ticker_name}: {e}")

# -------------------------------
# 📈 SUMMARY
# -------------------------------
results_df = pd.DataFrame(results)

print("\n===== SUMMARY =====")
print(f"Avg Price Error: {results_df['Price Error'].mean():.2f}")
print(f"Avg Actual Return: {results_df['Actual Return'].mean():.4f}")
print(f"Avg Predicted Return: {results_df['Predicted Return'].mean():.4f}")

# Direction accuracy
direction_correct = np.mean(
    np.sign(results_df['Actual Return']) == np.sign(results_df['Predicted Return'])
)

print(f"Direction Accuracy: {direction_correct:.2%}")