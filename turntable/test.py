import pandas as pd
from textblob import TextBlob
import numpy as np
from datetime import datetime
# from xgboost import XGBRegressor
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# import sklearn.metrics as m
# from sklearn.preprocessing import OneHotEncoder
import nltk, sys, json
import discogs_client
from urllib import request
from urllib.parse import parse_qsl
from urllib.parse import urlparse
import oauth2 as oauth

data = pd.read_csv('Record-Collection.csv')
consumer_key = 'FdxaljOTWBmKXCysYsQZ'
consumer_secret = 'lrfQIsgQonpeUnEuLWRpJgWKLdhKMaYe'
request_token_url = 'https://api.discogs.com/oauth/request_token'
authorize_url = 'https://www.discogs.com/oauth/authorize'
access_token_url = 'https://api.discogs.com/oauth/access_token'
user_agent = 'discogs_api_example/1.0'
consumer = oauth.Consumer(consumer_key, consumer_secret)
client = oauth.Client(consumer)
resp, content = client.request(request_token_url, 'POST', headers={'User-Agent': user_agent})
if resp['status'] != '200':
    sys.exit('Invalid response {0}.'.format(resp['status']))
request_token = dict(parse_qsl(content.decode('utf-8')))

print(' == Request Token == ')
print(f'    * oauth_token        = {request_token["oauth_token"]}')
print(f'    * oauth_token_secret = {request_token["oauth_token_secret"]}')
print()
print(f'Please browse to the following URL {authorize_url}?oauth_token={request_token["oauth_token"]}')

# Waiting for user input
accepted = 'n'
while accepted.lower() == 'n':
    print()
    accepted = input(f'Have you authorized me at {authorize_url}?oauth_token={request_token["oauth_token"]} [y/n] :')
oauth_verifier = input('Verification code : ')

# Generate objects that pass the verification key with the oauth token and oauth
# secret to the discogs access_token_url
token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
token.set_verifier(oauth_verifier)
client = oauth.Client(consumer, token)

resp, content = client.request(access_token_url, 'POST', headers={'User-Agent': user_agent})
access_token = dict(parse_qsl(content.decode('utf-8')))

print(' == Access Token ==')
print(f'    * oauth_token        = {access_token["oauth_token"]}')
print(f'    * oauth_token_secret = {access_token["oauth_token_secret"]}')
print(' Authentication complete. Future requests must be signed with the above tokens.')
print()

token = oauth.Token(key=access_token['oauth_token'],
        secret=access_token['oauth_token_secret'])
client = oauth.Client(consumer, token)

# With an active auth token, we're able to reuse the client object and request
# additional discogs authenticated endpoints, such as database search.

artist_ = 'Jade Cicada'
title_ = 'Brood VII'

resp, content = client.request('https://api.discogs.com/database/search?release_title='+title_.replace(" ",'+')+'&artist='+artist_.replace(" ",'+'),
        headers={'User-Agent': user_agent})

if resp['status'] != '200':
    sys.exit('Invalid API response {0}.'.format(resp['status']))

releases = json.loads(content.decode('utf-8'))
print('\n== Search results for release_title= ' + title_ + ', Artist= ' + artist_ + ' ==')
x = 0
for release in releases['results']:
    print(f'\n\t== discogs-id {release["id"]} ==')
    if x == 0: 
        id_ = {release["id"]}
        print({release["id"]})
    print(f'\tTitle\t: {release.get("title", "Unknown")}')
    print(f'\tYear\t: {release.get("year", "Unknown")}')
    print(f'\tLabels\t: {", ".join(release.get("label", ["Unknown"]))}')
    print(f'\tCat No\t: {release.get("catno", "Unknown")}')
    print(f'\tFormats\t: {", ".join(release.get("format", ["Unknown"]))}')

resp, content = client.request('https://api.discogs.com/releases/' + str(id_).replace("{","").replace("}",""),
        headers={'User-Agent': user_agent})

if resp['status'] != '200':
    sys.exit('Unable to fetch release 40522')

# load the JSON response content into a dictionary.
release = json.loads(content.decode('utf-8'))
# extract the first image uri.
image = release['images'][0]['uri']

# The authenticated URL is generated for you. There is no longer a need to
# wrap the image download request in an OAuth signature.
# build, send the HTTP GET request for the desired image.
# DOCS: http://www.discogs.com/forum/thread/410594
try:
    request.urlretrieve(image, image.split('/')[-1])
except Exception as e:
    sys.exit(f'Unable to download image {image}, error {e}')

print(' == API image request ==')
print(f'    * response status      = {resp["status"]}')
print(f'    * saving image to disk = {image.split("/")[-1]}')