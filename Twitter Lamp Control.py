    # TO IMPLEMENT AND MENTION ON WEBSITE:
# 1) Tweet out the sender's twitter handle, and action taken, when a command tweet is received.

# 2) Add time+date AND colour of each tweet to a dictionary
    # to record + replay a series of flashes!!!

# 5) Make it parse RGB with regex!

# 6) Update website with a few words per 

# 7) Optimise the final wait for as little down time as poss


# 9) Why does the Bulb API max out after only a few colours? How does it work/what is the rate limit????

# 10) Add new colours (orange, purple, pink, yellow)

# 11) Update website with details of project; add github link to website
    # 11b) add version control/github knowledge to cv; add

# 13 !!!! ADD feedback for tweeters - tweet them back with action taken !!!!
        # OR automatically record flashes an upload??? Put vid in tweet?

#14) Why UTC time, how set to UK time?


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

bulb = yeelight.Bulb(configfile.bulb_IP, effect='smooth',duration=1000)
bulb.turn_on()
bulb.set_brightness(30)
bulb.set_rgb(0,100,100)

my_bearer_token = configfile.my_bearer_token
consumer_key=configfile.API_key
consumer_secret=configfile.API_secret_key
access_token=configfile.accesstoken
access_token_secret=configfile.accesstokensecret

all_senders = []
all_dates = []
all_mentions =[]
colour_duration=''
colours_list=''
possible_colours = {
    'red':255,
    'blue':0,
    'green':0,
    'white':255,
    'purple':255,
    'orange':255,
    'pink':255,
    'yellow':255,
    }

possible_colours2 = {
    'red':0,
    'blue':0,
    'green':255,
    'white':255,
    'purple':0,
    'orange':165,
    'pink':105,
    'yellow':255,
    }

possible_colours3 = {
    'red':0,
    'blue':255,
    'green':0,
    'white':255,
    'purple':255,
    'orange':0,
    'pink':180,
    'yellow':0
    }

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

def check_mentions():
    global all_senders
    global all_dates
    global all_mentions
    
    x=api.mentions_timeline()
    for i in x:
        all_senders.append(i['user']['screen_name'])
        all_dates.append(i['created_at'])
        all_mentions.append(i['text'])

    while True:
        global colour_duration
        global colours_list
        global colours_tweeted
        colours_list=[]
        x=api.mentions_timeline()
        for i in x:
            colours_tweeted=[]
            if i['created_at'] not in all_dates:
                global possible_colours
                print(i['created_at'])
                all_senders.append(i['user']['screen_name'])
                all_dates.append(i['created_at'])
                all_mentions.append(i['text'])            
                most_recent_mention = i['text']
                most_recent_mention = most_recent_mention.split()

                print('Colours in this tweet:',most_recent_mention)
                for ii in most_recent_mention:
                    if ii in possible_colours:
                        colours_list.append(ii)
                        colours_tweeted.append(ii)
                print(colours_list)
                global colour_duration

                tweeter = i['user']['screen_name']
                tweet_id = i['id_str']
                print('reply id:', tweet_id)
                print('sender: ',tweeter)
                message = 'Thank you @'+tweeter+'! The bulb will flash the colours you tweeted! ('+i['created_at']+')'
                #if len(colours_list) < 3:
                    # message = message + "This includes these colours:',colours_list[0]+',',colours_list[0]+',',colours_list[0]+'.'"
                if '_Lampy_' not in tweeter:
                    api.update_status(status=message, in_reply_to_status_id=tweet_id)
                    print('tweet made:',message)
                
        print('All colours to flash: ',colours_list)
        for i in colours_list:
            bulb.set_brightness(80)
            bulb.set_rgb(possible_colours[i],possible_colours2[i],possible_colours3[i])
            time.sleep(2)
        bulb.set_brightness(30)
        bulb.set_rgb(0,100,100)
        snooze = 16-(2*len(colours_list))
        if snooze>= 0:
            time.sleep(snooze)

if __name__ == '__main__':
    check_mentions()
