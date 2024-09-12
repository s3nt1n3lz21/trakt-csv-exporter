from typing import Optional, Type, Union
import requests
import logging
import os
import time
from scripts.models import ShowProgress, ShowDetails, Ratings, Distribution, MovieProgress, WatchedMovie, WatchedShow
from scripts.urls import MOVIE_RATINGS_URL, WATCHED_PROGRESS_URL, SHOW_RATINGS_URL, WATCHED_MOVIES_URL, SHOW_DETAILS_URL, WATCHED_SHOWS_URL, WATCHLIST_MOVIES_URL, WATCHLIST_SHOWS_URL
from requests.exceptions import SSLError, Timeout, RequestException

CLIENT_ID = os.getenv('TRAKT_CLIENT_ID')
ACCESS_TOKEN = os.getenv('TRAKT_ACCESS_TOKEN')

if not CLIENT_ID or not ACCESS_TOKEN:
    logging.critical("TRAKT_CLIENT_ID or TRAKT_ACCESS_TOKEN is missing from the environment variables.")
    raise EnvironmentError("Missing Trakt API credentials.")

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'trakt-api-version': '2',
    'trakt-api-key': CLIENT_ID
}

url_to_type_map = {
    WATCHED_SHOWS_URL: WatchedShow,
    WATCHLIST_SHOWS_URL: WatchedShow,  # CHECK
    WATCHED_MOVIES_URL: WatchedMovie,
    WATCHLIST_MOVIES_URL: MovieProgress,  # CHECK
    SHOW_RATINGS_URL: Ratings,
    MOVIE_RATINGS_URL: Ratings,
    WATCHED_PROGRESS_URL: ShowProgress,
    SHOW_DETAILS_URL: ShowDetails # CHECK
}

def get_return_type_for_url(url: str) -> Optional[Type]:
    """
    Returns the corresponding model type for the given Trakt API URL.
    """
    return url_to_type_map.get(url)

def handle_rate_limit(response):
    retry_after = int(response.headers.get('Retry-After', 10))
    logging.warning(f"Rate limit reached. Retrying after {retry_after} seconds...")
    time.sleep(retry_after)

def log_error(response):
    status_code = response.status_code
    if status_code == 400:
        logging.error(f"Bad Request: {response.text}")
    elif status_code == 401:
        logging.error(f"Unauthorized: Check your API credentials. {response.text}")
    elif status_code == 404:
        logging.error(f"Not Found: The requested resource could not be found. {response.text}")
    elif status_code == 500:
        logging.error(f"Server Error: There was an issue on the server. {response.text}")
    else:
        logging.error(f"Unexpected Error: {status_code} - {response.text}")
    logging.debug(f"Full Response: {response.text}")
    logging.debug(f"Request Headers: {response.request.headers}")


def fetch_trakt_data(url: str) -> Optional[Union[WatchedShow, ShowProgress, ShowDetails, Ratings, MovieProgress]]:
    """
    Fetches data from the Trakt API and parses it into the appropriate model type based on the URL.
    """
    try:
        logging.debug(f"Fetching data from GET {url}")
        logging.debug(f"Request Headers: {headers}")
        
        response = requests.get(url, headers=headers, timeout=10)  # Added timeout to prevent hanging
        
        if response.status_code == 200:
            data = response.json()
            
            # Get the corresponding return type for the URL
            model_type = get_return_type_for_url(url)
            if model_type:
                try:
                    return model_type(**data)
                except TypeError as e:
                    logging.error(f"Error parsing data into {model_type.__name__}: {e}")
            else:
                logging.warning(f"No return type found for URL {url}")
                return data  # If no specific model, return raw data
            
        elif response.status_code == 429:
            handle_rate_limit(response)
        else:
            log_error(response)
    except SSLError as e:
        logging.error(f"SSL error occurred while fetching data from {url}: {e}")
    except Timeout as e:
        logging.error(f"Request timed out while fetching data from {url}: {e}")
    except RequestException as e:
        logging.error(f"Request exception occurred while fetching data from {url}: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

    return None

def fetch_watched_shows():
    return fetch_trakt_data(WATCHED_SHOWS_URL)

def fetch_watchlist_shows():
    return fetch_trakt_data(WATCHLIST_SHOWS_URL)

def fetch_watched_movies():
    return fetch_trakt_data(WATCHED_MOVIES_URL)

def fetch_watchlist_movies():
    return fetch_trakt_data(WATCHLIST_MOVIES_URL)

def fetch_show_progress(show_id: str) -> ShowProgress:
    """
    Fetches the progress of a show using the Trakt API and parses it into the ShowProgress object.
    """
    url = WATCHED_PROGRESS_URL.format(id=show_id)
    data = fetch_trakt_data(url)
    if data:
        try:
            # Parse the response JSON into the ShowProgress object
            return ShowProgress(**data)
        except TypeError as e:
            logging.error(f"Error parsing show progress data: {e}")
    return None

def fetch_show_details(show_id: str) -> ShowDetails:
    """
    Fetches the details of a show using the Trakt API and parses it into the Show object.
    """
    url = SHOW_DETAILS_URL.format(id=show_id)
    data = fetch_trakt_data(url)
    if data:
        try:
            # Parse the response JSON into the Show object
            return ShowDetails(**data)
        except TypeError as e:
            logging.error(f"Error parsing show details: {e}")
    return None

def fetch_show_ratings(show_id: str) -> Ratings:
    """
    Fetches the ratings of a show using the Trakt API and parses it into the Ratings object.
    """
    url = SHOW_RATINGS_URL.format(id=show_id)
    data = fetch_trakt_data(url)
    if data:
        try:
            # Parse the response JSON into the Ratings object
            return Ratings(**data)
        except TypeError as e:
            logging.error(f"Error parsing ratings data: {e}")
    return None

def fetch_movie_progress(movie_id: str) -> MovieProgress:
    """
    Fetches the progress of a movie using the Trakt API and parses it into the MovieProgress object.
    """
    url = WATCHED_MOVIES_URL.format(id=movie_id)
    data = fetch_trakt_data(url)
    if data:
        try:
            # Parse the response JSON into the MovieProgress object
            return MovieProgress(**data)
        except TypeError as e:
            logging.error(f"Error parsing movie progress data: {e}")
    return None

def fetch_movie_ratings(movie_id: str) -> Ratings:
    """
    Fetches the ratings of a movie using the Trakt API and parses it into the Ratings object.
    """
    url = MOVIE_RATINGS_URL.format(movie_id=movie_id)
    data = fetch_trakt_data(url)
    
    if data:
        try:
            # Parse the distribution data as a dictionary
            distribution_data = data.get('distribution', {})
            
            # Create a Distribution object and populate it with the dictionary
            distribution = Distribution(distribution=distribution_data)
            
            # Create and return a Ratings object, passing values to the constructor
            ratings = Ratings(
                rating=data.get('rating', 0.0),
                votes=data.get('votes', 0),
                distribution=distribution
            )
            
            return ratings
        except Exception as e:
            logging.error(f"Error parsing movie ratings data: {e}")
    
    return None

