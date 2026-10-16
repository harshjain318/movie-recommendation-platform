"""
TMDB API Client
Handles communication with The Movie Database (TMDB) API
to fetch movie posters, ratings, and descriptions dynamically.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"


def search_movie(title):
    """
    Search for a movie by title on TMDB.
    Returns the first matching result with poster, rating, and overview.
    """
    if not TMDB_API_KEY or TMDB_API_KEY == "your_tmdb_api_key_here":
        return None

    try:
        url = f"{TMDB_BASE_URL}/search/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "query": title,
            "language": "en-US",
            "page": 1,
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("results"):
            movie = data["results"][0]
            return {
                "tmdb_id": movie.get("id"),
                "title": movie.get("title", title),
                "overview": movie.get("overview", "No description available."),
                "poster_url": (
                    f"{TMDB_IMAGE_BASE_URL}{movie['poster_path']}"
                    if movie.get("poster_path")
                    else None
                ),
                "vote_average": movie.get("vote_average", 0),
                "release_date": movie.get("release_date", "N/A"),
            }
    except requests.RequestException as e:
        print(f"TMDB API error for '{title}': {e}")

    return None


def get_movie_details(tmdb_id):
    """
    Fetch detailed information for a specific movie by TMDB ID.
    """
    if not TMDB_API_KEY or TMDB_API_KEY == "your_tmdb_api_key_here":
        return None

    try:
        url = f"{TMDB_BASE_URL}/movie/{tmdb_id}"
        params = {
            "api_key": TMDB_API_KEY,
            "language": "en-US",
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        movie = response.json()

        return {
            "tmdb_id": movie.get("id"),
            "title": movie.get("title"),
            "overview": movie.get("overview", "No description available."),
            "poster_url": (
                f"{TMDB_IMAGE_BASE_URL}{movie['poster_path']}"
                if movie.get("poster_path")
                else None
            ),
            "vote_average": movie.get("vote_average", 0),
            "release_date": movie.get("release_date", "N/A"),
            "runtime": movie.get("runtime", 0),
            "genres": [g["name"] for g in movie.get("genres", [])],
            "tagline": movie.get("tagline", ""),
        }
    except requests.RequestException as e:
        print(f"TMDB API error for ID {tmdb_id}: {e}")

    return None


def get_trending_movies():
    """
    Fetch currently trending movies from TMDB.
    """
    if not TMDB_API_KEY or TMDB_API_KEY == "your_tmdb_api_key_here":
        return []

    try:
        url = f"{TMDB_BASE_URL}/trending/movie/week"
        params = {"api_key": TMDB_API_KEY}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        movies = []
        for movie in data.get("results", [])[:10]:
            movies.append(
                {
                    "tmdb_id": movie.get("id"),
                    "title": movie.get("title"),
                    "overview": movie.get("overview", ""),
                    "poster_url": (
                        f"{TMDB_IMAGE_BASE_URL}{movie['poster_path']}"
                        if movie.get("poster_path")
                        else None
                    ),
                    "vote_average": movie.get("vote_average", 0),
                    "release_date": movie.get("release_date", "N/A"),
                }
            )
        return movies
    except requests.RequestException as e:
        print(f"TMDB API error fetching trending: {e}")

    return []
