import json
import time
import tweepy
import pandas as pd
from urllib.request import urlopen

def get_geo_users(api,cities,itr):
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

def filter_name_geo(geo_user,cities):
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


def filter_gender(api,users,screen_name):
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

def get_user_profile(api,screenName=None, userId=None):   
    return api.get_user(user_id = userId,screen_name = screenName)
    
        
