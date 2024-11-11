import os
import requests
import pandas as pd
from flask import Flask, jsonify

app = Flask(__name__)

ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

def get_daily_stock_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if 'Time Series (Daily)' in data:
        df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
        df = df.rename(columns={
            '1. open': 'Open',
            '2. high': 'High',
            '3. low': 'Low',
            '4. close': 'Close',
            '5. volume': 'Volume'
        })
        return df.reset_index().to_dict(orient='records')
    else:
        return {"error": "Data not found"}

def get_intraday_stock_data(symbol, interval):
    url = (
        f"https://www.alphavantage.co/query"
        f"?function=TIME_SERIES_INTRADAY"
        f"&symbol={symbol}"
        f"&interval={interval}"
        f"&apikey={ALPHA_VANTAGE_API_KEY}"
    )
    response = requests.get(url)
    data = response.json()
    
    # Construct the correct key based on the interval
    time_series_key = f'Time Series ({interval})'
    
    if time_series_key in data:
        df = pd.DataFrame.from_dict(data[time_series_key], orient='index')
        df = df.rename(columns={
            '1. open': 'Open',
            '2. high': 'High',
            '3. low': 'Low',
            '4. close': 'Close',
            '5. volume': 'Volume'
        })
        return df.reset_index().to_dict(orient='records')
    else:
        # Check for error messages in the response
        error_message = data.get('Error Message', 'Data not found or API limit reached')
        return {"error": error_message}

@app.route('/api/data/daily/<symbol>', methods=['GET'])
def get_daily_data(symbol):
    return jsonify(get_daily_stock_data(symbol))

@app.route('/api/data/intraday/<symbol>/<interval>', methods=['GET'])
def get_intraday_data(symbol, interval):
    return jsonify(get_intraday_stock_data(symbol, interval))


if __name__ == "__main__":
    app.run(port=5001)