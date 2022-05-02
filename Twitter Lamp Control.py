# If @mr_lampy_lamp receives a tweet - flicker white
# if tweet include red/green/blue, flicker that colour
# If @lamp_lamp tweets, flicker white
# If tweet contains on/off, turn lamp on/off
# Tweet out the name, contents, and action taken, when a command tweet is received.

# TWEEPY METHODS:
# https://docs.tweepy.org/en/stable/client.html
# https://docs.tweepy.org/en/stable/api.html
# https://developer.twitter.com/en/docs/twitter-api/tweets/manage-tweets/api-reference/post-tweets

import configfile   # Lets you look at other files to...
import tweepy
import yeelight
import time

bulb = yeelight.Bulb(configfile.bulb_IP)
bulb.turn_on()
bulb.set_rgb(255,0,0) # red = default

my_bearer_token = configfile.my_bearer_token
consumer_key=configfile.API_key
consumer_secret=configfile.API_secret_key
access_token=configfile.accesstoken
access_token_secret=configfile.accesstokensecret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
# 'parser=' optional, but makes it return JSON rather than gibberish

def spam():
    x=0
    while True:
        time.sleep(3)
        x+=1
        api.update_status(x)
#spam()

def find_text():
    x=api.user_timeline()
    y=x[0]['text']
    print(y)
    if 'Test 1' in y:
        print('Found')
        bulb.set_rgb(255,0,0)
        time.sleep(1)
        bulb.set_rgb(0,255,0)
#find_text()


def check_own_new_tweet():  # Activates every time Lampy tweets
    x=api.user_timeline() # pulls data re: OWN tweets
    most_recent_text=x[0]['text']  # pulls account's most recent tweet's text
    most_recent_date=x[0]['created_at'] # pulls most recent tweet's date
    print(most_recent_date, most_recent_text)

    time.sleep(3)
    x=api.user_timeline() # Waits 3s then checks own tweets again...
    if most_recent_date != x[0]['created_at'] and most_recent_text != x[0]['text']:
        bulb.set_rgb(0,0,255) # if new tweet found, turns blue...
        time.sleep(3)
        bulb.set_rgb(255,0,0) # ...then red 3s later
    else: bulb.set_rgb(255,0,0) # Red is the default colour

while True: 
    check_own_new_tweet()

def post_to_self():    
    client = tweepy.Client(consumer_key=API_key,
        consumer_secret=API_secret_key,
        access_token=accesstoken,
        access_token_secret=accesstokensecret)
    client.create_tweet(text='Hi!')  # Tweets to authorised account:

if __name__ == '__main__':
    pass
