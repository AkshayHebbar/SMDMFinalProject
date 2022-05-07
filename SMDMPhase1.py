import pymongo
import tweepy
import time
import json
import pandas as pd
from urllib.request import urlopen


def oauth():
    consumer_key = 'IZfjQgPPaxGrYuqse8vPFIzNb'
    consumer_secret = 'vAWar1aANpFzTqY38TJJnwUG35u6zJcB7KOcuiKWqHcixkBzYV'
    OAUTH_TOKEN = '1504625808547188740-CjzhumBAl5laBgEr9dTUfCamOUcqsC'
    OAUTH_TOKEN_SECRET = 'rbEmQ8Jj8MuZZOpqyel7dUEG1R5jQqYlqQdVEjAaEMDVY'

    auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    return tweepy.API(auth)


def get_users(api, cities, max_pages):
    geo_users = []
    depth = 1
    for i in cities:
        while depth <= max_pages:
            try:
                geo_users.extend(api.search_users(q=i, page=depth))
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


def valid_users(geo_user, cities):
    last_name = pd.read_csv(r'/Users/abhishekteli/Downloads/Common_Surnames_Census_2000.csv')
    first_name = pd.read_excel(r'/Users/abhishekteli/Downloads/SSA_Names_DB.xlsx')
    last_name_users = pd.DataFrame(last_name, columns=['name'])
    first_name_users = pd.DataFrame(first_name, columns=['Name'])

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


def user_gender(users, screen_name):
    final_user = []
    myKey = "dac3d3a6b47e6ffb3d90162526e0f123"

    main_user = api.get_user(screen_name = screen_name)
    first_name = main_user.name.split(" ")[0]

    url = "https://gender-api.com/get?key=" + myKey + "&name=" + first_name.upper()
    response = urlopen(url)
    decoded = response.read().decode('utf-8')
    data = json.loads(decoded)
    main_user_gender = data["gender"]

    for user in users:
        user_first = user.name.split(" ")[0]
        url = "https://gender-api.com/get?key=" + myKey + "&name=" + user_first.upper()
        response = urlopen(url)
        decoded = response.read().decode('utf-8')
        data = json.loads(decoded)
        if data["gender"] != main_user_gender:
            final_user.append(user)

    return final_user


def load_mongodb(users):
    client = pymongo.MongoClient("mongodb+srv://tweetrimony:abhishek@cluster0.ypbt0.mongodb.net/tweetrimony?"
                                 "retryWrites=true&w=majority")
    db = client["tweetrimony"]
    col = db["tweeterdata"]

    myKey = "c8b0406344bf5704fb8b879a8d09e2a3"
    user_details = {}
    for i in users:
        user_first = i.name.split(" ")[0]
        url = "https://gender-api.com/get?key=" + myKey + "&name=" + user_first.upper()
        response = urlopen(url)
        decoded = response.read().decode('utf-8')
        data = json.loads(decoded)
        users_gender = data["gender"]
        user_details = {"user_id" : i.id,"user_id_str": i.id_str,"user_name": i.name,"user_screen_name": i.screen_name,
                        "user_location": i.location,"user_gender": users_gender, "user_description": i.description,
                        "user_follower_count": i.followers_count,"user_friends_count": i.friends_count,
                        "user_listed_count": i.listed_count,"user_count_creation": i.created_at,
                        "user_fav_count": i.favourites_count,
                        "user_statuses_count": i.statuses_count,"user_lang": i.lang,
                        "user_profile_background_image_url": i.profile_background_image_url,
                        "user_profile_image_url": i.profile_image_url}
        x = col.insert_one(user_details)


if __name__ == "__main__":
    api = oauth()
    screen_name = 'edmundyu1001'
    places = ['Winston–Salem','Chesapeake','Glendale','Garland','Scottsdale','Norfolk','Boise','Fremont','Spokane',
              'Santa Clarita','Baton Rouge','Richmond','Fremont','Boise','Salt Lake City','Syracuse']

    geo_users_dump = get_users(api,places,50)
    geo_users_name_filtered = valid_users(geo_users_dump,places)
    load_mongodb(geo_users_name_filtered)


# ['Chicago', 'Houston', 'Dallas', 'Austin', 'Seattle', 'Denver', 'Las Vegas', 'Boston', 'Charlotte',
# 'Nashville', 'Atlanta', 'Cleveland', 'Irvine', 'Buffalo', 'Yonkers',]

# ['Los Angeles','Phoenix','Philadelphia','San Antonio','San Diego','San Jose','Jacksonville','Fort Worth',
# 'Columbus','Indianapolis','San Francisco','Seattle','Washington','Oklahoma City','El Paso']

# ['Portland','Detroit','Memphis','Louisville','Baltimore','Milwaukee','Albuquerque','Tucson','Fresno',
# 'Sacramento','Kansas City','Mesa','Omaha','Colorado Springs','Raleigh']

# ['Long Beach','Virginia Beach','Miami','Oakland','Minneapolis','Tulsa','Bakersfield','Wichita','Arlington',
#  'Aurora','Tampa','New Orleans','Honolulu','Anaheim','Lexington']

# ['Stockton','Corpus Christi','Henderson','Riverside','Newark','Saint Paul','Santa Ana','Cincinnati',
#  'Orlando','Pittsburgh','St. Louis','Greensboro','Jersey City','Anchorage','Lincoln']

# ['Plano','Durham','Chandler','Chula Vista','Toledo','Madison','Gilbert','Reno','Fort Wayne','North Las Vegas',
# 'St. Petersburg','Lubbock','Irving','Laredo'] - 29c785591b5f01c069693ee033cf715e

# ['Winston–Salem','Chesapeake','Glendale','Garland','Scottsdale','Norfolk','Boise','Fremont','Spokane',
# 'Santa Clarita','Baton Rouge','Richmond','Fremont','Boise','Salt Lake City','Syracuse']
# - c8b0406344bf5704fb8b879a8d09e2a3


