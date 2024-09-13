from dataclasses import asdict
from typing import Any, List, Optional
from dotenv import load_dotenv
import pandas as pd
import logging

from scripts.models.models_csv import MovieCSV, ShowCSV
from scripts.models.models_api import Movie, Show, ShowProgress, WatchedShow
from scripts.util import combine_unique_shows, get_movies_from_watched_movies, get_movies_from_watchlist_movies, get_shows_from_watched_shows

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

def save_to_csv(data: List[Any], filename: str):
    # Validate if data is empty
    if not data:
        logging.warning(f"No data to save for {filename}. Skipping CSV generation.")
        return

    try:
        # Convert list of dataclass objects to list of dictionaries
        data_dicts = [asdict(item) for item in data]

        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame(data_dicts)

        # Check if 'rating' column exists and sort by it if it does
        if 'rating' in df.columns:
            # Convert the 'rating' column to numeric (float) if it's not already
            df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

            # Sort the DataFrame by the 'rating' column in descending order (largest to smallest)
            df = df.sort_values(by='rating', ascending=False)

        # Save the DataFrame to CSV with headers based on field names
        df.to_csv(filename, index=False)
        logging.info(f"Data saved to {filename}")

    except Exception as e:
        logging.error(f"Failed to save data to {filename}: {e}")

def process_shows_data(shows: List[Show]):
    processed_data: List[ShowCSV] = []

    for show in shows:
        try:
            title = show.title
            show_id = show.ids.slug

            # Use the show year as the release date
            release_date = str(show.year)

            # Fetch the rating using the proper function
            ratings = fetch_show_ratings(show_id)
            rating = None

            if not ratings:
                logging.warning(f"Data might be incomplete for {title}: Release Date={release_date}")
            else:
                rating = ratings.rating

            processed_data.append(ShowCSV(title, release_date, rating))

        except KeyError as e:
            logging.error(f"KeyError for show: {str(e)}")
            continue

    return processed_data

def process_movies_data(movies: List[Movie]):
    processed_data: List[MovieCSV] = []

    for movie in movies:
        try:
            title = movie.title
            movie_id = movie.ids.slug

            # Use the movie year as the release date
            release_date = str(movie.year)

            # Fetch the rating using the proper function
            ratings = fetch_movie_ratings(movie_id)
            rating = None

            if not ratings:
                logging.warning(f"Data might be incomplete for {title}: Release Date={release_date}")
            else:
                rating = ratings.rating

            processed_data.append(MovieCSV(title, release_date, rating))

        except KeyError as e:
            logging.error(f"KeyError for movie: {str(e)}")
            continue

    return processed_data

def fetch_in_progress_shows(watched_shows: Optional[List[WatchedShow]]):
    in_progress_shows: Optional[List[WatchedShow]] = []

    if watched_shows is None:
        return in_progress_shows
    
    for watched_show in watched_shows:
        show_id = watched_show.show.ids.slug
        
        # Fetch progress for the show
        progress: Optional[ShowProgress] = fetch_show_progress(show_id)
        
        if progress and progress.completed < progress.aired:
            in_progress_shows.append(watched_show)
    
    return in_progress_shows

def fetch_completed_shows(watched_shows: Optional[List[WatchedShow]]):
    completed_shows: Optional[List[WatchedShow]] = []

    if watched_shows is None:
        return completed_shows
    
    for watched_show in watched_shows:
        show_id = watched_show.show.ids.slug
        
        # Fetch progress for the show
        progress = fetch_show_progress(show_id)
        
        # Only add shows that are completed (i.e., all episodes watched)
        if progress and progress.completed == progress.aired:
            completed_shows.append(watched_show)
    
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
    combined_shows = combine_unique_shows(in_progress_shows, watchlist_shows)

    # Process and save the combined list of in-progress and watchlist shows
    processed_shows = process_shows_data(combined_shows)
    save_to_csv(processed_shows, 'watchlist_shows.csv')

    # Process and save completed shows to a separate CSV file
    processed_completed_shows = process_shows_data(get_shows_from_watched_shows(completed_shows))
    save_to_csv(processed_completed_shows, 'watched_shows.csv')

    # Fetch and process watched and watchlist movies
    watched_movies = fetch_watched_movies()
    watchlist_movies = fetch_watchlist_movies()

    processed_watched_movies = process_movies_data(get_movies_from_watched_movies(watched_movies))
    processed_watchlist_movies = process_movies_data(get_movies_from_watchlist_movies(watchlist_movies))

    save_to_csv(processed_watched_movies, 'watched_movies.csv')
    save_to_csv(processed_watchlist_movies, 'watchlist_movies.csv')
