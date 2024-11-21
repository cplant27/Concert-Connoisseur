import sys
import argparse
import json
import requests
import os
import csv

# Replace with your Ticketmaster API Key
API_KEY = "IGSONbJBdo7ZbdjgZdXG4glj2wG5MLi3"

def fetch_ticketmaster_data(artist):
    """Fetch concert data for an artist using Ticketmaster API."""
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": API_KEY,
        "keyword": artist,
        "size": 5  # Limit to 5 events for simplicity
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if "_embedded" in data:
            events = data["_embedded"]["events"]
            return [
                {
                    "name": event.get("name", "N/A"),
                    "url": event.get("url", "N/A"),
                    "date": event["dates"]["start"].get("localDate", "N/A"),
                }
                for event in events
            ]
        else:
            print("No events found for the given artist.")
            return []
    except requests.RequestException as e:
        print(f"Error fetching data from Ticketmaster API: {e}")
        return []

def static_mode(dataset_path):
    """Load and print static dataset."""
    try:
        if dataset_path.endswith('.json'):
            with open(dataset_path, "r") as f:
                data = json.load(f)
            print(f"Dataset loaded from {dataset_path}. Total entries: {len(data)}")
            print(json.dumps(data[:5], indent=2))
        elif dataset_path.endswith('.csv'):
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

def default_mode():
    """Fetch data, save it to a static file, and print a sample."""
    artist = "Taylor Swift" 
    print(f"Fetching and saving data for artist: {artist}...")
    events = fetch_ticketmaster_data(artist)
    if events:
        # Ensure the 'dat' directory exists
        dat_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir, "dat"))
        os.makedirs(dat_directory, exist_ok=True)  # Create 'dat' directory if it doesn't exist
        output_file = os.path.join(dat_directory, "ticketmaster_data.json")
        with open(output_file, "w") as f:
            json.dump(events, f)
        print(f"Data saved to {output_file}.")
        print(f"Total entries: {len(events)}. Sample data:")
        print(json.dumps(events[:5], indent=2))
    else:
        print("No data to save.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HW4 Script using Ticketmaster API.")
    parser.add_argument("--static", type=str, help="Path to static dataset for static mode.")
    parser.add_argument("--scrape", type=str, help="Artist name for scrape mode.")
    args = parser.parse_args()

    if args.static:
        static_mode(args.static)
    elif args.scrape:
        scrape_mode(args.scrape)
    else:
        default_mode()
