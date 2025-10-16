import json
import uvicorn 
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles                                   
from html import escape
from fastapi import Body
from pathlib import Path

JSON_FILE = "movies_database.json"   
INDEX_FILE = "templates/index.html"
OMDB_API_KEY = "9603611"
GENERATED_HTML_FILE = "static/generated/movies.html"

def fetch_movie_using_id_from_OMDb(movie_id: str) -> dict:
    '''
    Fetch movie data from OMDb API using the movie id
    Parameters:
    - movie_id: str : IMDb id or title of the movie
    Returns:
    - dict : movie data if found
    '''
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={movie_id}"
    response = requests.get(url)
    return response.json()

def fetch_movie_using_title_from_OMDb(movie_title: str) -> dict:
    '''
    Fetch movie data from OMDb API using the movie title
    Parameters:
    - movie_title: str : title of the movie
    Returns:
    - dict : movie data if found
    '''
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={movie_title}"
    response = requests.get(url)
    return response.json()

def movie_card_html(movie: dict) -> str:
    '''
    Generate HTML for a movie card
    Parameters:
    - movie: dict : movie data
    Returns:
    - str : HTML string for the movie card
    '''
    # Escape to prevent XSS(Cross-Site Scripting) attacks
    # Empty string fallbacks for missing fields
    title = escape(movie.get("Title") or movie.get("title", ""))
    img   = movie.get("Poster") or movie.get("image", "")
    imdb  = movie.get("imdbID") or movie.get("id", "")

    # OMDb sometimes returns "N/A" for Poster
    img_tag = f'<img src="{img}" alt="{title} poster" class="movie-image" />' if img and img != "N/A" else ""

    return f"""
      <div class="movie-card">
        <a href="/movies/{imdb}">
          {img_tag}
          <h2>{title}</h2>
        </a>
      </div>
    """.strip()

