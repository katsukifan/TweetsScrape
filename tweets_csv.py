import snscrape.modules.twitter as sntwitter
import pandas as pd
from tqdm import tqdm, trange
from datetime import datetime,timezone
import pytz
import re
import os
import emoji
import urllib.request

#UTC convert to JST
def change_time(utc_time):

    jst_time = utc_time.astimezone(pytz.timezone("Asia/Tokyo"))
    # return as a string
    str_time = jst_time.strftime("%Y-%m-%d_%H:%M:%S")
    return str_time

#Set the file name to the date and time of the tweet (Japan time)
def change_name(date):
    date_modify = re.sub("\:| ", "", date)
    return date_modify

#Delete emoji in tweets
def remove_emoji(src_str):
    noemoji = ''.join(c for c in src_str if c not in emoji.EMOJI_DATA)
    newtext =  re.sub("\n", "", noemoji)
#    newtext1 =  re.sub(r'http\S+', "", newtext)
    return newtext

#Create a folder for each user function
def makeDIR(name):
            document_path = os.getenv("USERPROFILE") + "/Pictures"
            path = document_path+"/"+name
            if not os.path.exists(path):
                os.mkdir(path)
            os.chdir(path)


# query = "(from:rin_agemon) -filter:replies"
query = "(from:babyblue_72) -filter:replies until:2022-11-25 since:2021-01-01"
tweets = []
limit = 1000

#create the folder
makeDIR("babyblue_72")

for tweet in tqdm(sntwitter.TwitterSearchScraper(query).get_items(),total=limit):
    # json.loads(vars(tweet).['content'])
    # print(vars(tweet))
    # break
    if len(tweets) == limit:
        break
    else:
        tweets.append([tweet.id,change_time(tweet.date),remove_emoji(tweet.content),tweet.likeCount,tweet.retweetCount,tweet.quoteCount,tweet.replyCount])


df = pd.DataFrame(tweets, columns=['id','Date','Tweet','like','RT','quote','reply',])

df.to_csv("babyblue_72.csv",encoding='utf-8-sig')

print("Task finish.\nTotal saved tweets:{}\n".format(len(tweets)))