"""
Movie Recommendation Platform 2025
Main Flask Application

A movie recommendation system using content-based filtering and genre similarity,
integrated with the TMDB API for dynamic movie data.
"""

import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from recommender import MovieRecommender
from tmdb_client import search_movie, get_trending_movies

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

# Initialize the recommendation engine
recommender = MovieRecommender(csv_path="data/movies.csv")


@app.route("/")
def index():
    """Home page with search and trending movies."""
    titles = recommender.get_all_titles()
    trending = get_trending_movies()
    return render_template("index.html", titles=titles, trending=trending)


@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    """Generate and display movie recommendations."""
    if request.method == "POST":
        movie_title = request.form.get("movie_title", "").strip()
    else:
        movie_title = request.args.get("movie", "").strip()

    if not movie_title:
        return render_template(
            "recommend.html",
            error="Please enter a movie title.",
            movie_title="",
            recommendations=[],
            movie_info=None,
            tmdb_data=None,
        )

    # Get recommendations from content-based filtering
    recommendations = recommender.get_recommendations(movie_title, n=10)
    movie_info = recommender.get_movie_info(movie_title)

    if not recommendations:
        return render_template(
            "recommend.html",
            error=f'No recommendations found for "{movie_title}". Try another title.',
            movie_title=movie_title,
            recommendations=[],
            movie_info=None,
            tmdb_data=None,
        )

    # Enrich recommendations with TMDB data (posters, live ratings)
    enriched = []
    for rec in recommendations:
        tmdb_info = search_movie(rec["title"])
        enriched.append(
            {
                **rec,
                "poster_url": tmdb_info["poster_url"] if tmdb_info else None,
                "tmdb_rating": tmdb_info["vote_average"] if tmdb_info else None,
            }
        )

    # Get TMDB data for the searched movie too
    tmdb_data = search_movie(movie_title)

    return render_template(
        "recommend.html",
        movie_title=movie_title,
        recommendations=enriched,
        movie_info=movie_info,
        tmdb_data=tmdb_data,
        error=None,
    )


@app.route("/api/search")
def api_search():
    """API endpoint for autocomplete search suggestions."""
    query = request.args.get("q", "").lower().strip()
    if not query:
        return jsonify([])

    titles = recommender.get_all_titles()
    matches = [t for t in titles if query in t.lower()]
    return jsonify(matches[:10])


@app.route("/api/recommend/<title>")
def api_recommend(title):
    """REST API endpoint for getting recommendations as JSON."""
    recommendations = recommender.get_recommendations(title, n=10)
    if not recommendations:
        return jsonify({"error": "Movie not found", "recommendations": []}), 404
    return jsonify({"movie": title, "recommendations": recommendations})


@app.route("/api/genres/<genre>")
def api_genre(genre):
    """API endpoint to get movies by genre."""
    movies = recommender.get_movies_by_genre(genre, n=10)
    return jsonify({"genre": genre, "movies": movies})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug, host="0.0.0.0", port=port)
