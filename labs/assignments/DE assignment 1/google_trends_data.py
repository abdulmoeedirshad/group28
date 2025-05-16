from pytrends.request import TrendReq
import pandas as pd
import os

def fetch_google_trends(keywords, timeframe='today 12-m', geo='PK'):
    ##google data fetch
    pytrends = TrendReq()
    pytrends.build_payload(keywords, timeframe=timeframe, geo=geo)
    trends_data = pytrends.interest_over_time()
    
    if 'isPartial' in trends_data.columns:
        trends_data = trends_data.drop(columns=['isPartial'])
    
    return trends_data

def save_to_csv(df, filename):
    #saveing to csv
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df.to_csv(filename, index=True)

def main():
    keywords = ["electric vehicle", "Tesla", "EV charging", "EV price"]
    df = fetch_google_trends(keywords)
    save_to_csv(df, "datasets/raw/google_trends.csv")
    print("Google Trends data saved successfully.")
    
if __name__ == "__main__":
    main()