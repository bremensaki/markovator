# Fill in the blanks below and rename this file twitter_settings.py

import oauth2 as oauth

screen_name='' # Twitter username
token = oauth.Token(key="", secret="") # Twitter users token and secret
consumer = oauth.Consumer(key="", secret="") # Key and secret of the twitter appliction
tweet_chance = 20 # % chance of generating a tweet on any run, set "100" for easy testing