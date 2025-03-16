# This function gets real-time cryptocurrency prices every day at 8 AM
# It also saves the data as a CSV
# It identifies the top 10 cryptos and sends emails

import requests
import pandas as pd
from datetime import datetime

# API information
url = 'https://api.coingecko.com/api/v3/coins/markets'
param = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc',
    'per_page': 250,
    'page': 1
}

# Sending request
response = requests.get(url, params=param)

if response.status_code == 200:
    print('Connection Successful! \nGetting the data...')
    
    # Storing the response into data
    data = response.json()
    
    # Creating dataframe
    df = pd.DataFrame(data)
    
    # Selecting relevant columns
    df = df[['id', 'current_price', 'market_cap', 'price_change_percentage_24h', 'ath', 'atl']]
    
    # Creating timestamp
    today = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')  # ✅ Replaces ":" with "_"
    df['time_stamp'] = today
    
    # Getting top 10 losers
    top_negative_10 = df.sort_values(by='price_change_percentage_24h', ascending=True).head(10)
    top_negative_10.to_csv(f'top_negative_10_{today}.csv', index=False)  # ✅ Fixed filename
    
    # Getting top 10 gainers
    top_positive_10 = df.sort_values(by='price_change_percentage_24h', ascending=False).head(10)
    top_positive_10.to_csv(f'top_positive_10_{today}.csv', index=False)  # ✅ Fixed filename
    
    # Saving the full data
    df
