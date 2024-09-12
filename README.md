# trakt-csv-exporter

`trakt-csv-exporter` is a Python script that uses the Trakt API to fetch and export a user's watchlist and completed shows and movies to CSV files. This tool helps users track their media progress and organize their data in an easily accessible format.

## Features

- Fetches watched and watchlist shows from Trakt.
- Identifies in-progress shows by filtering out completed ones.
- Exports in-progress and watchlist shows to a CSV file (`watchlist_shows.csv`).
- Exports completed shows to a separate CSV file (`watched_shows.csv`).
- Fetches watched and watchlist movies from Trakt.
- Exports watched and watchlist movies to separate CSV files (`watched_movies.csv`, `watchlist_movies.csv`).

## Requirements

- Python 3.7+
- `requests` library
- Trakt API key

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/trakt-csv-exporter.git
    cd trakt-csv-exporter
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your Trakt API key by creating a `.env` file:
    ```bash
    TRAKT_API_KEY=your_api_key_here
    ```

## Usage

To run the script and generate the CSVs:

```bash
python -m scripts.trakt
```

This will generate four CSV files:

- `watchlist_shows.csv`: A list of shows in your watchlist or in-progress.
- `watched_shows.csv`: A list of shows you've completed.
- `watchlist_movies.csv`: A list of movies in your watchlist.
- `watched_movies.csv`: A list of movies you've completed.

## Testing

Test scripts are located in the `scripts/tests` folder. To run the tests, use:

```bash
python -m scripts.tests.fetch_movie_ratings
```

Replace fetch_movie_ratings with the relevant test script you want to run.

## Contributing

Feel free to open issues or pull requests if you'd like to contribute!

## License

This project is licensed under the MIT License - see the LICENSE file for details.