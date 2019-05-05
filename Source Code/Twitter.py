#Import libraries
import tweepy
import json
from textblob import TextBlob
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
consumer_key= 'lfwX1K8WKvRKiMJbFdAHWasAP'
consumer_secret= 'CdP3aCqeqh0VlxPZMU32yQqYfB81A5fUdLKXuqNXvcjRoFtsJZ'
access_token='1112419514531106818-mfrqvlgd663qHNsvjonH9FMwRo9DeV'
access_token_secret='6Dhqvrwf3TkS832WPvHYYZCUt4SyYN3szy5pnq4GWrdUz'

# basic listener that prints received tweets to stdout.
class StdOutListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        for url in tweet["entities"]["urls"]:
            print (" - found URL: %s" % url["expanded_url"])
        return True
    def on_error(self, status):
        print (status)


# Given a string query, search Twitter for Tweets containing word
# and returns overall sentiment and a tweet that contains the query
def search_twitter(query):
    # handling Twitter authentification
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth_handler=auth)
    search_results = api.search(query)

    threshold = 0
    pos_sent_tweet = 0
    neg_sent_tweet = 0
    sentiment = 'Unknown'
    for tweet in search_results:
        analysis = TextBlob(tweet.text)
        if analysis.sentiment.polarity >= threshold:
            pos_sent_tweet = pos_sent_tweet + 1
        else:
            neg_sent_tweet = neg_sent_tweet + 1
    if pos_sent_tweet > neg_sent_tweet:
        sentiment = 'Positive'
    else:
        sentiment = 'Negative'

    for result in search_results:
        id_str = result._json['id_str']
        raw_html = api.get_oembed(id_str)['html']
        embed_html = raw_html.split('<script')[0]
        return sentiment, embed_html
