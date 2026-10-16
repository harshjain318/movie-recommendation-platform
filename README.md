# 🎬 Movie Recommendation Platform 2025

A movie recommendation system built with **Python, Flask, Pandas, and TMDB API** that uses **content-based filtering** and **genre similarity** to suggest movies you'll love.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask)
![Pandas](https://img.shields.io/badge/Pandas-2.2-purple?logo=pandas)
![TMDB](https://img.shields.io/badge/TMDB-API-01d277?logo=themoviedatabase)

---

## ✨ Features

- **Content-Based Filtering** — Recommends movies using TF-IDF vectorization and cosine similarity on genres + overviews
- **TMDB API Integration** — Fetches live movie posters, ratings, and descriptions dynamically
- **Autocomplete Search** — Real-time search suggestions as you type
- **Trending Movies** — Displays currently trending movies from TMDB
- **Genre Filtering** — Browse movies by genre via the REST API
- **Responsive Design** — Modern dark-themed UI that works on desktop and mobile
- **REST API** — JSON endpoints for programmatic access to recommendations

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| **Python 3.9+** | Core programming language |
| **Flask** | Web framework for routing & templating |
| **Pandas** | Data loading, cleaning, and processing |
| **scikit-learn** | TF-IDF vectorization & cosine similarity |
| **TMDB API** | Live movie metadata, posters, and trending data |
| **HTML/CSS/JS** | Frontend with dark theme UI |

## 📁 Project Structure

```
movie-recommendation-platform/
├── app.py                  # Main Flask application
├── recommender.py          # Content-based recommendation engine
├── tmdb_client.py          # TMDB API client
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── data/
│   └── movies.csv          # Movie dataset (30 popular movies)
├── templates/
│   ├── base.html           # Base layout template
│   ├── index.html          # Home page
│   └── recommend.html      # Recommendations page
└── static/
    ├── css/
    │   └── style.css       # Dark theme stylesheet
    └── js/
        └── main.js         # Autocomplete & interactivity
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- TMDB API Key ([Get one here](https://www.themoviedb.org/settings/api))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/movie-recommendation-platform.git
   cd movie-recommendation-platform
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your TMDB API key
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser** and navigate to `http://localhost:5000`

> **Note:** The app works without a TMDB API key — you just won't see movie posters and trending movies. All recommendations still function via the local dataset.

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/recommend` | GET/POST | Get movie recommendations |
| `/api/search?q=<query>` | GET | Autocomplete search suggestions |
| `/api/recommend/<title>` | GET | JSON recommendations for a movie |
| `/api/genres/<genre>` | GET | Movies filtered by genre |

### Example API Usage

```bash
# Get recommendations for "Inception"
curl http://localhost:5000/api/recommend/Inception

# Search for movies
curl http://localhost:5000/api/search?q=dark

# Get action movies
curl http://localhost:5000/api/genres/action
```

## 🧠 How It Works

1. **Data Loading** — Movie data (titles, genres, overviews, ratings) is loaded from CSV using Pandas
2. **Feature Engineering** — Genres and overviews are combined into a single text feature per movie
3. **TF-IDF Vectorization** — Text features are converted to numerical vectors using TF-IDF
4. **Cosine Similarity** — A similarity matrix is computed between all movie pairs
5. **Recommendation** — For a given movie, the most similar movies are returned, ranked by similarity score
6. **TMDB Enrichment** — Results are enriched with live poster images and ratings from the TMDB API

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [TMDB](https://www.themoviedb.org/) for the movie database API
- [scikit-learn](https://scikit-learn.org/) for the machine learning utilities
- [Flask](https://flask.palletsprojects.com/) for the web framework
