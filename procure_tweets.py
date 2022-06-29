### Gibson Farabow, Nov 23
### Project procuring Twitter tweets with the tweepy API
### 3 sections: get data by iterating through selected accounts, streaming realtime tweets, and iterating through tweet query results

import tweepy
import pandas as pd
import TextBlob
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

        
### get statistics of twitter accounts, in this case average favorites and retweets for the past 500 tweets

def twit_stats(twitter_handle):
    ''' get account info in json form'''
    j = api.get_user(screen_name=twitter_handle)
    js = j._json
    followers = js["followers_count"]
    on_lists = js["listed_count"]
    ### get tweets
    timeline = api.user_timeline(screen_name=twitter_handle, include_rts=False, exclude_replies=True, count=500)
    # create a dictionary of associated json data for each tweet
    tweets = {}
    for count in range(len(timeline)):
        c = 0
        for i in timeline:
            if c == count:
                tweets[count] = i._json
            c += 1 
    # index dictionary to find favorites and retweets for each tweet, then avg them
    favs=[]
    rts=[]
    for i in range(len(timeline)):
        favs.append(tweets[i]['favorite_count'])
        rts.append(tweets[i]['retweet_count'])
    f_avg = round(sum(favs) / len(favs), 2)
    rt_avg = round(sum(rts) / len(rts), 2)
    #print("average favorites: " + str(f_avg))
    #print("average retweets: " + str(rt_avg))
    row = [twitter_handle, followers, on_lists, f_avg, rt_avg]
    return row

def twitter_table(row, twit_table):
    screen_name=row[0]
    twit_table.loc[screen_name] = row[1:]
    return twit_table


# manually set columns 
twit_table = pd.DataFrame(columns = ["Followers", "Listed_Count", "avg_Favorites", "avg_Retweets"])

# create list of twitter handles at any length to pass through the program 
twitterhandles=["nytimes", "FoxNews", "CNN", "WSJ", "BreitbartNews", "HuffPost" ]

# create a table with twitter handles as an index that can be downloaded as a csv
for account in twitterhandles:
    row = twit_stats(account)
    twit_table = twitter_table(row, twit_table)

#twit_table.to_csv(r'[file location]')


### Stream Tweets in realtime 

# initialize any factors interested in - this program does basic sentiment analysis of negative or positive polarity
p = SentimentIntensityAnalyzer()
#avg = []

class StreamListener(tweepy.Stream):
    def on_status(self, status):
        if 'extended_tweet' in status._json:
            txt = status.extended_tweet['full_text']
            x = p.polarity_scores(txt)['compound']
            if x != 0:
                #avg.append(x)
                print("###")
                print(txt, '\n')
                print(x)
                print('###\n')

MyListener = StreamListener(consumer_key, consumer_secret, access_token, access_token_secret)

# run program 
#MyListener.filter(track=['facebook'], languages=['en'], locations=[-79.08, 35.90,-78.96, 35.99], filter_level=['low'])


### iterate through tweets
#avg = []
for tweet in tweepy.Cursor(api.search_tweets, "facebook", count=100).items(5000):
    if len(tweet.text) == 23 and ("https://t." in tweet.text): # filter if only a link
        pass
    if TextBlob(tweet.text).sentiment.polarity == 0:
        pass
    else:
        # to get the full text of a tweet, instead of the default snippet, a different query method (get_status) is needed
        i = tweet.id
        text = api.get_status(i, tweet_mode='extended')
        print(text.full_text)
        x = text.full_text
        c = (p.polarity_scores(x)['compound'])
        print(c)
        avg.append(c)
        print('###')

#avg1 = sum(avg) / len(avg)







