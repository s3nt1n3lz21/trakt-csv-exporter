from typing import Dict, List

from scripts.models import Show, WatchedShow, WatchlistShow

def get_shows_from_watched_shows(watched_shows: List[WatchedShow]) -> List[Show]:
    """
    Extracts a list of Show objects from a list of WatchedShow instances.
    """
    return [watched_show.show for watched_show in watched_shows]

def get_shows_from_watchlist_shows(watchlist_shows: List[WatchlistShow]) -> List[Show]:
    """
    Extracts a list of Show objects from a list of WatchlistShow instances.
    """
    return [watchlist_show.show for watchlist_show in watchlist_shows]

def combine_unique_shows(in_progress_shows: List[WatchedShow], watchlist_shows: List[WatchlistShow]) -> List[Show]:
    """
    Combines in-progress shows and watchlist (unwatched) shows into a unique list of Show objects.
    
    :param in_progress_shows: List of in-progress WatchedShow objects.
    :param watchlist_shows: List of WatchlistShow objects.
    :return: List of unique Show objects.
    """
    unique_shows: Dict[int, Show] = {}

    # Add in-progress shows to unique_shows dictionary
    for watched_show in in_progress_shows:
        show = watched_show.show
        unique_shows[show.ids.trakt] = show

    # Add watchlist shows to unique_shows if not already present
    for watchlist_show in watchlist_shows:
        show = watchlist_show.show
        if show.ids.trakt not in unique_shows:  # Ensure no duplicates
            unique_shows[show.ids.trakt] = show

    return list(unique_shows.values())