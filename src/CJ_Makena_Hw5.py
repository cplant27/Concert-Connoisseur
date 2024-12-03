import json
import os

import seatgeek_calls as sg
import spotipy_calls as sp
import ticketmaster_calls as tm


def scrape_data():
    sp.default_mode()
    top_artists = []
    with open("../dat/spotify_top_artists.json", "r") as spotify_top_artists_json:
        data = json.load(spotify_top_artists_json)
        for artist in data:
            top_artists.append(artist["name"])
        tm.production_mode(top_artists)
        for artist in top_artists:
            sg.default_mode(artist)


def display_paginated_events(json_file, mode, page_size=5):
    """
    Display events from a JSON file in a paginated format.
    :param json_file: Path to the JSON file containing events.
    :param mode: Determines the JSON format (True for list of events, False for 'concerts' format).
    :param page_size: Number of events to display per page.
    """
    try:
        with open(json_file, "r") as f:
            data = json.load(f)

        if mode:
            # Handle list of events format
            if not isinstance(data, list):
                print("Error: JSON file should contain a list of events.")
                return

            total_events = len(data)
            if total_events == 0:
                print("No events found in the file.")
                return

            current_page = 0
            while True:
                start = current_page * page_size
                end = start + page_size
                page_events = data[start:end]

                if not page_events:
                    print("\nNo more events to display.")
                    break

                print(
                    f"\nShowing events {start + 1} to {min(end, total_events)} of {total_events}:\n"
                )

                for idx, event in enumerate(page_events, start=start + 1):
                    print(
                        f"{idx}. {event['Artist']} at {event['Venue']}, {event['Location']}"
                    )
                    print(f"    Date: {event['Date']}, Time: {event['Time']}")
                    print(f"    Price Range: {event['Price Range']}")
                    print(f"    Link: {event['Link']}\n")

                if end >= total_events:
                    print("End of events.")
                    break

                user_input = (
                    input("Enter 'n' for next page, 'q' to quit: ").strip().lower()
                )
                if user_input == "n":
                    current_page += 1
                elif user_input == "q":
                    break
                else:
                    print("Invalid input. Exiting.")
                    break
        else:
            # Handle 'concerts' format
            if "concerts" not in data or "artist" not in data:
                print("Error: JSON file does not match the expected 'concerts' format.")
                return

            concerts = data["concerts"]
            total_concerts = len(concerts)

            if total_concerts == 0:
                print("No concerts found in the file.")
                return

            current_page = 0
            while True:
                start = current_page * page_size
                end = start + page_size
                page_concerts = concerts[start:end]

                if not page_concerts:
                    print("\nNo more concerts to display.")
                    break

                print(
                    f"\nShowing concerts {start + 1} to {min(end, total_concerts)} of {total_concerts}:\n"
                )

                for idx, concert in enumerate(page_concerts, start=start + 1):
                    print(f"{idx}. {data['artist']} at {concert['location']}")
                    print(f"    Date: {concert['date']}, Time: {concert['time']}")
                    print(f"    Link: {concert['link']}\n")

                if end >= total_concerts:
                    print("End of concerts.")
                    break

                user_input = (
                    input("Enter 'n' for next page, 'q' to quit: ").strip().lower()
                )
                if user_input == "n":
                    current_page += 1
                elif user_input == "q":
                    break
                else:
                    print("Invalid input. Exiting.")
                    break

    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found.")
    except json.JSONDecodeError:
        print("Error: File is not a valid JSON format.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    scrape = False
    if scrape:
        scrape_data()

    tm_or_sg = input(
        "\nWould you like to see events from Ticketmaster or Seatgeek? (tm/sg):"
    )
    if tm_or_sg == "tm":
        display_paginated_events("../dat/ticketmaster_data.json", True)

    elif tm_or_sg == "sg":
        display_paginated_events("../dat/seatgeek_data.json", False)
