import argparse
import csv
import json
import os
import sys

import requests

# Replace with your Ticketmaster API Key
API_KEY = "IGSONbJBdo7ZbdjgZdXG4glj2wG5MLi3"


def get_artist_attraction_id(artist):
    """Fetch the Ticketmaster attractionId for a specific artist."""
    url = "https://app.ticketmaster.com/discovery/v2/attractions.json"
    params = {"apikey": API_KEY, "keyword": artist}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if "_embedded" in data:
            attractions = data["_embedded"]["attractions"]
            for attraction in attractions:
                if attraction["name"].lower() == artist.lower():
                    return attraction["id"]
        print(f"Attraction ID for {artist} not found.")
        return None
    except requests.RequestException as e:
        print(f"Error fetching artist attraction ID: {e}")
        return None


def get_event_details(event_id):
    url = f"https://app.ticketmaster.com/discovery/v2/events/{event_id}.json"
    params = {"apikey": API_KEY}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def fetch_ticketmaster_data(artist):
    """Fetch concert data for an artist using Ticketmaster API and attractionId."""
    attraction_id = get_artist_attraction_id(artist)
    if not attraction_id:
        print(f"No data found for artist: {artist}")
        return []

    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": API_KEY,
        "attractionId": attraction_id,
        "size": 5,  # Limit to 5 events for simplicity
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if "_embedded" in data:
            events = data["_embedded"]["events"]
            return_list = []
            for event in events:
                event_id = event["id"]
                try:
                    details = get_event_details(event_id)
                    # Build a dictionary for each event with detailed information
                    event_data = {
                        "Artist": artist,
                        "Event": details.get("name", "Unknown Event"),
                        "Venue": details["_embedded"]["venues"][0].get(
                            "name", "Unknown Venue"
                        ),
                        "Location": (
                            f"{details['_embedded']['venues'][0]['city']['name']}, {details['_embedded']['venues'][0]['state']['name']}"
                            if "_embedded" in details
                            and "venues" in details["_embedded"]
                            else "Unknown Location"
                        ),
                        "Date": details["dates"]["start"].get(
                            "localDate", "Unknown Date"
                        ),
                        "Time": details["dates"]["start"].get(
                            "localTime", "Unknown Time"
                        ),
                        "Price Range": (
                            f"{details['priceRanges'][0]['min']} - {details['priceRanges'][0]['max']} {details['priceRanges'][0]['currency']}"
                            if "priceRanges" in details
                            else "Price information not available"
                        ),
                        "Link": details.get("url", "No link available"),
                    }
                    return_list.append(event_data)
                except Exception as e:
                    print(f"Error fetching details for event {event_id}: {e}")
            return return_list
        else:
            print("No events found for the given artist.")
            return []
    except requests.RequestException as e:
        print(f"Error fetching data from Ticketmaster API: {e}")
        return []


def static_mode(dataset_path):
    """Load and print static dataset."""
    try:
        if dataset_path.endswith(".json"):
            with open(dataset_path, "r") as f:
                data = json.load(f)
            print(f"Dataset loaded from {dataset_path}. Total entries: {len(data)}")
            print(json.dumps(data[:5], indent=2))
        elif dataset_path.endswith(".csv"):
            with open(dataset_path, "r") as f:
                reader = csv.reader(f)
                data = list(reader)
            print(f"Dataset loaded from {dataset_path}. Total rows: {len(data)}")
            print(data[:5])
        else:
            print("Unsupported file format. Please provide a .json or .csv file.")
    except Exception as e:
        print(f"Error loading dataset: {e}")


def scrape_mode(artist):
    """Fetch data from Ticketmaster API and print sample."""
    print(f"Fetching data for artist: {artist}...")
    events = fetch_ticketmaster_data(artist)
    if events:
        print(f"Sample data for {artist}:")
        print(json.dumps(events[:5], indent=2))


def default_mode(artist):
    """Fetch data, save it to a static file, and print a sample."""
    # artist = "Taylor Swift"
    print(f"\nFetching and saving data from ticketmaster for artist: {artist}...")
    events = fetch_ticketmaster_data(artist)
    if events:
        # Ensure the 'dat' directory exists
        dat_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir, "dat"))
        os.makedirs(
            dat_directory, exist_ok=True
        )  # Create 'dat' directory if it doesn't exist
        output_file = os.path.join(dat_directory, "ticketmaster_data.json")
        with open(output_file, "w") as f:
            json.dump(events, f)
        print(f"Data saved to {output_file}.")
        print(f"Total entries: {len(events)}. Sample data:")
        print(json.dumps(events[:5], indent=2))
    else:
        print("No data to save.")


def production_mode(artists):
    """
    Fetch data for multiple artists, save to a single output file.
    Should not be callable by command line.
    """
    print(f"\nFetching and saving data for {len(artists)} artists...")

    # Ensure the 'dat' directory exists
    dat_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir, "dat"))
    os.makedirs(dat_directory, exist_ok=True)

    output_file = os.path.join(dat_directory, "ticketmaster_data.json")
    all_events = []

    for artist in artists:
        print(f"Fetching data for artist: {artist}...")
        events = fetch_ticketmaster_data(artist)
        if events:
            all_events.extend(events)
            print(f"Added {len(events)} events for {artist}")
        else:
            print(f"No data found for {artist}")

    if all_events:
        with open(output_file, "w") as f:
            json.dump(all_events, f, indent=2)
        print(f"\nData saved to {output_file}.")
        print(f"Total entries: {len(all_events)}. Sample data:")
        print(json.dumps(all_events[:5], indent=2))
    else:
        print("No data to save.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HW4 Script using Ticketmaster API.")
    parser.add_argument(
        "--static", type=str, help="Path to static dataset for static mode."
    )
    parser.add_argument("--scrape", type=str, help="Artist name for scrape mode.")
    args = parser.parse_args()

    if args.static:
        static_mode(args.static)
    elif args.scrape:
        scrape_mode(args.scrape)
    else:
        default_mode()
