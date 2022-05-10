from Mongo import mongo
from Auth.oauth import Oauth
from User.user_detail import *

if __name__ == "__main__":

    db = "tweetrimony"
    collection = "tweeterdata"
    
    screen_name = str(input("Enter the 'screenname' of the person to be matched: "))
    api = Oauth(0).oauth()
    my_user = get_user_profile(api,screenName = screen_name)
    if not my_user.location:
        my_user.profile_location = my_user.location = str(input("Enter your location detail | Eg: Syracuse: "))
        print("User location set, searching nearby...\n")
    #print(user)
    # Get the state of the user
    # Get nearby cities of the user
    places = ['Chicago', 'Houston', 'Dallas', 'Austin', 'Seattle', 'Denver', 'Las Vegas', 'Boston', 'Charlotte',
              'Nashville', 'Atlanta', 'Cleveland', 'Irvine', 'Buffalo', 'Yonkers']
    #geo_users_dump = get_geo_users(api,places,50)
    geo_users_dump = []
    #geo_users_name_filtered = filter_name_geo(geo_users_dump,places)
    #gender_users_filtered = filter_gender(api,geo_users_name_filtered,my_user.screen_name)
    #print(len(gender_users_filtered))
    mongo = mongo.database(db,collection);
    #users = mongo.load_mongo()
    #mongo.save_mongo(gender_users_filtered)
    users = mongo.load_mongo(criteria={'user_gender':'male'})
    #print("Mongo Users1::",users)
    users = sorted(users, key=lambda item: item['user_friends_count'])
    #print("Mongo Users::",users)
    print("Mongo Users::",len(users))
    filtered_friends_ids = filter_friends(api,users[:100],my_user)
    print(len(filtered_friends_ids))
    print("----------")
    print(filtered_friends_ids)
    print("*************end")
    #for user in users:
    #    print(user['user_screen_name'])
    
