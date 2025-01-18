import tweepy
import os
from time import sleep
from dotenv import load_dotenv

load_dotenv()

#configuration
QUERY = '# saifalikhan'
LIKE = True
FOLLOW = True
SLEEP_TIME = 150

bearer_token = os.environ.get('BEARER_TOKEN')
client = tweepy.Client(
    bearer_token = bearer_token
)

print("twitter bot which retweets, likes and follows users(for now)")
print("bot settings")
print("like tweets:", LIKE)
print("follow users:", FOLLOW)

for tweet in tweepy.Cursor(client.search, q=QUERY).items():

    try:
        print('\nTweet by: @' + tweet.user.screen_name)
        tweet.retweet()
        print("Retweeted the tweet")

        if LIKE:
            tweet.favorite()
            print("Favorited the tweet")

        if FOLLOW:
            if not tweet.user.following:
                tweet.user.follow()
                print("Followed the user")

        sleep(SLEEP_TIME)

    except tweepy.TweepError as e:
        print(e.reason)

    except StopIteration:
        break
