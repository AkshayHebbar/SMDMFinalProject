from Mongo import mongo
from Auth.oauth import oauth
from User.user_detail import *

if __name__ == "__main__":

    db = "tweetrimony"
    collection = "tweeterdata"
    
    api = oauth()
    screen_name = str(input("Enter the 'screenname' of the person to be matched: "))
    print("\n")
    user_profile = get_user_profile(api,screenName = screen_name)
    if not user_profile.location:
        user_profile.profile_location = user_profile.location = str(input("Enter your location detail | Eg: Syracuse: "))
        print("User location set, searching nearby...\n")
    #print(user)
    # Get the state of the user
    # Get nearby cities of the user
    places = ['Chicago', 'Houston', 'Dallas', 'Austin', 'Seattle', 'Denver', 'Las Vegas', 'Boston', 'Charlotte',
              'Nashville', 'Atlanta', 'Cleveland', 'Irvine', 'Buffalo', 'Yonkers']
    #geo_users_dump = get_geo_users(api,places,50)
    #geo_users_name_filtered = filter_name_geo(geo_users_dump,places)
    #gender_users_filtered = filter_gender(api,geo_users_name_filtered,screen_name)
    #print(len(gender_users_filtered))
    mongo = mongo.database(db,collection);
    print(mongo.load_mongo())
    #mongo.save_mongo(gender_users_filtered)
    
    
