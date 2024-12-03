import argparse
import json
import os
import sys

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

import seatgeek_format as sgf


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
    """Perform request and print sample data."""
    artist = artist.lower().replace(" ", "-")
    url = f"https://seatgeek.com/{artist}-tickets"

    print(f"Scraping and saving data for artist: {artist}...")
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(10)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    concert_links = []
    for a_tag in soup.find_all(
        "a", {"data-testid": lambda x: x and x.startswith("event-link-")}
    ):
        if a_tag.has_attr("href"):
            concert_links.append(a_tag["href"])
    driver.quit()

    sample_data = concert_links[:5]
    print(f"Found {len(concert_links)} concert links. Sample data:")
    print(sample_data)


def default_mode(artist):
    """Scrape data, save it to a static file, and print it."""
    # artist = "Taylor Swift"
    artist = artist.lower().replace(" ", "-")
    url = f"https://seatgeek.com/{artist}-tickets"

    print(f"Scraping and saving data for artist: {artist}...")
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(10)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    concert_links = []
    for a_tag in soup.find_all(
        "a", {"data-testid": lambda x: x and x.startswith("event-link-")}
    ):
        if a_tag.has_attr("href"):
            concert_links.append(a_tag["href"])

    driver.quit()

    data = {"artist": artist, "concert_links": concert_links}
    project_root = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    dat_directory = os.path.join(project_root, "dat")
    os.makedirs(dat_directory, exist_ok=True)
    output_file = os.path.join(dat_directory, "concert_data.json")

    with open(output_file, "w") as f:
        json.dump(data, f)

    print(f"Data saved to {output_file}.")
    print(f"Total entries: {len(concert_links)}. Sample data:")
    print(json.dumps(data["concert_links"][:5], indent=2))

    sgf.seatgeek_format()
    print("Data formatted and saved to ticketmaster_data.py")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="HW4 Script for scraping and dataset handling."
    )
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
