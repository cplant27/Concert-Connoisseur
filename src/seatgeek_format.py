import json
import os


def seatgeek_format():
    fname = "../dat/concert_data.json"
    root = "https://seatgeek.com"
    try:
        # Load the JSON data from the file
        with open(fname, "r") as file:
            data = json.load(file)

        # Check if required keys exist
        if "artist" not in data or "concert_links" not in data:
            print(f"The file {fname} does not have the required format.")
            return

        # Parse and format the concert links
        parsed_data = {
            "artist": data["artist"].replace("-", " ").title(),
            "concerts": [],
        }

        for link in data["concert_links"]:
            parts = link.split("/")  # Split the URL by '/'
            location = (
                parts[2][:-15].replace("-", " ").title()
            )  # e.g., "toronto-canada-rogers-centre"
            datetime = parts[2][-15::]  # e.g., "2024-11-21-7-pm"
            date, time = datetime.split("-")[:3], datetime.split("-")[3:]
            date_str = "-".join(date)  # Convert ['2024', '11', '21'] to "2024-11-21"
            time_str = " ".join(time)  # Convert ['7', 'pm'] to "7 pm"
            full_link = root + link

            parsed_data["concerts"].append(
                {
                    "location": location,
                    "date": date_str,
                    "time": time_str,
                    "link": full_link,
                }
            )

        # Define the output file path
        project_root = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        dat_directory = os.path.join(project_root, "dat")
        os.makedirs(dat_directory, exist_ok=True)
        output_file = os.path.join(dat_directory, "seatgeek_data.json")

        with open(output_file, "w") as output:
            json.dump(parsed_data, output, indent=4)

        print(f"Parsed data saved to {output_file}")

    except FileNotFoundError:
        print(f"The file {fname} was not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    seatgeek_format()
