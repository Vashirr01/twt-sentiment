import tweepy
from time import sleep
from config import QUERY, FOLLOW, LIKE, SLEEP_TIME
from dotenv import load_dotenv
load_dotenv()


bearer_token = os.environ.get('BEARER_TOKEN')
client = tweepy.Client(
    bearer_token = bearer_token
)

print("twitter bot which retweets, likes and follows users(for now)")
print("bot settings")
print("like tweets:", LIKE)
print("follow users:", FOLLOW)

for tweet in tweepy.Cursor(api.search, q=QUERY).items():
    try:
        print('\nTweet by: ')
