from dotenv import load_dotenv
import os
import logging

path_env = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(path_env)

from scripts.api import fetch_movie_ratings

logging.basicConfig(
    filename='trakt_api.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s:%(message)s'
)

if __name__ == "__main__":
    # Fetch and process watched and watchlist shows
    logging.debug(f"Using .env file from path: {path_env}")
    try: 
        show_details = fetch_movie_ratings("godzilla-x-kong-the-new-empire-2024")
        print('show_details: ', show_details)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")