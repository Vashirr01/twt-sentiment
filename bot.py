import tweepy
import os
from time import sleep
from dotenv import load_dotenv

load_dotenv()

#configuration
QUERY = 'saif ali khan'
LIKE = True
FOLLOW = True
SLEEP_TIME = 100

bearer_token = os.environ.get('BEARER_TOKEN')
consumer_key = os.environ.get('API_KEY')
consumer_secret = os.environ.get('API_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_SECRET')

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)
api = tweepy.API(auth, wait_on_rate_limit=True)

client = tweepy.Client(bearer_token=bearer_token)

def main():
    print("twitter bot which retweets, likes and follows users(for now)")
    print("bot settings")
    print("like tweets:", LIKE)
    print("follow users:", FOLLOW)

    try:
        tweets = client.search_recent_tweets(
            query=QUERY,
            max_results=10,
            tweet_fields=['author_id', 'created_at']
        )

        if not tweets.data:
            print("No tweets found matching the criteria.")
            return

        for tweet in tweets.data:
            try:

                print('\nTweet id: ' + str(tweet.id))
                print('\nTweet by: @' + str(tweet.author_id))

                api.retweet(tweet.id)
                print("Retweeted the tweet")

                if LIKE:
                    api.like(tweet.id)
                    print("liked the tweet")

                if FOLLOW:
                    api.follow_user(tweet.author_id)
                    print("Followed the user")

                sleep(SLEEP_TIME)

            except tweepy.errors.TweepyException as e:
                print(f"Error processing tweet: {e}")
                continue

    except tweepy.errors.TweepyException as e:
        print(f"Error: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
