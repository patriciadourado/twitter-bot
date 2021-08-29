# coding=utf-8
import os
import time
import logging
import tweepy
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# API key
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
# API secret key
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
# Access token
KEY = os.getenv('KEY')
# Access token secret
SECRET = os.getenv('SECRET')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(KEY, SECRET)

# Create API object
api = tweepy.API(auth)

# First tweet from your bot account!
# api.update_status('bot tweeting live!')

FILE_NAME = 'last_seen.txt'

def read_last_seen(FILE_NAME):
  file_read = open(FILE_NAME,'r')
  last_seen_id = int(file_read.read().strip())
  file_read.close()
  return last_seen_id

def store_last_seen(FILE_NAME, last_seen_id):
  file_write = open(FILE_NAME,'w')
  file_write.write(str(last_seen_id))
  file_write.close()
  return

def reply():
  tweets = api.mentions_timeline(read_last_seen(FILE_NAME), tweet_mode = 'extended')

  for tweet in reversed(tweets):
    if 'brazil' in tweet.full_text.lower():
      api.update_status("@" + tweet.user.screen_name + " In brazilian portuguese we don't say foreign we say GRINGO and I think that is beautiful!", tweet.id)
      store_last_seen(FILE_NAME, tweet.id)

def retweet():
  for tweet in api.search(q="brazilian", lang="en", count=25):
    status = api.get_status(tweet.id, tweet_mode = 'extended')
    if not status.retweeted:  # Check if Retweet
      try:
        api.retweet(tweet.id)
      except Exception as e:
        logger.error("Error on retweet", exc_info=True)

def favorite():
  for tweet in api.search(q="brazilian", lang="en", count=25):
      try:
        api.create_favorite(tweet.id)
      except Exception as e:
        logger.error("Error on retweet", exc_info=True)

def retweet_and_reply(i):
  for tweet in api.search(q="brazilian", lang="en", count=12):
    status = api.get_status(tweet.id, tweet_mode = 'extended')
    if not status.retweeted:  # Check if Retweet
      try:
        i = i + 1
        api.update_status("@" + tweet.user.screen_name + " In brazilian portuguese we don't say foreign we say GRINGO and I think that is beautiful! +"+str(i), tweet.id)
        api.retweet(tweet.id)
      except Exception as e:
        logger.error("Error on retweet", exc_info=True)

def see():
  for tweet in api.search(q="brazilian", lang="pt", count=25):
    status = api.get_status(tweet.id, tweet_mode = 'extended')
    try:
      print(str(tweet.id) + status.retweetd_status.full_text)
    except Exception as e:
      print(str(tweet.id) + ' - ' + status.full_text)
      logger.error("Error on retweet", exc_info=True)

i = 0
while True:
  # reply()
  # retweet()
  favorite()
  # retweet_and_reply(i)
  # see()
  time.sleep(900)