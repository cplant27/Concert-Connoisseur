
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
