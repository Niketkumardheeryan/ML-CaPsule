import requests

API_KEY = "Add_API_KEY"

BASE_URL = "https://api.themoviedb.org/3"


def get_movies(movie_name):
    url = f"{BASE_URL}/search/movie"

    params = {
        "api_key": API_KEY,
        "query": movie_name
    }

    response = requests.get(url, params=params).json()

    movies = []

    for movie in response.get("results", [])[:5]:
        movies.append({
            "id": movie["id"],
            "title": movie["title"],
            "image": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie["poster_path"] else "",
            "description": movie["overview"]
        })

    return movies


def get_reviews(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/reviews"

    params = {
        "api_key": API_KEY
    }

    response = requests.get(url, params=params).json()

    reviews = []

    for review in response.get("results", [])[:20]:
        reviews.append(review["content"])

    return reviews