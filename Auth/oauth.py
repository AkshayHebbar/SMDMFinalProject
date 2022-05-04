import tweepy

def oauth():
    consumer_key = 'bIcIUee01j6hzvNl8GABYRkNw'
    consumer_secret = 'nRgigF5MzKnec4GKJTApQtHxVm8azOrF5DJsmfx007NuCaqJVX'
    OAUTH_TOKEN = '2199301128-R8n4JUQot2w4wwHa4cGGb61V7ZaZ95kIlmdA6Oj'
    OAUTH_TOKEN_SECRET = 'gC3RoazOZ6ZvCVQUCKB2MWi80P9TF7JTbLLLHHQIUB4gL'

    auth = tweepy.OAuthHandler(consumer_key = consumer_key,consumer_secret = consumer_secret)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    return(tweepy.API(auth))
