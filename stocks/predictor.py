import numpy as np
import pandas as pd
import joblib
import yfinance as yf
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

VALID_SECTORS = {
    "Tech", "Health", "Finance", "Industry", "Energy",
    "Communication", "Consumables", "Materials",
    "Services", "Real_Estate", "Utilities"
}

def predict_stock(ticker_name, ticker_type):
    ticker_name = ticker_name.upper()
    ticker_type = ticker_type.replace(" ", "_")

    if ticker_type not in VALID_SECTORS:
        return {"error": f"Invalid sector: {ticker_type}"}

    try:
        X_columns = [
            "Date_Cyclic", "Volatility", "Mean_Return",
            *[f"Return{i}" for i in range(99)],
            "Type_Communication", "Type_Consumables", "Type_Energy",
            "Type_Finance", "Type_Health", "Type_Industry",
            "Type_Materials", "Type_Real_Estate", "Type_Services",
            "Type_Tech", "Type_Utilities"
        ]

        type_columns = [
            "Type_Communication", "Type_Consumables", "Type_Energy",
            "Type_Finance", "Type_Health", "Type_Industry",
            "Type_Materials", "Type_Real_Estate", "Type_Services",
            "Type_Tech", "Type_Utilities"
        ]

        model = joblib.load(MODEL_PATH)
    except Exception as e:
        return {"error": f"Model load failed: {e}"}

    try:
        ticker = yf.Ticker(ticker_name)
        df = ticker.history(period="200d")

        if df.empty:
            return {"error": "No data found for ticker"}
    except Exception as e:
        return {"error": f"Data fetch failed: {e}"}

    close_prices = df['Close'].values

    if len(close_prices) < 130:
        return {"error": "Not enough data"}

    try:
        current_index = len(close_prices) - 31
        prices_window = close_prices[current_index-100:current_index]
        current_price = close_prices[current_index]

        target_date = df.index[current_index]
        day_of_year = target_date.timetuple().tm_yday
        date_cyclic = np.cos(2 * np.pi * day_of_year / 366.0)

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

        chosen_type = f"Type_{ticker_type}"

        for col in type_columns:
            row_dict[col] = 1 if col == chosen_type else 0

        new_df = pd.DataFrame([row_dict])[X_columns]

        predicted_return = model.predict(new_df)[0]
        predicted_price = current_price * (1 + predicted_return)

        return {
            "ticker": ticker_name,
            "sector": ticker_type,
            "current_price": round(float(current_price), 2),
            "predicted_return": round(float(predicted_return), 3),
            "predicted_price": round(float(predicted_price), 2)
        }

    except Exception as e:
        return {"error": f"Prediction failed: {e}"}