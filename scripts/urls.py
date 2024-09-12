# Trakt API URLs

WATCHED_PROGRESS_URL = 'https://api.trakt.tv/shows/{id}/progress/watched?hidden=false&specials=false&count_specials=true'

# Response format
# {
#   "aired": 8,
#   "completed": 6,
#   "last_watched_at": "2015-03-21T19:03:58.000Z",
#   "reset_at": null,
#   "seasons": [
#     {
#       "number": 1,
#       "title": "The first Hodor.",
#       "aired": 8,
#       "completed": 6,
#       "episodes": [
#         {
#           "number": 1,
#           "completed": true,
#           "last_watched_at": "2015-03-21T19:03:58.000Z"
#         },
#         {
#           "number": 2,
#           "completed": true,
#           "last_watched_at": "2015-03-21T19:03:58.000Z"
#         },
#         {
#           "number": 3,
#           "completed": true,
#           "last_watched_at": "2015-03-21T19:03:58.000Z"
#         },
#         {
#           "number": 4,
#           "completed": true,
#           "last_watched_at": "2015-03-21T19:03:58.000Z"
#         },
#         {
#           "number": 5,
#           "completed": true,
#           "last_watched_at": "2015-03-21T19:03:58.000Z"
#         },
#         {
#           "number": 6,
#           "completed": true,
#           "last_watched_at": "2015-03-21T19:03:58.000Z"
#         },
#         {
#           "number": 7,
#           "completed": false,
#           "last_watched_at": null
#         },
#         {
#           "number": 8,
#           "completed": false,
#           "last_watched_at": null
#         }
#       ]
#     }
#   ],
#   "hidden_seasons": [
#     {
#       "number": 2,
#       "ids": {
#         "trakt": 3051,
#         "tvdb": 498968,
#         "tmdb": 53334
#       }
#     }
#   ],
#   "next_episode": {
#     "season": 1,
#     "number": 7,
#     "title": "Water",
#     "ids": {
#       "trakt": 62315,
#       "tvdb": 4849873,
#       "imdb": null,
#       "tmdb": null
#     }
#   },
#   "last_episode": {
#     "season": 1,
#     "number": 6,
#     "title": "Fire",
#     "ids": {
#       "trakt": 62314,
#       "tvdb": 4849872,
#       "imdb": null,
#       "tmdb": null
#     }
#   }
# }

WATCHED_SHOWS_URL = 'https://api.trakt.tv/sync/watched/shows'

# Response format
# [
#   {
#     "plays": 56,
#     "last_watched_at": "2014-10-11T17:00:54.000Z",
#     "last_updated_at": "2014-10-11T17:00:54.000Z",
#     "reset_at": null,
#     "show": {
#       "title": "Breaking Bad",
#       "year": 2008,
#       "ids": {
#         "trakt": 1,
#         "slug": "breaking-bad",
#         "tvdb": 81189,
#         "imdb": "tt0903747",
#         "tmdb": 1396
#       }
#     },
#     "seasons": [
#       {
#         "number": 1,
#         "episodes": [
#           {
#             "number": 1,
#             "plays": 1,
#             "last_watched_at": "2014-10-11T17:00:54.000Z"
#           },
#           {
#             "number": 2,
#             "plays": 1,
#             "last_watched_at": "2014-10-11T17:00:54.000Z"
#           }
#         ]
#       },
#       {
#         "number": 2,
#         "episodes": [
#           {
#             "number": 1,
#             "plays": 1,
#             "last_watched_at": "2014-10-11T17:00:54.000Z"
#           },
#           {
#             "number": 2,
#             "plays": 1,
#             "last_watched_at": "2014-10-11T17:00:54.000Z"
#           }
#         ]
#       }
#     ]
#   },
#   {
#     "plays": 23,
#     "last_watched_at": "2014-10-12T17:00:54.000Z",
#     "last_updated_at": "2014-10-12T17:00:54.000Z",
#     "show": {
#       "title": "Parks and Recreation",
#       "year": 2009,
#       "ids": {
#         "trakt": 4,
#         "slug": "parks-and-recreation",
#         "tvdb": 84912,
#         "imdb": "tt1266020",
#         "tmdb": 8592
#       }
#     },
#     "seasons": [
#       {
#         "number": 1,
#         "episodes": [
#           {
#             "number": 1,
#             "plays": 1,
#             "last_watched_at": "2014-10-11T17:00:54.000Z"
#           },
#           {
#             "number": 2,
#             "plays": 1,
#             "last_watched_at": "2014-10-11T17:00:54.000Z"
#           }
#         ]
#       },
#       {
#         "number": 2,
#         "episodes": [
#           {
#             "number": 1,
#             "plays": 1,
#             "last_watched_at": "2014-10-11T17:00:54.000Z"
#           },
#           {
#             "number": 2,
#             "plays": 1,
#             "last_watched_at": "2014-10-11T17:00:54.000Z"
#           }
#         ]
#       }
#     ]
#   }
# ]

SHOW_RATINGS_URL = 'https://api.trakt.tv/shows/{id}/ratings'

# Response format
# {
#   "rating": 9.38363,
#   "votes": 51065,
#   "distribution": {
#     "1": 320,
#     "2": 77,
#     "3": 73,
#     "4": 131,
#     "5": 300,
#     "6": 514,
#     "7": 1560,
#     "8": 4399,
#     "9": 9648,
#     "10": 34042
#   }
# }

SHOW_DETAILS_URL = 'https://api.trakt.tv/shows/id'

# Response format
# {
#   "title": "Game of Thrones",
#   "year": 2011,
#   "ids": {
#     "trakt": 353,
#     "slug": "game-of-thrones",
#     "tvdb": 121361,
#     "imdb": "tt0944947",
#     "tmdb": 1399
#   }
# }

WATCHLIST_SHOWS_URL = 'https://api.trakt.tv/sync/watchlist/shows'

# Response format

WATCHED_MOVIES_URL = 'https://api.trakt.tv/sync/watched/movies'

# Response format
# [
#   {
#     "plays": 4,
#     "last_watched_at": "2014-10-11T17:00:54.000Z",
#     "last_updated_at": "2014-10-11T17:00:54.000Z",
#     "movie": {
#       "title": "Batman Begins",
#       "year": 2005,
#       "ids": {
#         "trakt": 6,
#         "slug": "batman-begins-2005",
#         "imdb": "tt0372784",
#         "tmdb": 272
#       }
#     }
#   },
#   {
#     "plays": 2,
#     "last_watched_at": "2014-10-12T17:00:54.000Z",
#     "last_updated_at": "2014-10-12T17:00:54.000Z",
#     "movie": {
#       "title": "The Dark Knight",
#       "year": 2008,
#       "ids": {
#         "trakt": 4,
#         "slug": "the-dark-knight-2008",
#         "imdb": "tt0468569",
#         "tmdb": 155
#       }
#     }
#   }
# ]

WATCHLIST_MOVIES_URL = 'https://api.trakt.tv/sync/watchlist/movies'

MOVIE_RATINGS_URL = 'https://api.trakt.tv/movies/{movie_id}/ratings'

# Response format
# {
#   "rating": 7.33778,
#   "votes": 7866,
#   "distribution": {
#     "1": 298,
#     "2": 46,
#     "3": 87,
#     "4": 178,
#     "5": 446,
#     "6": 1167,
#     "7": 1855,
#     "8": 1543,
#     "9": 662,
#     "10": 1583
#   }
# }