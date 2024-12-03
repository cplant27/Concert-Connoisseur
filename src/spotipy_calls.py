import argparse
import json
import os

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials


def static_mode(dataset_path):
    """Load and print static dataset."""
    try:
        with open(dataset_path, "r") as f:
            data = json.load(f)
        print(f"Dataset loaded from {dataset_path}. Total entries: {len(data)}")
        print(json.dumps(data[:5], indent=2))
    except Exception as e:
        print(f"Error loading dataset: {e}")


def scrape_mode():
    """Perform API request and print sample data."""
    username = os.getlogin()
    try:
        token = util.prompt_for_user_token(
            username,
            scope=["user-top-read"],
        )
    except:
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(
            username,
            scope=["user-top-read"],
        )
    spotify_object = spotipy.Spotify(auth=token)
    top_artists = spotify_object.current_user_top_artists(limit=5)["items"]

    print("Sample of Top 5 Artists:")
    for i, artist in enumerate(top_artists, start=1):
        print(f"{i}. {artist['name']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spotify Data Analysis Script")
    parser.add_argument("--static", type=str, help="Path to static dataset")
    parser.add_argument(
        "--scrape", action="store_true", help="Scrape data from Spotify API"
    )
    args = parser.parse_args()

    if args.static:
        static_mode(args.static)
    elif args.scrape:
        scrape_mode()
    else:
        default_mode()
