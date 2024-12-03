import json
import os

import seatgeek_calls as sg
import spotipy_calls as sp
import ticketmaster_calls as tm


def clean_sg_data():
    with open("../dat/concert_data copy.json", "r") as f:
        data = json.load(f)
        for artist in data:
            print(artist)

    print(data)


if __name__ == "__main__":
    # sp.default_mode()
    top_artists = []
    with open("../dat/spotify_top_artists.json", "r") as spotify_top_artists_json:
        data = json.load(spotify_top_artists_json)
        for artist in data:
            top_artists.append(artist["name"])
        tm.production_mode(top_artists)
    # sg.default_mode()
    # tm.default_mode()
