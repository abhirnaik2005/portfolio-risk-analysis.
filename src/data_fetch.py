import requests
import pandas as pd
import os

# Replace with your Alpha Vantage API key
ALPHA_VANTAGE_API_KEY = 'ONER6IXAETD06BUY'

def fetch_data(symbol, outputsize='compact'):
    """
    Fetch historical data for a given stock symbol using Alpha Vantage API.
    Args:
        symbol (str): The stock ticker symbol (e.g., AAPL for Apple).
        outputsize (str): 'compact' for last 100 data points, 'full' for full history.
    Returns:
        pd.DataFrame: Dataframe containing historical price data.
    """
    base_url = 'https://www.alphavantage.co/query?'
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': ALPHA_VANTAGE_API_KEY,
        'datatype': 'json',
        'outputsize': outputsize
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()

    # Check if the API returned valid data
    if 'Time Series (Daily)' not in data:
        raise ValueError(f"Failed to fetch data for {symbol}. Error: {data}")
    
    time_series = data['Time Series (Daily)']
    df = pd.DataFrame.from_dict(time_series, orient='index')
    df.index = pd.to_datetime(df.index)
    
    # Rename columns for better readability
    df.columns = ['open', 'high', 'low', 'close', 'volume']
    
    # Convert columns to numeric values
    df = df.apply(pd.to_numeric)
    return df

def save_data(df, symbol):
    """
    Save the fetched data to a CSV file.
    Args:
        df (pd.DataFrame): Dataframe containing the stock data.
        symbol (str): Stock ticker symbol.
    """
    output_path = f'../data/{symbol}_data.csv'
    df.to_csv(output_path)
    print(f"Data for {symbol} saved to {output_path}")

if __name__ == '__main__':
    symbol = 'AAPL'  # Example stock symbol
    try:
        data = fetch_data(symbol)
        save_data(data, symbol)
    except ValueError as e:
        print(e)
