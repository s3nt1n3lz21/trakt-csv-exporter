from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class ShowIds:
    trakt: int
    slug: str
    tvdb: Optional[int]
    imdb: Optional[str]
    tmdb: Optional[int]
    tvrage: Optional[str]

@dataclass
class EpisodeProgress:
    number: int
    completed: bool
    last_watched_at: Optional[str]

@dataclass
class SeasonProgress:
    number: int
    title: str
    aired: int
    completed: int
    episodes: List[EpisodeProgress]

@dataclass
class EpisodeSummary:
    season: int
    number: int
    title: Optional[str]
    ids: Dict[str, Optional[int]]

@dataclass
class HiddenSeason:
    number: int
    ids: Dict[str, Optional[int]]

@dataclass
class ShowProgress:
    aired: int
    completed: int
    last_watched_at: Optional[str]
    reset_at: Optional[str]
    seasons: List[SeasonProgress]
    hidden_seasons: Optional[List[HiddenSeason]]
    next_episode: Optional[EpisodeSummary]
    last_episode: Optional[EpisodeSummary]

@dataclass
class Show:
    title: str
    year: int
    ids: ShowIds

@dataclass
class ShowDetails:
    title: str
    year: int
    ids: Dict[str, str]  # e.g., {"trakt": "1234", "imdb": "tt1234567", "tmdb": "56789"}
    overview: Optional[str]
    status: Optional[str]
    aired_episodes: Optional[int]
    runtime: Optional[int]
    genres: List[str]
    first_aired: Optional[str]
    language: Optional[str]

@dataclass
class Episode:
    number: int
    plays: int
    last_watched_at: Optional[str]  # ISO 8601 timestamp (e.g., 2014-10-11T17:00:54.000Z)

@dataclass
class Season:
    number: int
    episodes: List[Episode]

@dataclass
class WatchedShow:
    plays: int
    last_watched_at: Optional[str]  # ISO 8601 timestamp
    last_updated_at: Optional[str]  # ISO 8601 timestamp
    reset_at: Optional[str]  # Can be null, so Optional
    show: Show
    seasons: List[Season]

@dataclass
class WatchlistShow:
    rank: int
    id: int
    listed_at: str  # ISO 8601 timestamp (e.g., "2014-09-01T09:10:11.000Z")
    notes: Optional[str]
    type: str  # This will be "show" based on the response
    show: Show

@dataclass
class Ratings:
    rating: float
    votes: int
    distribution: Dict[str, int]

@dataclass
class MovieProgress:
    completed: bool
    last_watched_at: Optional[str]
    
@dataclass
class MovieDetails:
    title: str
    year: int
    ids: Dict[str, str]  # e.g., {"trakt": "1234", "imdb": "tt1234567", "tmdb": "56789"}
    overview: Optional[str]
    runtime: Optional[int]
    released: Optional[str]
    trailer: Optional[str]
    homepage: Optional[str]
    language: Optional[str]
    genres: List[str]
    rating: Optional[float]
    votes: Optional[int]

@dataclass
class MovieIds:
    trakt: int
    slug: str
    imdb: Optional[str]
    tmdb: Optional[int]

@dataclass
class Movie:
    title: str
    year: int
    ids: MovieIds

@dataclass
class WatchedMovie:
    plays: int
    last_watched_at: Optional[str]
    last_updated_at: Optional[str]
    movie: Movie

@dataclass
class WatchlistMovie:
    rank: int
    id: int
    listed_at: str  # ISO 8601 timestamp (e.g., "2014-09-01T09:10:11.000Z")
    notes: Optional[str]
    type: str  # This will be "movie" based on the response
    movie: Movie