import snscrape.modules.twitter as sntwitter
import pytz
import re
import os
from tqdm import tqdm
import emoji
import pandas as pd
import urllib.request
import logging
import random
import time


# UTC convert to JST
def change_time(utc_time):
    jst_time = utc_time.astimezone(pytz.timezone("Asia/Tokyo"))
    # change to str
    str_time = jst_time.strftime("%Y-%m-%d_%H:%M:%S")
    return str_time

  
# File name set to tweet time (japan time)
def change_name(date):
    date_modify = re.sub("\:| ", "", date)
    new_date = re.sub("-", "_", date_modify)
    return new_date


# image download -- Supports multiple numbers
def picDL(name, datas):
    title = ["a", "b", "c", "d"]
    for index in range(len(datas)):
        # print(title[p],tweet.media[p].fullUrl)
        photo_url = datas[index].fullUrl
        photo_name = name + "_{}.jpg".format(title[index])
        urllib.request.urlretrieve(photo_url, photo_name)


# Video download--save all gifs and videos in mp4 format
def movieDL(name, datas):
    video_url = datas[0].url
    bit = int(datas[0].bitrate or 0)
    for index in range(len(datas) - 1):
        if bit > int(datas[index + 1].bitrate or 0):
            video_url = video_url
        else:
            video_url = datas[index + 1].url
            bit = int(datas[index + 1].bitrate or 0)
    video_name = name + ".mp4"
    urllib.request.urlretrieve(video_url, video_name)


# Delete emoji in tweets
def remove_emoji(src_str):
    noemoji = ''.join(c for c in src_str if c not in emoji.EMOJI_DATA)
    newtext = re.sub("\n", "", noemoji)
    return newtext


# Create a folder for each user
def makeDIR(girl):
    document_path = os.getenv("USERPROFILE") + "/Pictures"
    path = document_path + "/" + girl
    if not os.path.exists(path):
        os.mkdir(path)
    os.chdir(path)


def media_down(name, limit):
    global file_name
    tweet_count = 0
    pic_count = 0
    video_count = 0
    for tweet in tqdm(sntwitter.TwitterSearchScraper(name).get_items(), total=limit):
        if len(tweets) == limit:
            break
        else:
            tweets.append(
                [tweet.id, change_time(tweet.date), remove_emoji(tweet.rawContent), tweet.likeCount, tweet.retweetCount,
                 tweet.quoteCount, tweet.replyCount])
            tweet_count = tweet_count + 1
            file_name = change_name(change_time(tweet.date))
            if tweet.media:
                for medium in tweet.media:
                    if isinstance(medium, sntwitter.Photo):  # download pictures
                        try:
                            picDL(name=file_name, datas=tweet.media)
                            pic_count = pic_count + len(tweet.media)
                            break
                        except Exception as e:
                            logging.exception(e)
                    elif isinstance(medium, sntwitter.Video) or isinstance(medium, sntwitter.Gif):  # download videos
                        try:
                            movieDL(name=file_name, datas=medium.variants)
                            video_count = video_count + 1
                            break
                        except Exception as e:
                            logging.exception(e)
                time.sleep(random.randint(0, 1))
    # tweet data save into database
    df = pd.DataFrame(tweets, columns= ['id', 'Date', 'Tweet', 'like', 'RT', 'quote', 'reply'])
    # check csv header
    if os.path.exists(csv_file):
        header = None
    else:
        header = ['id', 'Date', 'Tweet', 'like', 'RT', 'quote', 'reply']
    # save to csv file.
    df.to_csv(csv_file, mode='a+', index=False, header=header, encoding='utf-8-sig')
    print(
        "Task finish.\nTotal checked tweets:{}\nNumber of Downloaded Videos:{}\nNumber of Downloaded Pictures:{}\n".format(
            tweet_count, video_count, pic_count))

if __name__ == '__main__':
    query = "(from:XXXOOO) -filter:replies until:2023-01-30 since:2021-03-01"   # XXXOOO is the user name
    limit = 500              #  How many tweets you want to check
    # create media folder's name and tweets sheet's name
    fav = "XXXXX"
    makeDIR(fav)
    csv_file = 'tw_{}.csv'.format(fav)
    tweets = []
    media_down(name=query, limit=limit)
    # Delete Duplicate data
    df = pd.read_csv(csv_file)
    df.drop_duplicates(subset=['id'], inplace=True, keep='first')
    # save the csv files
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    print('Data checked is over!')
