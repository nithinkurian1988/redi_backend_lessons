import json

JSON_FILE = "movies_database.json"

# Read a movie from a JSON file using the movie id
def read_movie_from_json_file(file_path: str, movie_id: int):
    try:
        with open(file_path, 'r') as file:
            movies = json.load(file)
            for movie in movies:
                if movie['id'] == movie_id:
                    return movie
            return {"error": "Movie not found"}
    except FileNotFoundError:
        return {"error": "File not found"}
    
# read all movies from a JSON file
def read_all_movies_from_json_file(file_path: str):
    try:
        with open(file_path, 'r') as file:
            movies = json.load(file)
            return movies
    except FileNotFoundError:
        return {"error": "File not found"}

# create a movie data in a JSON file
# If same movie id exists, update the existing movie data
# with the new one, thereby avoiding duplicates
def write_movie_to_json_file(file_path: str, movie: dict):
    try:
        with open(file_path, 'r+') as file:
            movies = json.load(file)
            for i, m in enumerate(movies):
                if m['id'] == movie['id']:
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
        return {"error": "File not found"}
    
# update a movie data in a JSON file using the movie id
def update_movie_in_json_file(file_path: str, movie_id: int, movie: dict):
    try:
        with open(file_path, 'r+') as file:
            movies = json.load(file)
            for i, m in enumerate(movies):
                if m['id'] == movie_id:
                    movies[i] = movie
                    file.seek(0)
                    json.dump(movies, file, indent=4)
                    file.truncate()
                    return movie
            return {"error": "Movie not found"}
    except FileNotFoundError:
        return {"error": "File not found"}

# delete a movie data from a JSON file using the movie id
def delete_movie_from_json_file(file_path: str, movie_id: int):
    try:
        with open(file_path, 'r+') as file:
            movies = json.load(file)
            for i, m in enumerate(movies):
                if m['id'] == movie_id:
                    deleted_movie = movies.pop(i)
                    file.seek(0)
                    json.dump(movies, file, indent=4)
                    file.truncate()
                    return deleted_movie
            return {"error": "Movie not found"}
    except FileNotFoundError:
        return {"error": "File not found"}

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Nithin-flix"}

# Read all the movies
@app.get("/movies")
def get_movies():
    return read_all_movies_from_json_file(JSON_FILE)

# Read a movie by id
@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    return read_movie_from_json_file(JSON_FILE, movie_id)

# create a movie
@app.post("/movies")
def create_movie(movie: dict):
    return write_movie_to_json_file(JSON_FILE, movie)

# Update a movie by id
@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, movie: dict):
    return update_movie_in_json_file(JSON_FILE, movie_id, movie)

# delete a movie by id
@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    return delete_movie_from_json_file(JSON_FILE, movie_id)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
