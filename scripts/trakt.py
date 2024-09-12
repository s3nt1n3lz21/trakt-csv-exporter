from dotenv import load_dotenv
import pandas as pd
import logging
import math

load_dotenv()

# Set up logging
logging.basicConfig(
    filename='trakt_api.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s:%(message)s'
)

# Import specific fetch functions from api.py
from scripts.api import fetch_watched_shows, fetch_watchlist_shows, fetch_watched_movies, fetch_watchlist_movies
from scripts.api import fetch_show_ratings, fetch_movie_ratings, fetch_show_progress

def save_to_csv(data, filename):
    df = pd.DataFrame(data)

    # Convert the 'Rating' column to floats, with errors='coerce' to handle non-convertible values
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

    # Handle NaN ratings by replacing them with a default value, e.g., 0
    df['Rating'] = df['Rating'].fillna(0)

    # Sort by Rating after conversion
    df = df.sort_values(by='Rating', ascending=False)

    df.to_csv(filename, index=False)
    logging.info(f"Data saved to {filename}")

def process_shows_data(shows):
    processed_data = []

    for show in shows:
        try:
            title = show['show']['title']
            show_id = show['show']['ids']['slug']

            # Use the show year as the release date
            release_date = str(show['show']['year'])

            # Fetch the rating using the proper function
            ratings = fetch_show_ratings(show_id)

            if not ratings:
                logging.warning(f"Data might be incomplete for {title}: Release Date={release_date}")

            processed_data.append({
                'Title': title,
                'Release Date': release_date,
                'Seasons Watched': show['seasons'] if 'seasons' in show else 'N/A',
                'Rating': ratings.rating
            })

        except KeyError as e:
            logging.error(f"KeyError for show: {str(e)}")
            continue

    return processed_data

def process_movies_data(movies):
    processed_data = []

    for movie in movies:
        try:
            title = movie['movie']['title']
            movie_id = movie['movie']['ids']['slug']

            # Use the movie year as the release date
            release_date = str(movie['movie']['year'])

            # Fetch the rating using the proper function
            ratings = fetch_movie_ratings(movie_id)

            if not ratings:
                logging.warning(f"Data might be incomplete for {title}: Release Date={release_date}")

            processed_data.append({
                'Title': title,
                'Release Date': release_date,
                'Rating': ratings.rating
            })

        except KeyError as e:
            logging.error(f"KeyError for movie: {str(e)}")
            continue

    return processed_data

def fetch_in_progress_shows(watched_shows):
    in_progress_shows = []
    
    for show in watched_shows:
        show_id = show['show']['ids']['slug']
        
        # Fetch progress for the show
        progress = fetch_show_progress(show_id)
        
        if progress and progress.completed < progress.aired:
            in_progress_shows.append(show)
    
    return in_progress_shows

def fetch_completed_shows(watched_shows):
    completed_shows = []
    
    for show in watched_shows:
        show_id = show['show']['ids']['slug']
        
        # Fetch progress for the show
        progress = fetch_show_progress(show_id)
        
        # Only add shows that are completed (i.e., all episodes watched)
        if progress and progress.completed == progress.aired:
            completed_shows.append(show)
    
    return completed_shows

if __name__ == "__main__":
    # Fetch watched and watchlist shows
    watched_shows = fetch_watched_shows()
    watchlist_shows = fetch_watchlist_shows()

    # Fetch in-progress shows by filtering out completed ones
    in_progress_shows = fetch_in_progress_shows(watched_shows)

    # Fetch completed shows
    completed_shows = fetch_completed_shows(watched_shows)

    # Combine in-progress shows with watchlist shows
    combined_shows = in_progress_shows + watchlist_shows

    # Process and save the combined list of in-progress and watchlist shows
    processed_shows = process_shows_data(combined_shows)
    save_to_csv(processed_shows, 'watchlist_shows.csv')

    # Process and save completed shows to a separate CSV file
    processed_completed_shows = process_shows_data(completed_shows)
    save_to_csv(processed_completed_shows, 'watched_shows.csv')

    # Fetch and process watched and watchlist movies
    watched_movies = fetch_watched_movies()
    watchlist_movies = fetch_watchlist_movies()

    processed_watched_movies = process_movies_data(watched_movies)
    processed_watchlist_movies = process_movies_data(watchlist_movies)

    save_to_csv(processed_watched_movies, 'watched_movies.csv')
    save_to_csv(processed_watchlist_movies, 'watchlist_movies.csv')
