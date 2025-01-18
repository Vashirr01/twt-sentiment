import re
import os
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient:
    def __init__(self):
        consumer_key = os.environ.get('API_KEY')
        consumer_secret = os.environ.get('API_SECRET')
        access_token = os.environ.get('ACC_TOKEN')
        access_token_secret = os.environ.get('ACC_SECRET')
        
        try:
            self.client = tweepy.Client(
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_token=access_token,
                access_token_secret=access_token_secret
            )
        except Exception as e:
            print(f"Error: Authentication Failed - {str(e)}")

    def clean_tweet(self, tweet):
        """Remove special characters and links from tweet."""
        return ' '.join(
            re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\\w+:\\/\\/\\S+)",
                  " ",
                  tweet).split())

    def get_tweet_sentiment(self, tweet):
        """Determine sentiment of tweet using TextBlob."""
        analysis = TextBlob(self.clean_tweet(tweet))
        
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        """Fetch tweets and return list with text and sentiment."""
        tweets = []
        try:
            # Using the new Twitter API v2 endpoint
            fetched_tweets = self.client.search_recent_tweets(
                query=query,
                max_results=count
            )
            
            if fetched_tweets.data:
                for tweet in fetched_tweets.data:
                    parsed_tweet = {
                        'text': tweet.text,
                        'sentiment': self.get_tweet_sentiment(tweet.text)
                    }
                    tweets.append(parsed_tweet)
                    
            return tweets
        except tweepy.errors.TweepyException as e:
            print(f"Error: {str(e)}")
            return None

def main():
    # Initialize the TwitterClient
    api = TwitterClient()
    
    # Get tweets for the search query
    tweets = api.get_tweets(query='Elon Musk', count=10)
    
    # Check if tweets were retrieved successfully
    if tweets is None or len(tweets) == 0:
        print("No tweets were retrieved. Please check your API credentials and query.")
        return

    # Filter positive tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    print("Positive tweets percentage: {:.2f}%".format(100 * len(ptweets) / len(tweets)))
    
    # Filter negative tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    print("Negative tweets percentage: {:.2f}%".format(100 * len(ntweets) / len(tweets)))
    
    # Calculate neutral tweets
    neutral_count = len(tweets) - (len(ntweets) + len(ptweets))
    print("Neutral tweets percentage: {:.2f}%".format(100 * neutral_count / len(tweets)))

    # Print all positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets:
        print(tweet['text'])

    # Print all negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets:
        print(tweet['text'])

if __name__ == "__main__":
    main()
