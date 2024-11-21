import os

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

print("\n")

username = os.getlogin()

# User ID: wpia9ov4me8c4k0jd1mqsydf0?si=160319f9c8154fce

try:
    token = util.prompt_for_user_token(
        username,
        scope=[
            "user-top-read",
        ],
    )
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(
        username,
        scope=[
            "user-top-read",
        ],
    )

spotifyObject = spotipy.Spotify(auth=token)

user = spotifyObject.current_user()

displayName = user["display_name"]
limit = 50
print("{}'s Top {} Artists\n\n".format(displayName, limit))

top_artists = spotifyObject.current_user_top_artists(limit)["items"]

for i in range(limit):
    num = i + 1
    print("{}. {}".format(num, top_artists[i]["name"]))
