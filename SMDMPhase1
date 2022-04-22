import pymongo
import tweepy
import time
import nltk

def mongocon():
    client = pymongo.MongoClient("mongodb+srv://tweetrimony:SMDMProj123@cluster0.ypbt0.mongodb.net/tweetrimony?"
                                 "retryWrites=true&w=majority")
    db = client['tweetrimony']
    col = db['tweeter data']
    return col

def OAUTH():
    consumer_key = 'IZfjQgPPaxGrYuqse8vPFIzNb'
    consumer_secret = 'vAWar1aANpFzTqY38TJJnwUG35u6zJcB7KOcuiKWqHcixkBzYV'
    OAUTH_TOKEN = '1504625808547188740-CjzhumBAl5laBgEr9dTUfCamOUcqsC'
    OAUTH_TOKEN_SECRET = 'rbEmQ8Jj8MuZZOpqyel7dUEG1R5jQqYlqQdVEjAaEMDVY'

    auth = tweepy.OAuthHandler(consumer_key = consumer_key,consumer_secret = consumer_secret)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    return(tweepy.API(auth))

#def gender_users(geo_users):



def user_same_location(api,screenname,itr):
    depth = 51
    #geo_users = []
    #same_location_user = []
    user = api.get_user(screen_name = screenname)
    location = user.location
    fields = location.split(",")
    if len(fields) == 3:
        user_location = fields[1]
    elif len(fields) == 2:
        user_location = fields[0]
    else:
        user_location = location
    print(user_location)
    geo_users = api.search_users(q = user_location, page = depth)
    while depth <= itr:
        depth += 1
        try:
            geo_users.extend(api.search_users(q = user_location, page = depth))
            print(len(geo_users))
        except tweepy.errors.TooManyRequests:
            time.sleep(1000)
        except tweepy.errors.Unauthorized:
            print("experencing 401 error")
        except tweepy.errors.TwitterServerError:
            print("experencing 503 error")
        except tweepy.errors.BadRequest:
            print("experencing 400 error")
    return geo_users

def load_mongodb(col,users):
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
            time.sleep(500)

if  __name__  ==  "__main__":
    api = OAUTH()
    collection = mongocon()
    screen_name = 'klrahul11'
    geo_users = user_same_location(api,screen_name,60)
    for i in geo_users:
        print(i.screen_name)
    #load_mongodb(collection,geo_users)
