#!/usr/bin/env python
#reference https://github.com/jesseward/discogs-oauth-example

import json
import sys
from urllib import request
from urllib.parse import parse_qsl

import oauth2 as oauth
import secrettoken as st

# The following oauth end-points are defined by discogs.com staff. These static endpoints
# are called at various stages of oauth handshaking.
request_token_url = "https://api.discogs.com/oauth/request_token"
authorize_url = "https://www.discogs.com/oauth/authorize"
access_token_url = "https://api.discogs.com/oauth/access_token"

# A user-agent is required with Discogs API requests. Be sure to make your user-agent
# unique, or you may get a bad response.
user_agent = "discogs_api_example/1.0"

# create oauth Consumer and Client objects using
consumer = oauth.Consumer(st.customer_key, st.customer_secret)
client = oauth.Client(consumer)

# pass in your consumer key and secret to the token request URL. Discogs returns
# an ouath_request_token as well as an oauth request_token secret.
resp, content = client.request(
    request_token_url, "POST", headers={"User-Agent": user_agent}
)

# we terminate if the discogs api does not return an HTTP 200 OK. Something is
# wrong.
if resp["status"] != "200":
    sys.exit("Invalid response {0}.".format(resp["status"]))

request_token = dict(parse_qsl(content.decode("utf-8")))

print(" == Request Token == ")
print(f'    * oauth_token        = {request_token["oauth_token"]}')
print(f'    * oauth_token_secret = {request_token["oauth_token_secret"]}')
print()

# Authorize our newly received request_token against the discogs oauth endpoint.
# Prompt your user to "accept" the terms of your application. The application
# will act on behalf of their discogs.com account.
# If the user accepts, discogs displays a key to the user that is used for
# verification. The key is required in the 2nd phase of authentication.
print(
    f'Please browse to the following URL {authorize_url}?oauth_token={request_token["oauth_token"]}'
)

# Waiting for user input
accepted = "n"
while accepted.lower() == "n":
    print()
    accepted = input(
        f'Have you authorized me at {authorize_url}?oauth_token={request_token["oauth_token"]} [y/n] :'
    )

# request the verification token from the user.
oauth_verifier = input("Verification code : ")

# Generate objects that pass the verification key with the oauth token and oauth
# secret to the discogs access_token_url
token = oauth.Token(request_token["oauth_token"], request_token["oauth_token_secret"])
token.set_verifier(oauth_verifier)
client = oauth.Client(consumer, token)

resp, content = client.request(
    access_token_url, "POST", headers={"User-Agent": user_agent}
)

# if verification is successful, the discogs oauth API will return an access token
# and access token secret. This is the final authentication phase. You should persist
# the oauth_token and the oauth_token_secret to disk, database or some
# other local store. All further requests to the discogs.com API that require authentication
# and must be made with these access_tokens.
access_token = dict(parse_qsl(content.decode("utf-8")))

print(" == Access Token ==")
print(f'    * oauth_token        = {access_token["oauth_token"]}')
print(f'    * oauth_token_secret = {access_token["oauth_token_secret"]}')
print(" Authentication complete. Future requests must be signed with the above tokens.")
print()


# We're now able to fetch an image using the application consumer key and secret,
# along with the verified oauth token and oauth token for this user.
token = oauth.Token(
    key=access_token["oauth_token"], secret=access_token["oauth_token_secret"]
)
client = oauth.Client(consumer, token)

# With an active auth token, we're able to reuse the client object and request
# additional discogs authenticated endpoints, such as database search.
resp, content = client.request(
    "https://api.discogs.com/database/search?release_title=House+For+All&artist=Blunted+Dummies",
    headers={"User-Agent": user_agent},
)

if resp["status"] != "200":
    sys.exit("Invalid API response {0}.".format(resp["status"]))

releases = json.loads(content.decode("utf-8"))
print("\n== Search results for release_title=House For All, Artist=Blunted Dummies ==")
for release in releases["results"]:
    print(f'\n\t== discogs-id {release["id"]} ==')
    print(f'\tTitle\t: {release.get("title", "Unknown")}')
    print(f'\tYear\t: {release.get("year", "Unknown")}')
    print(f'\tLabels\t: {", ".join(release.get("label", ["Unknown"]))}')
    print(f'\tCat No\t: {release.get("catno", "Unknown")}')
    print(f'\tFormats\t: {", ".join(release.get("format", ["Unknown"]))}')

# In order to download release images, fetch the release data for id=40522
# 40522 = http://www.discogs.com/Blunted-Dummies-House-For-All/release/40522
resp, content = client.request(
    "https://api.discogs.com/releases/40522", headers={"User-Agent": user_agent}
)

if resp["status"] != "200":
    sys.exit("Unable to fetch release 40522")

# load the JSON response content into a dictionary.
release = json.loads(content.decode("utf-8"))
# extract the first image uri.
image = release["images"][0]["uri"]

# The authenticated URL is generated for you. There is no longer a need to
# wrap the image download request in an OAuth signature.
# build, send the HTTP GET request for the desired image.
# DOCS: http://www.discogs.com/forum/thread/410594
try:
    request.urlretrieve(image, image.split("/")[-1])
except Exception as e:
    sys.exit(f"Unable to download image {image}, error {e}")

print(" == API image request ==")
print(f'    * response status      = {resp["status"]}')
print(f'    * saving image to disk = {image.split("/")[-1]}')