def movie_description_html(movie: dict) -> str:
    '''
    Generate HTML for a detailed movie description
    Parameters:
    - movie: dict : movie data
    Returns:
    - str : HTML string for the detailed movie description
    '''
    title = escape(movie.get("Title", "Movie Details"))
    year = escape(movie.get("Year", ""))
    genre = escape(movie.get("Genre", ""))
    director = escape(movie.get("Director", ""))
    poster = escape(movie.get("Poster", ""))
    plot = escape(movie.get("Plot", "No plot available."))
    actors = escape(movie.get("Actors", "N/A"))
    language = escape(movie.get("Language", "N/A"))
    awards = escape(movie.get("Awards", "N/A"))
    imdb_rating = escape(movie.get("imdbRating", "N/A"))

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>{title}</title>
        <link rel="stylesheet" href="/static/styles.css" />
        <style>
            .movie-detail {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }}
            .movie-poster {{
                display: block;
                margin: 0 auto 20px auto;
                max-width: 300px;
                height: auto;
            }}
            .movie-info {{
                max-width: 600px;
            }}
            .movie-info ul {{
                list-style-type: none;
                padding-left: 0;
            }}
        </style>
    </head>
    <body>
        <header class="hero">
            <h1>{title}</h1>
            <p>{year} | {genre} | {director}</p>
        </header>
        <main class="movie-detail">
            <img src="{poster}" alt="{title} Poster" class="movie-poster"/>
            <div class="movie-info">
                <h2>Plot</h2>
                <p>{plot}</p>
                <h2>Details</h2>
                <ul>
                    <li><strong>Actors:</strong> {actors}</li>
                    <li><strong>Language:</strong> {language}</li>
                    <li><strong>Awards:</strong> {awards}</li>
                    <li><strong>IMDB Rating:</strong> {imdb_rating}</li>
                </ul>
            </div>
        </main>
    </body>
    </html>
    """.strip()

def read_movie_from_json_file(file_path: str, movie_id: str):
    ''' 
    Read a movie from a JSON file using the movie id
    Parameters:
    - file_path: str : path to the JSON file
    - movie_id: str : IMDb id of the movie to be read
    Returns:
    - dict : movie data if found
    '''
    try:
        with open(file_path, 'r') as file:
            movies = json.load(file)
            for movie in movies:
                if movie['imdbID'] == movie_id:
                    return movie
            return None
    except FileNotFoundError:
        return None
    
def read_all_movies_from_json_file(file_path: str):
    '''
    Read all movies from a JSON file
    Parameters:
    - file_path: str : path to the JSON file
    Returns:
    - list : list of all movies if file found
    '''
    try:
        with open(file_path, 'r') as file:
            movies = json.load(file)
            return movies
    except FileNotFoundError:
        return []

def write_movie_to_json_file(file_path: str, movie: dict):
    '''
    Create a movie data in a JSON file
    If same movie id exists, update the existing movie data
    with the new one, thereby avoiding duplicates
    Parameters:
    - file_path: str : path to the JSON file
    - movie: dict : movie data to be written
    Returns:
    - dict : movie data if written successfully 
    '''
    try:
        with open(file_path, 'r+') as file:
            movies = json.load(file)
            for i, m in enumerate(movies):
                if m['imdbID'] == movie['imdbID']:
                    movies[i] = movie
                    file.seek(0)
                    json.dump(movies, file, indent=4)
                    file.truncate()
                    return movie
            movies.append(movie)
            file.seek(0)
            json.dump(movies, file, indent=4)
            return movie
    except FileNotFoundError:
        with open(JSON_FILE, 'w') as file:
            json.dump([movie], file, indent=4)
            return movie
    
def update_movie_in_json_file(file_path: str, movie_id: str, movie: dict):
    '''
    Update a movie data in a JSON file using the movie id
    Parameters:
    - file_path: str : path to the JSON file
    - movie_id: str : IMDb id of the movie to be updated
    - movie: dict : updated movie data
    Returns:
    - dict : updated movie data if found and updated
    '''
    try:
        with open(file_path, 'r+') as file:
            movies = json.load(file)
            for i, m in enumerate(movies):
                if m['imdbID'] == movie_id:
                    movies[i] = movie
                    file.seek(0)
                    json.dump(movies, file, indent=4)
                    file.truncate()
                    return movie
            return None
    except FileNotFoundError:
        return None

def delete_movie_from_json_file(file_path: str, movie_id: str):
    '''
    Delete a movie data from a JSON file using the movie id
    Parameters:
    - file_path: str : path to the JSON file
    - movie_id: str : IMDb id of the movie to be deleted
    Returns:
    - dict : deleted movie data if found and deleted
    '''
    try:
        with open(file_path, 'r+') as file:
            movies = json.load(file)
            for i, m in enumerate(movies):
                if m['imdbID'] == movie_id:
                    deleted_movie = movies.pop(i)
                    file.seek(0)
                    json.dump(movies, file, indent=4)
                    file.truncate()
                    return deleted_movie
            return None
    except FileNotFoundError:
        return None

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    ''' Home page '''
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/movies")
def show_movies(request: Request):
    ''' Show all movies '''
    movies = read_all_movies_from_json_file(JSON_FILE)
    # Generate HTML for all movie cards
    # Join them into a single string
    movie_cards = ''.join([movie_card_html(movie) for movie in movies])
    
    # Render index.html and inject movie_cards into it
    index_path = Path(INDEX_FILE)
    if not index_path.exists():
        return HTMLResponse(content="index.html not found", status_code=404)
    with open(index_path, "r", encoding="utf-8") as f:
        index_html = f.read()

    # Replace a placeholder in index.html with movie_cards
    # The placeholder is ***Movie Cards*** in the HTML file
    html_content = index_html.replace("***Movie Cards***", movie_cards)

    # Write the html_content to a file
    output_path = Path(GENERATED_HTML_FILE)
    # Ensure the output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return HTMLResponse(content=html_content, status_code=200)

@app.get("/movies/{movie_id}")
def show_movie_id(request: Request, movie_id: str):
    ''' Show a movie by id '''
    movie = read_movie_from_json_file(JSON_FILE, movie_id)
    if not movie:
        # If movie not found in the database, fetch from OMDb API
        movie = fetch_movie_using_id_from_OMDb(movie_id)
        if not movie or movie.get("Response") == "False":
            return HTMLResponse(content="Movie not found", status_code=404)
        # Save the fetched movie to the database
        write_movie_to_json_file(JSON_FILE, movie)
        # Append the new movie to the movies HTML file
        output_path = Path(GENERATED_HTML_FILE)
        if output_path.exists():
            with open(output_path, "r", encoding="utf-8") as f:
                existing_html = f.read()
            # Insert the new movie card before the closing </div> of movie-container
            new_movie_card = movie_card_html(movie)
            updated_html = existing_html.replace("</div>\n    </main>", f"{new_movie_card}\n        </div>\n    </main>")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(updated_html)

    # Generate HTML for the movie description
    html_content = movie_description_html(movie)

    return HTMLResponse(content=html_content, status_code=200)

@app.post("/movies")
def add_movie(request: Request):
    ''' Add a movie by title using query parameter t '''
    movie_title = request.query_params.get("t", "")
    # Handle invalid title input
    if not movie_title or not movie_title.strip():
        return HTMLResponse(content="Invalid movie title", status_code=400)
    movie_title = movie_title.strip()
    
    movie = fetch_movie_using_title_from_OMDb(movie_title)
    if not movie or movie.get("Response") == "False":
        return HTMLResponse(content="Movie not found", status_code=404)
    
    # Save the fetched movie to the database
    saved_movie = write_movie_to_json_file(JSON_FILE, movie)

    # Append the fetched movie to the movies HTML file
    output_path = Path(GENERATED_HTML_FILE)
    if output_path.exists():
        with open(output_path, "r", encoding="utf-8") as f:
            existing_html = f.read()
        # Insert the new movie card before the closing </div> of movie-container
        new_movie_card = movie_card_html(movie)
        updated_html = existing_html.replace("</div>\n    </main>", f"{new_movie_card}\n        </div>\n    </main>")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(updated_html)

    return saved_movie

@app.put("/movies")
def update_movie(movie: dict = Body(...)):
    ''' Update a movie by id '''

    # Get movie id from the request body
    movie_id = movie.get("imdbID", "")
    if not movie_id or not movie_id.strip():
        return HTMLResponse(content="Invalid movie id", status_code=400)
    movie_id = movie_id.strip()
    
    movie_exists = read_movie_from_json_file(JSON_FILE, movie_id)
    if not movie_exists:
        return HTMLResponse(content="Movie not found", status_code=404)
    
    #Update the movie card in the movies HTML file
    output_path = Path(GENERATED_HTML_FILE)
    if output_path.exists():
        with open(output_path, "r", encoding="utf-8") as f:
            existing_html = f.read()
        # Generate new movie card HTML
        new_movie_card = movie_card_html(movie)
        # Find the existing movie card by searching for the movie ID in the href
        start_index = existing_html.find(f'/movies/{movie_id}')
        if start_index != -1:
            # Find the start of the movie card div
            card_start = existing_html.rfind('<div class="movie-card">', 0, start_index)
            # Find the end of the movie card div
            card_end = existing_html.find('</div>', start_index) + len('</div>')
            # Replace the existing movie card with the new one
            updated_html = existing_html[:card_start] + new_movie_card + existing_html[card_end:]
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(updated_html)

    return update_movie_in_json_file(JSON_FILE, movie_id, movie)

@app.delete("/movies")
def delete_movie(request: Request):
    ''' Delete a movie by id using query parameter i '''
    movie_id = request.query_params.get("i", "")
    if not movie_id or not movie_id.strip():
        return HTMLResponse(content="Invalid movie id", status_code=400)
    movie_id = movie_id.strip()

    movie_exists = read_movie_from_json_file(JSON_FILE, movie_id)
    if not movie_exists:
        return HTMLResponse(content="Movie not found", status_code=404)
    
    # Remove the movie card from the movies HTML file
    output_path = Path(GENERATED_HTML_FILE)
    if output_path.exists():
        with open(output_path, "r", encoding="utf-8") as f:
            existing_html = f.read()
        # Find the existing movie card by searching for the movie ID in the href
        start_index = existing_html.find(f'/movies/{movie_id}')
        if start_index != -1:
            # Find the start of the movie card div
            card_start = existing_html.rfind('<div class="movie-card">', 0, start_index)
            # Find the end of the movie card div
            card_end = existing_html.find('</div>', start_index) + len('</div>')
            # Remove the existing movie card
            updated_html = existing_html[:card_start] + existing_html[card_end:]
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(updated_html)

    return delete_movie_from_json_file(JSON_FILE, movie_id)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
