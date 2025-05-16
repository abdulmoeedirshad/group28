import praw
import pandas as pd
import os

def fetch_reddit_data(subreddit_name, keywords, limit=200):
    #reddit api
    reddit = praw.Reddit(
        client_id='p_NydHVpTprO7ejCqYvD4Q',
        client_secret='3hdwXlNNI3_Lu_srfwDN7Z9TXG4Z_Q',
        user_agent='EVDataScraper/1.0 by hisham_fawad'
    )

    
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    
    for submission in subreddit.hot(limit=limit):
        if any(keyword.lower() in submission.title.lower() for keyword in keywords):
            posts.append({
                'title': submission.title,
                'text': submission.selftext,
                'author': str(submission.author),
                'date': submission.created_utc,
                'upvotes': submission.score,
                'subreddit': subreddit_name
            })
    
    return pd.DataFrame(posts)

def save_to_csv(df, filename):
    ##saving to CSV
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df.to_csv(filename, index=False)

def main():
    keywords = ["electric vehicle", "EV", "Tesla", "charging"]
    df = fetch_reddit_data("ElectricVehicles", keywords)
    save_to_csv(df, "datasets/raw/reddit_posts.csv")
    print("Reddit data saved successfully.")
    
if __name__ == "__main__":
    main()