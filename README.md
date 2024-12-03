# Concert Connoisseur by CJ Plantemoli and Makena Robison
# Spotify Data Analysis Script

## Description
This script fetches and analyzes user data from the Spotify API. It can run in three modes:
1. **Static Mode**: Reads and displays a static dataset stored as a JSON file.
2. **Scrape Mode**: Fetches sample data (top 5 artists) using the Spotify API and displays it.
3. **Default Mode**: Combines scraping, saving the data to a static JSON file, and displaying a sample.

## Prerequisites
Ensure the following Python modules are installed:
- `os`
- `argparse`
- `json`
- `spotipy`

To install Spotipy, use:
```bash
pip install spotipy
```

You must also have Spotify Developer credentials (Client ID, Client Secret) set as environment variables:
- `SPOTIPY_CLIENT_ID`
- `SPOTIPY_CLIENT_SECRET`
- `SPOTIPY_REDIRECT_URI`

Refer to the Spotipy documentation for detailed setup instructions: https://spotipy.readthedocs.io/

## Files Included
1. **spotipy_calls.py**: The main Python script to be run.
2. **top_artists.json**: The static dataset generated in default mode (created upon running the script).
3. **README.txt**: Instructions for running the script.
4. **Diagram.png**: A diagram showing the script workflow.

## Running the Script
### Static Mode
This mode loads a static dataset and prints its contents or a sample. Provide the path to a JSON file.
```bash
python spotipy_callst.py --static <path/to/static_dataset.json>
```
Example:
```bash
python spotipy_calls.py --static top_artists.json
```

### Scrape Mode
This mode fetches sample data (top 5 artists) from the Spotify API.
```bash
python spotipy_calls.py --scrape
```

### Default Mode
This mode performs the full process:
1. Fetches top 50 artists using the Spotify API.
2. Saves the data to a JSON file (`spotify_top_artists.json`).
3. Prints a sample of the data.
```bash
python spotipy_calls.py
```

## Extensibility
This script can be extended by:
- Adding more data endpoints from the Spotify API, such as user playlists or track data.
- Supporting additional output formats, such as CSV or SQL.
- Incorporating data visualization libraries for graphical representation of the data.

## Maintainability
The following points outline potential issues:
- **API Limits**: The Spotify API may have rate limits that could cause the script to fail with frequent requests.
- **Static Dataset Size**: Large datasets may slow down processing or exceed memory limits.
- **Environment Variables**: Missing Spotify API credentials will cause authentication failures.
- **Dependency Updates**: Changes to the Spotipy library may require updates to the script.

## Approximate Runtime
- **Static Mode**: Instantaneous (depends on the size of the dataset).
- **Scrape Mode**: 5-10 seconds (depending on network speed).
- **Default Mode**: 10-15 seconds (includes data fetching and file saving).

## Diagram
Refer to the `Diagram.png` file included in the submission for a visual representation of the script's workflow.

# Seatgeek Script
This script fetches data from Seatgeek using a web scraper. It can run in three modes:
1. **Static Mode**: Reads and displays a static dataset stored as a JSON file.
2. **Scrape Mode**: Fetches sample data  using the web scraper and displays it.
3. **Default Mode**: Combines scraping, saving the data to a static JSON file, and displaying a sample.


# Ticketmaster Script
This script fetches data from the Ticketmaster API. It can run in three modes:
1. **Static Mode**: Reads and displays a static dataset stored as a JSON file.
2. **Scrape Mode**: Fetches sample datausing the Ticketmaster API and displays it.
3. **Default Mode**: Combines scraping, saving the data to a static JSON file, and displaying a sample.



## Running the Scripts

### Static Mode


For Ticketmaster:
```bash
python ticketmaster_calls.py --static <path/to/static_dataset.json>
```
Example:
```bash
python ticketmaster_calls.py --static dat/ticketmaster_data.json
```

For SeatGeek:
```bash
python seatgeek_calls.py --static <path/to/static_dataset.json>
```
Example:
```bash
python seatgeek_calls.py --static dat/seatgeek_data.json
```

---

### Scrape Mode


For Ticketmaster:
```bash
python ticketmaster_calls.py --scrape "Taylor Swift"
```

For SeatGeek:
```bash
python seatgeek_calls.py --scrape "Taylor Swift"
```

---

### Default Mode
This mode performs the full process:
1. Fetches event data for a predefined artist (e.g., "Taylor Swift").
2. Saves the data to a JSON file (`ticketmaster_data.json` or `concert_data.json`) in the `dat` directory.
3. Prints a sample of the data.

For Ticketmaster:
```bash
python3 ticketmaster_calls.py
```

For SeatGeek:
```bash
python3 seatgeek_calls.py
```

---

## Extensibility
These scripts can be extended by:
- Adding more data fields, such as ticket prices or seating options, by expanding the API request parameters.
- Supporting additional APIs for event data, allowing for cross-platform comparisons.
- Including output formats like CSV or SQL for easier integration with other tools.
- Adding filtering and sorting functionality for events by date, location, or price.

---

## Maintainability
The following points outline potential issues:
- **API Limits**: Ticketmaster API may enforce rate limits or quotas, causing the script to fail if too many requests are made in a short period.
- **Static Dataset Size**: Large datasets could slow down processing or lead to memory errors when printing or loading.
- **Environment Variables**: Missing API credentials (e.g., Ticketmaster API key) will cause authentication failures.
- **Website Structure (SeatGeek)**: Changes to the SeatGeek website's structure could break the scraping functionality.
- **Dependency Updates**: Updates to libraries like `requests`, `selenium`, or `BeautifulSoup` may require adjustments to the script.

