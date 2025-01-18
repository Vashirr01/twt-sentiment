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

def main():
    print("twitter bot which retweets, likes and follows users(for now)")
    print("bot settings")
    print("like tweets:", LIKE)
    print("follow users:", FOLLOW)


    try:
        tweets = client.search_recent_tweets(
            query=QUERY,
            max_results=3,
            tweet_fields=['author_id', 'created_at']
        )

        if not tweets.data:
            print("No tweets found matching the criteria.")
            return

        for tweet in tweets.data:
            try:

                print('\nTweet id: ' + tweet.id)
                print('\nTweet by: @' + tweet.author_id)

                client.retweet(tweet.id)
                print("Retweeted the tweet")

                if LIKE:
                    client.like(tweet.id)
                    print("liked the tweet")

                if FOLLOW:
                    client.follow_user(tweet.author_id)
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
