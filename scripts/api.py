from dataclasses import fields
from typing import Dict, List, Optional, Type, Union
import requests
import logging
import os
import time
from scripts.models import ShowProgress, ShowDetails, Ratings, MovieProgress, WatchedMovie, WatchedShow, WatchlistMovie, WatchlistShow
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
    WATCHLIST_SHOWS_URL: WatchlistShow,
    WATCHED_MOVIES_URL: WatchedMovie,
    WATCHLIST_MOVIES_URL: WatchlistMovie,  # CHECK
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

def parse_dataclass(model_type: Type, data: Union[dict, list]) -> any:
    """
    Recursively parses a dictionary or list into the corresponding dataclass.
    """
    if isinstance(data, list):
        return [parse_dataclass(model_type, item) for item in data]

    if isinstance(data, dict):
        # Parse each field in the dataclass
        fieldtypes = {f.name: f.type for f in fields(model_type)}
        parsed_data = {}
        
        for key, value in data.items():
            if key in fieldtypes and is_dataclass_type(fieldtypes[key]):
                # Recursively parse if it's another dataclass
                parsed_data[key] = parse_dataclass(fieldtypes[key], value)
            else:
                parsed_data[key] = value

        return model_type(**parsed_data)

    return data

def is_dataclass_type(tp: Type) -> bool:
    """
    Checks if the type is a dataclass type.
    """
    return hasattr(tp, '__dataclass_fields__')

def fetch_trakt_data(url: str, model_type: Type) -> Optional[Union[WatchedShow, ShowProgress, ShowDetails, Ratings, MovieProgress]]:
    """
    Fetches data from the Trakt API and parses it into the appropriate model type.
    """
    try:
        logging.debug(f"Fetching data from GET {url}")
        logging.debug(f"Request Headers: {headers}")
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()

            # If the data is a list, parse each item in the list into the model type
            if isinstance(data, list):
                return parse_dataclass(model_type, data)
            else:
                return parse_dataclass(model_type, data)  # Parse single object

        elif response.status_code == 429:
            handle_rate_limit(response)
        else:
            log_error(response)
    
    except (SSLError, Timeout, RequestException) as e:
        logging.error(f"Error occurred while fetching data from {url}: {e}")
    except TypeError as e:
        logging.error(f"Error parsing data into {model_type.__name__}: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

    return None

def fetch_watched_shows() -> List[WatchedShow]:
    watched_shows = fetch_trakt_data(WATCHED_SHOWS_URL, WatchedShow)
    if watched_shows is None:
        return []
    else:
        return watched_shows

def fetch_watchlist_shows() -> List[WatchlistShow]:
    watchlist_shows = fetch_trakt_data(WATCHLIST_SHOWS_URL, WatchlistShow)
    if watchlist_shows is None:
        return []
    else:
        return watchlist_shows

def fetch_watched_movies() -> List[WatchedMovie]:
    watched_movies = fetch_trakt_data(WATCHED_MOVIES_URL, WatchedMovie)
    if watched_movies is None:
        return []
    else:
        return watched_movies

def fetch_watchlist_movies() -> List[WatchlistMovie]:
    watchlist_movies = fetch_trakt_data(WATCHLIST_MOVIES_URL, WatchlistMovie)
    if watchlist_movies is None:
        return []
    else:
        return watchlist_movies

def fetch_show_progress(show_id: str) -> Optional[ShowProgress]:
    return fetch_trakt_data(WATCHED_PROGRESS_URL.format(id=show_id), ShowProgress)

def fetch_show_details(show_id: str) -> Optional[ShowDetails]:
    """
    Fetches the details of a show using the Trakt API and parses it into the Show object.
    """
    url = SHOW_DETAILS_URL.format(id=show_id)
    return fetch_trakt_data(url, ShowDetails)

def fetch_show_ratings(show_id: str) -> Optional[Ratings]:
    """
    Fetches the ratings of a show using the Trakt API and parses it into the Ratings object.
    """
    url = SHOW_RATINGS_URL.format(id=show_id)
    return fetch_trakt_data(url, Ratings)

# def fetch_movie_progress(movie_id: str) -> MovieProgress:
#     """
#     Fetches the progress of a movie using the Trakt API and parses it into the MovieProgress object.
#     """
#     url = WATCHED_MOVIES_URL.format(id=movie_id)
#     data = fetch_trakt_data(url)
#     if data:
#         try:
#             # Parse the response JSON into the MovieProgress object
#             return MovieProgress(**data)
#         except TypeError as e:
#             logging.error(f"Error parsing movie progress data: {e}")
#     return None

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
            distribution: Dict[str, int] = {}
            
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

