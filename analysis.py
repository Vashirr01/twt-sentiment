import re
import os
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):

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
            print(&quot;Error: Authentication Failed&quot;)

    def clean_tweet(self, tweet):

        return ' '.join(re.sub(&quot;(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)&quot;, &quot; &quot;,tweet).split())

    def get_tweet_sentiment(self, tweet):

        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity &gt; 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count = 5):

        tweets = []

        tr


