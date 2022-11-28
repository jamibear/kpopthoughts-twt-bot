import requests
import tweepy
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

# Reddit get hot posts from r/hauntedchocolatier
subreddit = 'hauntedchocolatier'
limit = 3
timeframe = 'month' #hour, day, week, month, year, all
listing = 'new' # controversial, best, hot, new, random, rising, top
 
def get_reddit(subreddit,listing,limit,timeframe):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}'
        request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
    except:
        print('An Error Occured')
    return request.json()
 
r = get_reddit(subreddit,listing,limit,timeframe)

# Twitter post tweets from subreddit 
client = tweepy.Client(
    consumer_key=os.getenv('CONSUMER_KEY'),
    consumer_secret=os.getenv('CONSUMER_SECRET'),
    access_token=os.getenv('ACCESS_TOKEN'),
    access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'),
)

def post_tweet(r, client):
    for post in r['data']['children']:
        twt_title = post['data']['title']
        twt_selftext = post['data']['selftext']
        new_twt = f'''
        {twt_title}

[🗨] {(twt_selftext[:175] + '...') if len(twt_selftext)>178 else twt_selftext}

        {post['data']['url']}
        '''
        client.create_tweet(text=new_twt)

post_tweet(r, client)
