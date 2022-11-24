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




#関数:　UTCをJSTに変換する
def change_time(utc_time):
    #イギリスのtimezoneを設定するために再定義する
    # utc_time = datetime(u_time.year, u_time.month,u_time.day, \
    # u_time.hour,u_time.minute,u_time.second, tzinfo=timezone.utc)
    #タイムゾーンを日本時刻に変換
    jst_time = utc_time.astimezone(pytz.timezone("Asia/Tokyo"))
    # 文字列で返す
    str_time = jst_time.strftime("%Y-%m-%d_%H:%M:%S")
    return str_time

#ファイル名をツイート日時（日本時間）に設定
def change_name(date):
    date_modify = re.sub("\:| ", "", date)
    date_modify1 = re.sub("-", "_", date_modify)
    return date_modify1


#画像ダウンロード--複数枚対応
def picDL(check_url):
    new_file = tweets[j][0]
    title =["a","b","c","d"]
    for i in range(len(check_url)):
        image_url = check_url[i].fullUrl
        # urllib.request.urlretrieve(image_url,new_file+"_"+title[i]+".jpg")
        print(image_url)


#動画ダウンロード--すべてのgifおよび動画をmp4形式で保存
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
        


#ユーザーごとにフォルダを作成
def makeDIR(name):
            document_path = os.getenv("USERPROFILE") + "/Pictures"
            path = document_path+"/"+name
            if not os.path.exists(path):
                os.mkdir(path)
            os.chdir(path)



Tweet_count = 0
Pic_count = 0
Video_count = 0


# query = "(from:rin_agemon) -filter:replies"
# query = "(from:mayuri_prsm) -filter:replies until:2022-11-23 since:2019-09-01"
# query = "(from:yume_bmhr) -filter:replies until:2022-02-26 since:2021-05-01"
query = "(from:yume_bmhr) -filter:replies until:2021-10-16 since:2021-05-01"
tweets = []
limit = 20

#フォルダの作成
# makeDIR("yume")


for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    # json.loads(vars(tweet).['content'])
    # print(vars(tweet))
    # break
    if len(tweets) == limit:
        break
    else:
        tweets.append([change_name(change_time(tweet.date)),tweet.user.username,tweet.media])
        if tweet.media:
            for medium in tweet.media:
                # print(medium)
                if isinstance(medium,sntwitter.Photo):
                    # print(medium)
                    print(medium.fullUrl)
                    # print(medium.previewUrl)
                elif isinstance(medium,sntwitter.Video):
                    # print(medium.thumbnailUrl)
                    # print(medium.variants)
                    for v in medium.variants:
                        print(v.url)

# print(isinstance(tweets[0][2], sntwitter.Video))

# df = pd.DataFrame(tweets, columns=['Date','name','media'])

# print(df)









#  df.to_csv("tw_yume.csv",encoding='utf-8-sig')

# for j in trange(len(tweets)):
#     Tweet_count = Tweet_count + 1
#     if "Photo" in str(tweets[j][2]):  #图片
#         Pic_count = Pic_count + len(tweets[j][2])
#         picDL(tweets[j][2])
#         # continue

#     elif "Video" in str(tweets[j][2]):  #动画
#         Video_count = Video_count + 1
#         movieDL(tweets[j][2])
#         # continue
#     else:
#         print(">")
#         # continue

# print("处理结束。\n共检查推文数:{}\n下载视频数:{}\n下载图片数:{}\n".format(Tweet_count,Video_count,Pic_count))