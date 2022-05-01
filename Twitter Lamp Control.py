# If @lampy_lamp receives a tweet - flicker white
# if tweet include red/green/blue, flicker that colour
# If @lamp_lamp tweets, flicker white
# If tweet contains on/off, turn lamp on/off
# Tweet out the name, contents, and action taken, when a command tweet is received.


# TWEEPY METHODS:
# https://docs.tweepy.org/en/stable/client.html

import configfile   # Lets you look at other files to...
import tweepy
API_key = configfile.API_key    # ...import variables, functions, etc from them!
API_secret_key = configfile.API_secret_key
my_bearer_token = configfile.my_bearer_token
accesstoken = configfile.accesstoken
accesstokensecret = configfile.accesstokensecret

import yeelight
bulb = yeelight.Bulb(configfile.bulb_IP)

#https://developer.twitter.com/en/docs/twitter-api/tweets/manage-tweets/api-reference/post-tweets


def main():
    
    #if 'toggle' in [tweet]:
        #bulb.toggle()
    
    # Tweets to authorised account:
#client = tweepy.Client(consumer_key=API_key,
 #   consumer_secret=API_secret_key,
  #  access_token=accesstoken,
   # access_token_secret=accesstokensecret)
#client.create_tweet(text='Hi!')
    # DOESN'T WORK YET - WAIT FOR ELEVATED PERMISSIONS EMAIL (check spam)

if __name__ == '__main__':
    main()
