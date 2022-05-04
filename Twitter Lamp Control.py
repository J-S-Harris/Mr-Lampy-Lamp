    # TO IMPLEMENT?:
# 1) Tweet out the sender's twitter handle, and action taken, when a command tweet is received.

# 2) Add time+date AND colour of each tweet to a dictionary
    # to record + replay a series of flashes!!!

# 3) Post everywhere! Molten twitter, UK Melee discord, etc

# 4) allow it to check for multiple colours, (incl. rgb), and cycle through all of them!
    # total ~16 seconds, i.e: 16/len(rgb+if_r+if_g+if_b)

# 5) Make it parse RGB with regex!

# 6) Update website with a few words per capability

# 7) Why rate limit????


# TWEEPY METHODS:
# https://docs.tweepy.org/en/stable/client.html
    # ^ methods
# https://docs.tweepy.org/en/stable/api.html
# https://developer.twitter.com/en/docs/twitter-api/tweets/manage-tweets/api-reference/post-tweets

import configfile
import tweepy
import yeelight
import time
import re

all_mentions =[]

bulb = yeelight.Bulb(configfile.bulb_IP, effect='smooth',duration=3000)
bulb.turn_on()
bulb.set_brightness(30)

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

#while True: 
#    check_own_new_tweet()


def check_mentions():
    x=api.mentions_timeline()
        # Make it so that a list of mentions is collected,
        # so no tweet gets missed.
        # Tweet out a thank you, pulling handle from JSON, and explaining what was done.
    most_recent_mention=x[0]['text']
    most_recent_mention_date=x[0]['created_at']
    time.sleep(15)
    while True:
        print(most_recent_mention, most_recent_mention_date)
        time.sleep(15)
        x=api.mentions_timeline(count=1)
        global all_mentions
        if x[0]['text'] not in all_mentions:
            all_mentions.append(x[0]['text'])
        bulb.turn_on()
        if most_recent_mention != x[0]['text'] and most_recent_mention_date != x[0]['created_at']:
            bulb.set_brightness(80)
            colours_list=[]
            if 'rgb' in x[0]['text'].lower():
                pass
                #use a regex and read that from the tweet!!
            if 'red' in x[0]['text'].lower():
                bulb.set_rgb(255,0,0)   # Change each of these lines to add respective colour to colours_list...
            if 'blue' in x[0]['text'].lower():
                bulb.set_rgb(0,0,255)
            if 'green' in x[0]['text'].lower():
                bulb.set_rgb(0,255,0)
            # ... then strobe them all for 16/colours seconds.
            time.sleep(12)  # Get rid of this?
            bulb.set_brightness(30)
            bulb.set_rgb(255,255,255)
            # Make it check here if there are any tweets in 'all_mentions' that haven't been flashed,
                # ^ and ONLY THEN get more (reduce API calls)
        x=api.mentions_timeline(count=1)
        most_recent_mention=x[0]['text']
        most_recent_mention_date=x[0]['created_at']
        

check_mentions()

def post_to_self():    
    client = tweepy.Client(consumer_key=API_key,
        consumer_secret=API_secret_key,
        access_token=accesstoken,
        access_token_secret=accesstokensecret)
    client.create_tweet(text='Hi!')  # Tweets to authorised account:

if __name__ == '__main__':
    pass
