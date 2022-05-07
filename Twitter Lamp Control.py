    # TO IMPLEMENT AND MENTION ON WEBSITE:
# 1) Tweet out the sender's twitter handle, and action taken, when a command tweet is received.

# 2) Add time+date AND colour of each tweet to a dictionary
    # to record + replay a series of flashes!!!

# 3) Post everywhere! Molten twitter, UK Melee discord, etc

# 4) Allow multiple colours per tweet
    #(DONE! 10 per tweet; disco mode)

# 5) Make it parse RGB with regex!

# 6) Update website with a few words per 

# 7) Optimise the final wait for as little down time as poss

# 8) Currently skips tweets??

# 9) Why does the Bulb API max out after only a few colours? How does it work/what is the rate limit????

# 10) Add new colours (orange, purple, pink, yellow)
    # DONE

# 11) Update website with details of project; add github link to website
    # 11b) add version control/github knowledge to cv; add

# 12) If given a non-colour string, make it flash white rather than skip it

# 13 !!!! ADD feedback for tweeters - tweet them back with action taken !!!!
        # OR automatically record flashes an upload??? Put vid in tweet?


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

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
# 'parser=' optional, but makes it return JSON rather than gibberish


# api.update_status(x)
    # ^ Tweets 'x'

# Main function:
def check_mentions():

    global all_senders
    global all_dates
    global all_mentions
    
    x=api.mentions_timeline() # establishes initial list of mentions

    for i in x:
        all_senders.append(i['user']['screen_name'])
        all_dates.append(i['created_at'])
        all_mentions.append(i['text'])

    while True:
        
        global colour_duration
        global colours_list
        
        x=api.mentions_timeline()    # refreshes list of most recent mentions
        for i in x:
            if i['created_at'] not in all_dates:

                all_senders.append(i['user']['screen_name'])
                all_dates.append(i['created_at'])
                all_mentions.append(i['text'])            

                bulb.turn_on()
                bulb.set_brightness(80) # Flash brightness

                global colours_list
                colours_list=[]

                most_recent_mention = i['text']
                most_recent_mention = most_recent_mention.split()
                for z in most_recent_mention:
                    print('z:',z)
                    if z == 'red':
                        colours_list.append('red')
                    elif z == 'blue':
                        colours_list.append('blue')
                    elif z == 'green':
                        colours_list.append('green')
                    elif z == 'white':
                        colours_list.append('white')
                    elif z == 'purple':
                        colours_list.append('purple')
                    elif z == 'orange':
                        colours_list.append('orange')
                    elif z == 'pink':
                        colours_list.append('pink')
                    elif z == 'yellow':
                        colours_list.append('yellow')
                    
                    #elif 'rgb' in z:
                        # regex to find colours directly between 'rgb(' and ')'
                print(colours_list)
                if len(colours_list) == 0:
                    colours_list.append('white')
                global colour_duration
                colour_duration = 20/int(len(colours_list))
                print('colour duration assigned:',colour_duration)

                x=0
                for z in colours_list:
                    if x<10:
                        x+=1
                        print(x)
                        if z == 'red':  # Make this a dictionary of colour/rgb key/value pairs
                            bulb.set_rgb(255,0,0)   # WHY DOES API MAX OUT? Increase the colour_duration integer??? [what is the limit? not 60a minute???
                            time.sleep(colour_duration)
                        elif z == 'blue':
                            bulb.set_rgb(0,0,255)
                            time.sleep(colour_duration)
                        elif z == 'green':
                            bulb.set_rgb(0,255,0)
                            time.sleep(colour_duration)
                        elif z == 'white':
                            bulb.set_rgb(200,200,200)
                            time.sleep(colour_duration)
                        elif z == 'purple':
                            bulb.set_rgb(128,0,190)
                            time.sleep(colour_duration)
                        elif z == 'orange':
                            bulb.set_rgb(255,172,28)
                            time.sleep(colour_duration)
                        elif z == 'pink':   # HOW MAKE PURPLE AND PINK LESS SIMILAR?
                            bulb.set_rgb(255,0,255)
                            time.sleep(colour_duration)
                        elif z == 'yellow':
                            bulb.set_rgb(255,234,0)
                            time.sleep(colour_duration)
                        #elif ',' in z:
                            # regex to see if it is (num,num,num)                            
                            #bulb.set_rgb(z)
                            #time.sleep(colour_duration)
                print('end of colours flashed?')
        
            bulb.set_brightness(30) # Resting brightness
            bulb.set_rgb(0,100,100)

        print('\nT E S T: end of function\n\n',all_senders,'\n\n',all_dates,'\n\n',all_mentions,'\n\n') # TEST SCRIPT
        
        
        time.sleep(30-(2*len(colours_list))) # Should always lead to 26s cycles (16 lit up)

if __name__ == '__main__':
    check_mentions()
