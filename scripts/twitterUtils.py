import twitter

def getApi(keys):
    api = twitter.Api(consumer_key = keys.consumer_key,
                       consumer_secret = keys.consumer_secret,
                       access_token_key = keys.access_token,
                       access_token_secret = keys.access_token_secret)
    return api