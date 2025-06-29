# Install required libraries
!pip install yfinance scikit-learn pandas numpy matplotlib tensorflow

# Import libraries
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# Function to fetch historical stock data
def fetch_historical_data(ticker, start_date="2010-01-01", end_date="2023-12-31"):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# Function to preprocess data for LSTM
def preprocess_data(data, sequence_length=60):
    # Extract closing prices
    close_prices = data[['Close']].values

    # Normalize data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(close_prices)

    # Create sequences for LSTM
    X, y = [], []
    for i in range(sequence_length, len(scaled_data)):
        X.append(scaled_data[i-sequence_length:i, 0])
        y.append(scaled_data[i, 0])
    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))  # Reshape for LSTM input

    return X, y, scaler

# Function to build LSTM model
def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Function to detect anomalies using Isolation Forest
def detect_anomalies(data):
    model = IsolationForest(contamination=0.05)
    anomalies = model.fit_predict(data[['Close']])
    data['Anomaly'] = anomalies
    return data

# Function to analyze correlations
def analyze_correlations(data):
    correlation_matrix = data[['Open', 'High', 'Low', 'Close', 'Volume']].corr()
    return correlation_matrix

# Function to forecast future prices
def forecast_future(model, data, scaler, sequence_length=60, future_days=30):
    last_sequence = data[-sequence_length:]
    last_sequence_scaled = scaler.transform(last_sequence)

    future_predictions = []
    for _ in range(future_days):
        X = last_sequence_scaled[-sequence_length:].reshape(1, sequence_length, 1)
        pred = model.predict(X)
        future_predictions.append(pred[0, 0])
        last_sequence_scaled = np.append(last_sequence_scaled, pred).reshape(-1, 1)

    future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))
    return future_predictions

# Main analysis pipeline
def analyze_market(ticker):
    # Fetch data
    data = fetch_historical_data(ticker)
    print(f"Historical Data for {ticker}:\n{data.tail()}\n")

    # Anomaly Detection
    data_with_anomalies = detect_anomalies(data)
    anomalies = data_with_anomalies[data_with_anomalies['Anomaly'] == -1]
    print(f"Detected Anomalies:\n{anomalies[['Close']]}\n")

    # Correlation Analysis
    corr_matrix = analyze_correlations(data)
    print("Correlation Matrix:\n", corr_matrix)

    # LSTM Forecasting
    X, y, scaler = preprocess_data(data)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = build_lstm_model((X_train.shape[1], 1))
    model.fit(X_train, y_train, epochs=50, batch_size=32)

    # Predict on test data
    predictions = model.predict(X_test)
    predictions = scaler.inverse_transform(predictions)
    y_test_actual = scaler.inverse_transform(y_test.reshape(-1, 1))

    # Forecast future prices
    future_predictions = forecast_future(model, data[['Close']].values, scaler)
    future_dates = pd.date_range(start=data.index[-1], periods=30+1, freq='B')[1:]

    # Plot results
    plt.figure(figsize=(15, 6))
    plt.plot(data.index[-len(y_test):], y_test_actual, label='Actual Prices')
    plt.plot(data.index[-len(y_test):], predictions, label='Predicted Prices')
    plt.plot(future_dates, future_predictions, label='Future Forecast', linestyle='--')
    plt.scatter(anomalies.index, anomalies['Close'], color='red', label='Anomalies')
    plt.title(f"{ticker} Stock Price Analysis")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.show()

# Execute the analysis
ticker = input("Enter the company ticker (e.g., AAPL, TSLA): ").upper()
analyze_market(ticker)