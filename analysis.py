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
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        """Remove special characters and links from tweet."""
        return ' '.join(
            re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)",
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

    def get_tweets(self, query, count=5):
        """Fetch tweets and return list with text and sentiment."""
        tweets = []

        try:
            fetched_tweets = self.api.search(q=query, count=count)
            
            for tweet in fetched_tweets:
                parsed_tweet = {
                    'text': tweet.text,
                    'sentiment': self.get_tweet_sentiment(tweet.text)
                }
                
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
                    
            return tweets

        except tweepy.TweepError as e:
            print("Error: " + str(e))


