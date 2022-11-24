import snscrape.modules.twitter as sntwitter
import pandas as pd
from time import sleep
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
    date_modify1 = re.sub("-", "_", date_modify)
    return date_modify1


#Image download--Multiple images supported

def picDL(check_url):
    new_file = tweets[j][0]
    title =["a","b","c","d"]
    for i in range(len(check_url)):
        image_url = check_url[i].fullUrl
        # urllib.request.urlretrieve(image_url,new_file+"_"+title[i]+".jpg")
        print(image_url)


#Video download--save all gifs and videos in mp4 format

def movieDL(check_url):
    new_file = tweets[j][0]
    tw_video = re.findall(r'https\S+mp4',str(check_url))
    movie_url = tw_video[0]
    # for k in range(len(check_url)):
    #     movie_url.append(str(check_url[k]["url"]))
    #     movie_size.append(int(urllib.request.urlopen(movie_url[k]).info()['Content-Length']))
    # max_size = max(movie_size)
    # max_size_index = movie_size.index(max_size)
    print(new_file,movie_url)
    # urllib.request.urlretrieve(movie_url,new_file+".mp4")
        


#Create a folder for each user

def makeDIR(name):
            document_path = os.getenv("USERPROFILE") + "/Pictures"
            path = document_path+"/"+name
            if not os.path.exists(path):
                os.mkdir(path)
            os.chdir(path)



Tweet_count = 0
Pic_count = 0
Video_count = 0


#INPUT USER ID

print("---")
print("Please input userid who you want to download")
userId = input(">>>")
print("---")
print("Please input numbers of tweet which you want to check")
limit = input(">>>")
print("---")
print("Now Loading.\nPlease Wait for a moment...")

#create the folder
makeDIR(userId)

# query = "(from:rin_agemon) -filter:replies"
# query = "(from:mayuri_prsm) -filter:replies until:2022-11-23 since:2019-09-01"
# query = "(from:yume_bmhr) -filter:replies until:2022-02-26 since:2021-05-01"
query = "(from:"+userId+") -filter:replies until:2022-10-01 since:2022-09-15"
tweets = []
limits = int(limit)

for tweet in sntwitter.TwitterSearchScraper(query).get_items():

    if len(tweets) == limits:
        break
    else:
        tweets.append([change_name(change_time(tweet.date)),tweet.user.username,tweet.media])
        Tweet_count = Tweet_count + 1
        if tweet.media:
            for medium in tweet.media:
                title =["a","b","c","d"]
                # print(medium)
                if isinstance(medium,sntwitter.Photo):
                    # print(medium)
                    for p in range(len(tweet.media)):
                        # print(title[p],tweet.media[p].fullUrl)
                        Pic_count = Pic_count + 1
                        photo_url = tweet.media[p].fullUrl
                        photo_name = change_name(change_time(tweet.date))+"_"+title[p]+".jpg"
                        urllib.request.urlretrieve(photo_url,photo_name)                    
                    # for i in tweet.media:                        
                    #     print(title[i],tweet.media[i].fullUrl)
                    break
                        
                    # print(medium.previewUrl)
                elif isinstance(medium,sntwitter.Video) or isinstance(medium,sntwitter.Gif):
                    # print(medium.thumbnailUrl)
                    # print(medium.variants)
                    for v in range(len(medium.variants)):
                        # print(title[v],medium.variants[v].url)
                        Video_count = Video_count + 1
                        video_url = medium.variants[v].url
                        video_name = change_name(change_time(tweet.date))+"_"+title[v]+".mp4"
                        urllib.request.urlretrieve(video_url,video_name)

# print(isinstance(tweets[0][2], sntwitter.Video))

df = pd.DataFrame(tweets, columns=['Date','name','media'])

print(df)

print("Task finish.\nTotal checked tweets:{}\nNumber of Downloaded Videos:{}\nNumber of Downloaded Pictures:{}\n".format(Tweet_count,Video_count,Pic_count))

