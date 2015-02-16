import json

import oauth2 as oauth

import urllib


class TwitterError(Exception):
    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content

    def __str__(self):
        return "Twitter returned " + str(self.status_code) + " " + self.content


def auth_client(consumer_key, consumer_secret, token_key, token_secret):
    try:
        consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
        token = oauth.Token(key=token_key, secret=token_secret)
        client = oauth.Client(consumer, token)

        resp, content = client.request("https://api.twitter.com/1.1/account/verify_credentials.json?include_entities=false&skip_status=true", "GET")
        if resp.status != 200:
            raise TwitterError(resp.status, content)
    except TwitterError, e:
        print "Authentication failure: %s" % e
        return False

    return client


def get_mentions(client, since=-1):
    if since > -1:
        resp, content = client.request(
            "https://api.twitter.com/1.1/statuses/mentions_timeline.json?count=800&since_id=" + str(since), "GET")
    else:
        resp, content = client.request("https://api.twitter.com/1.1/statuses/mentions_timeline.json?count=200", "GET")

    if resp.status != 200:
        raise TwitterError(resp.status, content)

    return json.loads(content)


def get_tweets(client, screen_name):
    resp, content = client.request(
        'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=' + screen_name + '&count=800&trim_user=true',
        "GET")

    if resp.status != 200:
        raise TwitterError(resp.status, content)

    return json.loads(content)


def get_timeline_tweets(client, count):
    resp, content = client.request('https://api.twitter.com/1.1/statuses/home_timeline.json?count=' + str(count), "GET")

    if resp.status != 200:
        raise TwitterError(resp.status, content)

    return json.loads(content)


def get_search_tweets(client, count, query):
    resp, content = client.request(
        'https://api.twitter.com/1.1/search/tweets.json?q=' + urllib.quote(query) + '&count=' + str(count), "GET")

    if resp.status != 200:
        raise TwitterError(resp.status, content)

    return json.loads(content)


def get_timeline_tweets_since(client, since_id=-1):
    tweets = []

    if since_id < 0:
        resp, content = client.request('https://api.twitter.com/1.1/statuses/home_timeline.json', "GET")

        if resp.status != 200:
            raise TwitterError(resp.status, content)

        tweets.extend(json.loads(content))
    else:
        # TODO 1 or 0?
        current_page = 0
        while len(tweets) == 0 or not since_id >= max(map(lambda t: int(t['id']), tweets)):
            resp, content = client.request(
                'https://api.twitter.com/1.1/statuses/home_timeline.json?count=800&page=' + str(current_page), "GET")
            new_tweets = json.loads(content)
            if len(new_tweets) == 0:
                break
            tweets.extend(new_tweets)
            current_page += 1

    return tweets


def post_tweet(client, text, reply_to_id=-1):
    # TODO only include reply_to_id if replying
    resp, content = client.request("https://api.twitter.com/1.1/statuses/update.json", "POST",
            urllib.urlencode([("status", unicode(text).encode('utf-8')),
                              ("in_reply_to_status_id", unicode(reply_to_id).encode('utf-8')),
                              ]))

    # TODO Check status code

    return content


def follow_user(client, screen_name):
    resp, content = client.request("https://api.twitter.com/1.1/friendships/create.json", "POST",
                                   urllib.urlencode([("screen_name", screen_name)]))

    # TODO Check status code

    return content


def get_rate_limit_status(client):
    resp, content = client.request('https://api.twitter.com/1.1/application/rate_limit_status.json', "GET")

    return json.loads(content)
