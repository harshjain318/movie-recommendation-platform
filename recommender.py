"""
Movie Recommendation Engine
Uses content-based filtering with genre similarity and TF-IDF
on movie overviews to generate recommendations.
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:
    """Content-based movie recommendation engine using genre similarity and TF-IDF."""

    def __init__(self, csv_path="data/movies.csv"):
        """Initialize the recommender by loading and preprocessing movie data."""
        self.df = pd.read_csv(csv_path)
        self._preprocess()
        self._build_similarity_matrix()

    def _preprocess(self):
        """Clean and prepare the dataset for similarity computation."""
        # Fill missing values
        self.df["genres"] = self.df["genres"].fillna("")
        self.df["overview"] = self.df["overview"].fillna("")
        self.df["vote_average"] = pd.to_numeric(
            self.df["vote_average"], errors="coerce"
        ).fillna(0)

        # Combine genres and overview into a single feature string for TF-IDF
        self.df["combined_features"] = (
            self.df["genres"] + " " + self.df["overview"]
        )

        # Normalize title for case-insensitive lookup
        self.df["title_lower"] = self.df["title"].str.lower().str.strip()

    def _build_similarity_matrix(self):
        """Build the cosine similarity matrix from combined features using TF-IDF."""
        tfidf = TfidfVectorizer(stop_words="english")
        tfidf_matrix = tfidf.fit_transform(self.df["combined_features"])
        self.similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    def get_recommendations(self, title, n=10):
        """
        Get top-N movie recommendations based on content similarity.

        Args:
            title: Movie title to find recommendations for.
            n: Number of recommendations to return (default: 10).

        Returns:
            List of dictionaries containing recommended movie info,
            or an empty list if the title is not found.
        """
        title_lower = title.lower().strip()

        # Find the movie index
        matches = self.df[self.df["title_lower"] == title_lower]
        if matches.empty:
            # Try partial match
            matches = self.df[
                self.df["title_lower"].str.contains(title_lower, na=False)
            ]
            if matches.empty:
                return []

        idx = matches.index[0]

        # Get similarity scores and sort them
        sim_scores = list(enumerate(self.similarity_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Skip the first one (it's the movie itself) and take top N
        sim_scores = sim_scores[1 : n + 1]

        # Build recommendation list
        recommendations = []
        for i, score in sim_scores:
            row = self.df.iloc[i]
            recommendations.append(
                {
                    "title": row["title"],
                    "genres": row["genres"],
                    "overview": row["overview"],
                    "vote_average": round(float(row["vote_average"]), 1),
                    "release_year": int(row["release_year"])
                    if pd.notna(row.get("release_year"))
                    else "N/A",
                    "similarity_score": round(float(score), 3),
                }
            )

        return recommendations

    def get_all_titles(self):
        """Return a sorted list of all movie titles in the dataset."""
        return sorted(self.df["title"].tolist())

    def get_movie_info(self, title):
        """Get information about a specific movie from the dataset."""
        title_lower = title.lower().strip()
        matches = self.df[self.df["title_lower"] == title_lower]

        if matches.empty:
            matches = self.df[
                self.df["title_lower"].str.contains(title_lower, na=False)
            ]
            if matches.empty:
                return None

        row = matches.iloc[0]
        return {
            "title": row["title"],
            "genres": row["genres"],
            "overview": row["overview"],
            "vote_average": round(float(row["vote_average"]), 1),
            "release_year": int(row["release_year"])
            if pd.notna(row.get("release_year"))
            else "N/A",
        }

    def get_movies_by_genre(self, genre, n=10):
        """Get top-rated movies filtered by a specific genre."""
        genre_lower = genre.lower()
        filtered = self.df[
            self.df["genres"].str.lower().str.contains(genre_lower, na=False)
        ]
        filtered = filtered.sort_values("vote_average", ascending=False).head(n)

        return [
            {
                "title": row["title"],
                "genres": row["genres"],
                "overview": row["overview"],
                "vote_average": round(float(row["vote_average"]), 1),
                "release_year": int(row["release_year"])
                if pd.notna(row.get("release_year"))
                else "N/A",
            }
            for _, row in filtered.iterrows()
        ]
