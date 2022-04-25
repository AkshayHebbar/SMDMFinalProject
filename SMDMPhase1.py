import pymongo
import tweepy
import time
import nltk
import json
import pandas as pd
from pymongo import MongoClient
from urllib.request import urlopen



def oauth():
    consumer_key = ''
    consumer_secret = ''
    OAUTH_TOKEN = ''
    OAUTH_TOKEN_SECRET = ''

    auth = tweepy.OAuthHandler(consumer_key = consumer_key,consumer_secret = consumer_secret)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    return(tweepy.API(auth))

def connect_mongo():
    client = pymongo.MongoClient("mongodb+srv://tweetrimony:SMDMProj123@cluster0.ypbt0.mongodb.net/"
                                 "tweetrimony?retryWrites=true&w=majority")
    db = client.test
    print(db)
    return db

def get_users(api,cities,itr):
    geo_users = []
    depth = 1
    for i in cities:
        while depth <= itr:
            try:
                geo_users.extend(api.search_users(q = i, page = depth))
                print(len(geo_users))
            except tweepy.errors.TooManyRequests:
                print("Too many requests")
                time.sleep(1000)
            except tweepy.errors.Unauthorized:
                print("experencing 401 error")
            except tweepy.errors.TwitterServerError:
                print("experencing 503 error")
            except tweepy.errors.BadRequest:
                print("experencing 400 error")
            depth += 1
        depth = 1
    return geo_users


def valid_users(geo_user,cities):
    last_name = pd.read_csv(r'<pathname>/Common_Surnames_Census_2000.csv')
    first_name = pd.read_excel(r'<pathname>/SSA_Names_DB.xlsx')
    last_name_users = pd.DataFrame(last_name, columns = ['name'])
    first_name_users = pd.DataFrame(first_name, columns = ['Name'])

    geo_user_name_filtered = []
    geo_dump = []
    for city in range(len(cities)):
        for user in range(len(geo_user)):
            if cities[city].casefold() in geo_user[user].name.casefold():
                geo_dump.append(geo_user[user])

    for user in geo_user:
        if user not in geo_dump:
            fields = user.name.split(" ")
            if len(fields) == 3 or len(fields) == 2:
                user_first = fields[0]
                user_second = fields[1]
                if user_first in first_name_users.values:
                    if user_second.upper() in last_name_users.values:
                        geo_user_name_filtered.append(user)
            else:
                user_first = fields[0]
                if user_first.upper() in first_name_users.values:
                    geo_user_name_filtered.append(user)

    return geo_user_name_filtered

def user_gender(users,screen_name):
    final_user = []
    myKey = ""


    main_user = api.get_user(screen_name = screen_name)
    first_name = main_user.name.split(" ")[0]

    url = "https://gender-api.com/get?key=" + myKey + "&name=" + first_name.upper()
    response = urlopen(url)
    decoded = response.read().decode('utf-8')
    data = json.loads(decoded)
    main_user_gender = data["gender"]

    for user in users:
        #fields = user.name.split(" ")
        user_first = user.name.split(" ")[0]
        url = "https://gender-api.com/get?key=" + myKey + "&name=" + user_first.upper()
        response = urlopen(url)
        decoded = response.read().decode('utf-8')
        data = json.loads(decoded)
        if data["gender"] != main_user_gender:
            final_user.append(user)

    return final_user


def load_mongodb(users):
    client = pymongo.MongoClient("mongodb+srv://tweetrimony:abhishek@cluster0.ypbt0.mongodb.net/myFirstDatabase?"
                                 "retryWrites=true&w=majority")
    db = client["tweetrimony"]
    col = db["tweeterdata"]

    user_details = {}
    for i in users:
        try:
            user_details = {"user_id" : i.id,"user_id_str" : i.id_str,"user_name" : i.name,"user_screen_name" : i.screen_name,
                        "user_location" : i.location,"user_description" : i.description,"user_follower_count": i.followers_count,
                        "user_friends_count" : i.friends_count, "user_listed_count" : i.listed_count,
                        "user_count_creation" : i.created_at,"user_fav_count" : i.favourites_count,
                        "user_statuses_count" :i.statuses_count,"user_lang" : i.lang,
                        "user_profile_background_image_url" : i.profile_background_image_url,
                        "user_profile_image_url" : i.profile_image_url}
            x = col.insert_one(user_details)
        except pymongo.errors.ServerSelectionTimeoutError:
            print("pymongo.errors.ServerSelectionTimeoutError")


if __name__ == "__main__":
    api = oauth()
    screen_name = 'edmundyu1001'
    places = ['Chicago', 'Houston', 'Dallas', 'Austin', 'Seattle', 'Denver', 'Las Vegas', 'Boston', 'Charlotte',
              'Nashville', 'Atlanta', 'Cleveland', 'Irvine', 'Buffalo', 'Yonkers']
    geo_users_dump = get_users(api,places,50)
    geo_users_name_filtered = valid_users(geo_users_dump,places)
    final_users = user_gender(geo_users_name_filtered,screen_name)
    print(len(final_users))
    load_mongodb(final_users)
